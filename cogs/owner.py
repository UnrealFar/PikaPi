import discord
import sys, os
from discord.ext import commands
from jishaku.codeblocks import codeblock_converter

from bot import PikaPi
from helper import ApplicationContext

class Owner(commands.Cog):
    """Commands for the owner!"""

    def __init__(self, bot):
        self.bot: PikaPi = bot

    @discord.commands.slash_command(
        name = "run",
        owner_ids = (873181946786762804,)
    )
    async def run(
        self,
        ctx: ApplicationContext,
        code: discord.Option(
            str, "The code to evaluate!"
        )
    ):
        """Run code in Python."""
        if ctx.author.id not in self.bot.owner_ids:
            return await ctx.respond("You need owner permission to run this command!")
        await ctx.respond(f"Running your code!", ephemeral = True)
        try:
            await self.bot.get_cog("Jishaku").jsk_python(ctx, argument = codeblock_converter(code))
        except:
            pass

    @discord.commands.slash_command(
        name = "restart",
        guild_ids = (873181946786762804,)
    )
    async def restart(self, ctx: ApplicationContext):
        """Restarts the bot!"""
        if ctx.author.id not in self.bot.owner_ids:
            return await ctx.respond("You don't have perms to restart me!")
        await ctx.respond("Restarting the botto!")
        os.execv(sys.executable, ["python"] + sys.argv)

def setup(bot):
    bot.add_cog(Owner(bot))
