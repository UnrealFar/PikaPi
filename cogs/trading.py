from discord.ext import commands
from discord.commands import slash_command
import discord

class Trading(commands.Cog):
    """Commands for the trading system!"""

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def trade(self, ctx, member: discord.Member):
        return await ctx.respond("Not ready for use")

def setup(bot):
    bot.add_cog(Trading(bot))
