from discord.ext import commands
from discord.commands import slash_command
import discord
import bot

class Misc(commands.Cog):
    """Miscellaneous commands that do not fit anywhere else"""

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def invite(self, ctx):
        iE = discord.Embed(title = "My Invite Links!", colour = discord.Colour.red())
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label = "https://discord.com/oauth2/authorize?client_id=871051341248737290&permissions=8&scope=bot%20applications.commands", style = discord.ButtonStyle.url))
        view.add_item(discord.ui.Button(label = "Join the support server!", url = "https://discord.gg/Vu7G79rvwW", style = discord.ButtonStyle.url))
        await ctx.respond(embed = iE, view = view)

def setup(bot):
    bot.add_cog(Misc(bot))
