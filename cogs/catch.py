from discord.ext import commands
import discord, random, asyncio
from helper import ApplicationContext
from models import Pokemon, User

class Catch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hint_cooldown = []

    @discord.commands.slash_command(
        name = "catch",
    )
    async def catch_command(
        self,
        ctx: ApplicationContext,
        pokemon: discord.Option(
            str,
            "The Pokemon you want to catch!",
            required = True
        )
    ):
        r"""Catch a wild Pokemon that has spawned in your channel!
        """
        pokemon: str = pokemon.lower().replace("shiny ", "")
        acc: User = await self.bot.get_account(ctx.author)
        if not acc:
            return await ctx.respond(
                "Sorry! You do not have an account!"
            )
        poke: Pokemon = self.bot.uncaught.get(ctx.channel.id)
        if not poke:
            return await ctx.respond(
                "No wild Pokemon have spawned in this channel! Please note that wild Pokemon are reset on bot restart!"
            )

        if (
            (poke.slug.lower() == pokemon)
            or
            (pokemon in (p for p in poke.names.values()))
        ):
            desc = f"Congratulations! You have caught a {poke.names['en'].title()} of level **{round(poke.level)}**"
            if poke.shiny:
                desc += f"\n\nThese colours seem unusual... ✨✨"
            await acc.add_pokemon(poke)
            success = discord.Embed(
                title = "New Catch!",
                description = desc,
                colour = discord.Colour.og_blurple()
            )
            await ctx.respond(embed = success)
            self.bot.uncaught.pop(ctx.channel.id, None)
        else:
            await ctx.respond(f"Sorry, {pokemon} is not the pokemon!")

    @discord.commands.slash_command(
        name = "hint",
    )
    async def hint(self, ctx: ApplicationContext):
        """Get a hint to the Pokemon that spawned in the channel."""
        if ctx.channel.id in self.hint_cooldown:
            return await ctx.respond(
                "This command is on cooldown! Please try again later!"
            )
        poke = self.bot.uncaught.get(ctx.channel.id)
        if not poke:
            return await ctx.respond("There are no wild Pokemon in this channel!")
        ret = ""
        for char in poke.names.get('en'):
            ret += char if random.choice((False, True, False)) == True else "_"
        await ctx.respond(f"`{ret}`")
        self.hint_cooldown.append(ctx.channel.id)
        await asyncio.sleep(7)
        try:
            self.hint_cooldown.remove(ctx.channel.id)
        except:
            return

def setup(bot):
    bot.add_cog(Catch(bot))
