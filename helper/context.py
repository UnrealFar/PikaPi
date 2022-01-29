import discord
from discord.ext import commands

import aiohttp

class ApplicationContext(discord.ApplicationContext):

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.bot.session

class CommandContext(commands.Context):

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.bot.session

