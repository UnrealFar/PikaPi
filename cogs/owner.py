from discord.ext import commands
import discord
import json
import asyncio
import bot

class Owner(commands.Cog):
    """Commands for the owner!"""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Owner(bot))
