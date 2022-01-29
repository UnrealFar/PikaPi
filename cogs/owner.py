import discord
import sys, os
from discord.ext import commands

class Owner(commands.Cog):
    """Commands for the owner!"""

    def __init__(self, bot):
        self.bot = bot

    @discord.commands.slash_command(
        name = "restart",
        guild_ids = (873181946786762804,)
    )
    async def restart(self, ctx):
        """Restarts the bot!"""
        if ctx.author.id not in self.bot.owner_ids:
            return await ctx.respond("You don't have perms to restart me!")
        await ctx.respond("Restarting the botto!")
        os.execv(sys.executable, ["python"] + sys.argv)

def setup(bot):
    bot.add_cog(Owner(bot))
