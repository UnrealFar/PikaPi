import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name = "balance")
    async def _balance(
        self, 
        ctx
    ):
        accounts = await self.bot.economy.get_all()
        account = self.bot.db["economy"].find_one({"_id": ctx.author.id})

        if account is None:
            acc = await self.bot.db["pokedata"].find_one({"_id": ctx.author.id})

            if acc is None:
                return await ctx.respond("You do not have an account! Please do `/start` to start your journey!")
            else:
                await self.bot.economy.insert({"_id": ctx.author.id, "balance": {"coins": 100, "shards": 0}})

        accounts = await self.bot.db["economy"].find_one({"_id": ctx.author.id})

        coins = account["balance"]["coins"]
        shards = account["balance"]["shards"]

        balEm = discord.Embed(
            title = f"{ctx.author.name}'s balalnce",
            colour = discord.Colour.red()
        )
        balEm.set_thumbnail(url = ctx.author.display_avatar.url)
        balEm.add_field(name = "Coins", value = coins, inline = False)
        balEm.add_field(name = "Shards", value = shards)

        await ctx.respond(embed = balEm)

def setup(bot):
    bot.add_cog(Economy(bot))