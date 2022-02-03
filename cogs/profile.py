import discord
from discord.ext import commands

from helper import ApplicationContext, EmbedPaginator
from bot import PikaPi

class Profile(commands.Cog):
    """Profile related commands."""

    def __init__(self, bot):
        self.bot: PikaPi = bot

    @discord.commands.slash_command(
        name = "profile",
    )
    async def profile(
        self,
        ctx: ApplicationContext,
        user: discord.Option(
            discord.Member,
            "The user of whomst profile you want to see.",
            required = False
        )
    ):
        """Get your's or another member's PikaPi profile!"""
        user = user if user else ctx.author
        acc = await self.bot.get_account(user)
        if not acc:
            return await ctx.respond(f"{user} does not have an account!")
        badges = "".join(acc.badges)
        caught = f"""
        **Total**: {acc.caught.get("t")}
        **Normal**: {acc.caught.get("n")}
        **Legendary**: {acc.caught.get("l")}
        **Mythical**: {acc.caught.get("m")}
        **Ultra Beast**: {acc.caught.get("u")}
        **Shiny**: {acc.caught.get("s")}
        """
        embed = discord.Embed(
            title = f"{user}'s profile!",
            colour = discord.Colour.red()
        )
        embed.add_field(name = "Catch stats!", value = caught)
        bal = f"**Coins**: {acc.bal.get('c')}\n**Shards**: {acc.bal.get('s')}"
        embed.add_field(name = "Balance", value = bal)
        if len(badges) >= 1:
            embed.add_field(name = "Badges", value = badges)
        embed.set_thumbnail(url = user.display_avatar.url)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar.url)
        await ctx.respond(embed = embed)

    @discord.commands.slash_command(
        name = "pokemon",
    )
    async def all_pokemon(self, ctx: ApplicationContext):
        """View all the Pokemon that you have caught!"""
        acc = await self.bot.get_account(ctx.author)
        if not acc:
            return await ctx.respond("You haven't started your journey yet!")
        all_pokes = [poke async for poke in acc.all_pokemon()]
        pag = commands.Paginator(
            prefix = "",
            suffix = "",
            max_size = 350
        )
        for p_id, poke in all_pokes:
            pag.add_line(f"`{p_id}` - **{poke.names.get('en')}** - Lvl. {(poke.level)}\n")
        em = discord.Embed(
            title = f"{ctx.author}'s Pokemon",
            description = pag.pages[0]
        )
        em.set_thumbnail(url = ctx.author.display_avatar.url)
        pag = EmbedPaginator(pag, ctx.author, embed = em)
        await ctx.respond(embed = em, view = pag)

    @discord.commands.slash_command(
        name = "info",
        guild_ids = (873181946786762804,)
    )
    async def info(
        self,
        ctx: ApplicationContext,
        pokemon_id: discord.Option(
            int,
            "The Pokemon which should be searched for!"
        )
    ):
        """Get information for a Pokemon that you have caught!"""
        acc = await self.bot.get_account(ctx.author)
        if not acc:
            return await ctx.respond("Sorry! You do not have an account! Please use `/start <pokemon>` to begin your journey!")
        poke = await acc.get_pokemon(pokemon_id)
        if not poke:
            return await ctx.respond(f"Sorry! You do not have a Pokemon with the ID {pokemon_id}")
        stats = poke.stats
        desc = f"""
        __***Stats***__
        **HP:** `{stats.get('hp')}`
        **Attack:** `{stats.get('atk')}`
        **Defence:** `{stats.get('df')}`
        **Sp. Atk.:** `{stats.get('satk')}`
        **Sp. Def.:** `{stats.get('sdf')}`
        **Total IV:** `{poke.iv}%`
        """
        embed = discord.Embed(title = f"Level {poke.level} {poke}", description = desc, colour = discord.Colour.og_blurple())
        embed.set_image(url = "attachment://pokemon.png")
        embed.set_thumbnail(url = ctx.author.display_avatar.url)
        await ctx.respond(embed = embed, file = await poke.get_image())


def setup(bot):
    bot.add_cog(Profile(bot))
