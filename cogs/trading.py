from discord.ext import commands
import discord

class Trading(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Trading(bot))
