from discord.ext import commands
import discord

STARTER_POKEMON = ("bulbasaur", "charmander", "squirtle", "chikorita", "cyndaquil", "totodile", "treecko", "torchic", "mudkip", "turtwig", "chimchar", "piplup", "snivy", "tepig", "oshawott", "chespin", "fennekin", "froakie", "rowlet", "litten", "popplio", "grookey", "scorbunny", "sobble")

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @discord.commands.slash_command(
        name = "start"
    )
    async def start(
        self,
        ctx,
        pokemon: discord.Option(
            str,
            "The pokemon partner to begin tour journey with!",
            choices = STARTER_POKEMON
        )
    ):
        acccheck = await self.bot.get_account(ctx.author)
        if acccheck:
            return await ctx.respond("You already have an account!")

        s = await self.bot.new_pokemon({"slug": pokemon})
        acc = await self.bot.create_account(ctx.author)
        await acc.add_pokemon(s)
        return await ctx.respond(f"Congratulations! You have chosen {pokemon} as your partner!")

def setup(bot):
    bot.add_cog(Start(bot))

