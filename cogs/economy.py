import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = self.bot.economy

    @slash_command(name = "balance")
    async def _balance(
        self, 
        ctx,
        currency: Option(
            str,
            "Choose the currency!",
            choices = ["coins", "shards"],
            default = "coins"
        )
    ):
        account = await self.economy.find({"_id": ctx.author.id})
        if account is None:
            acc = await self.bot.pokedata.find({"_id": ctx.author.id})
            if acc is None:
                return await ctx.respond("You do not have an account! Please do `/start` to start your journey!")
            await self.economy.insert({"_id": ctx.author.id, "coins": 100, "shards": 0})
            account = await self.economy.find({"_id": ctx.author.id})

        coins = account["coins"]
        shards = account["shards"]

        balEm = discord.Embed(title = f"{ctx.author.name}'s balalnce")
        balEm.add_field(name = "Coins", value = coins, inline = False)
        balEm.add_field(name = "Shards", value = shards)

        await ctx.respond(embed = balEm)

def setup(bot):
    bot.add_cog(Economy(bot))