import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        accounts = await self.bot.economy.get_all()
        account = None
        for accs in accounts:
            if accs["_id"] == ctx.author.id:
                account = accs
                break

        if account is None:
            ta = await self.bot.pokedata.get_all()
            acc = None
            for acct in ta:
                if acct["_id"] == ctx.author.id:
                    acc = acct
                    break

            if acc is None:
                return await ctx.respond("You do not have an account! Please do `/start` to start your journey!")
            else:
                await self.bot.economy.insert({"_id": ctx.author.id, "balance": {"coins": 100, "shards": 0}})

        accounts = await self.bot.economy.get_all()
        account = None
        for accs in accounts:
            if accs["_id"] == ctx.author.id:
                account = accs
                break

        coins = account["balance"]["coins"]
        shards = account["balance"]["shards"]

        balEm = discord.Embed(title = f"{ctx.author.name}'s balalnce")
        balEm.add_field(name = "Coins", value = coins, inline = False)
        balEm.add_field(name = "Shards", value = shards)

        await ctx.respond(embed = balEm)

def setup(bot):
    bot.add_cog(Economy(bot))