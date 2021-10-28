import discord
from discord.ext import commands
from discord.commands import slash_command

class Help(commands.Cog, name = "Help command"):
    """Category that holds the help command!"""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Help(bot))
