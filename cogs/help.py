from discord.ext import commands
import bot

class Help(commands.Cog, name="Help command"):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Help(bot))