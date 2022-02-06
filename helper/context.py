import discord
from discord.ext import commands
import aiohttp

from typing import Callable, Awaitable

class ApplicationContext(discord.ApplicationContext):

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.bot.session

    @property
    def send(self) -> Callable[..., Awaitable[discord.Message]]:
        return self.channel.send

class CommandContext(commands.Context):

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.bot.session

