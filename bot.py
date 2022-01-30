import discord
from discord.ext import commands
import models
import aiohttp
import helper
import random
import os
import numpy
from typing import (
    Union
)
from motor.motor_asyncio import AsyncIOMotorClient

from webserver import app

MONGO_URI = os.environ.get("mongo_uri")

class PikaPi(commands.Bot):
    r"""The bot object.
    """
    def __init__(self):
        super().__init__(
            command_prefix = "p.",
            owner_ids = (859996173943177226,),
            allowed_mentions = discord.AllowedMentions(
                roles = False,
                everyone = False,
                users = True
            )
        )

        self.remove_command("help")

        self.helper: helper = helper
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop = self.loop)

        # Load our exts here
        self.load_extension("cogs.help")
        self.load_extension("cogs.utilities")
        self.load_extension("cogs.start")
        self.load_extension("cogs.owner")
        self.load_extension("jishaku")


        # Database stuff
        db = dict()
        self.mongo = AsyncIOMotorClient(MONGO_URI)
        metadata = self.mongo["METADATA"]
        userdata = self.mongo["USERDATA"]
        db["pokedata"] = helper.Mongo(metadata["pokemon"])
        self.pokedata: helper.Mongo = db["pokedata"]
        db["accounts"] = helper.Mongo(userdata["accounts"])
        self.accounts: helper.Mongo = db["accounts"]
        
        self.db: dict[str, helper.Mongo] = db

    async def get_account(
        self,
        user: Union[discord.User, discord.Member]
    ) -> models.User:
        payload = await self.accounts.find_one({"_id": user.id})
        if not payload: 
            return None
            
        payload["bot"] = self
        return models.User.get_account(payload)

    async def create_account(
        self,
        user: Union[discord.User, discord.Member]
    ) -> models.User:
        return await models.User.create_account(self, user.id)

    async def get_pokemon(self, **kwargs) -> models.Pokemon:
        return models.Pokemon(await self.pokedata.find_one(kwargs))

    async def fetch_pokemon(self, **kwargs) -> models.Pokemon:
        if "shiny" not in kwargs:
            sh = {"t": True, "f": False}
            shiny = numpy.random.choice(
                ["f", "t"], p = [0.999, 0.001]
            )
            shiny = sh[shiny]
        else: shiny = kwargs.pop("shiny")
        poke = await self.pokedata.find_one(kwargs)
        if not poke: return None
        poke["bot"] = self
        poke = await models.Pokemon.new_pokemon(**poke)
        poke.shiny = shiny
        return poke

    async def spawn_pokemon(self, shiny = False, **kwargs) -> models.Pokemon:
        if "rarity" not in kwargs:
            kwargs["rarity"] = numpy.random.choice(
                ["normal", "leg", "myth", "ub"],
                p = [0.9825, 0.001, 0.005, 0.0025]
            )
        poke = random.choice((i async for i in self.pokedata.find_one(kwargs)))
        poke["bot"] = self
        poke = await models.Pokemon.new_pokemon(poke)

        if not shiny:
            sh = {"t": True, "f": False}
            shiny = numpy.random.choice(
                ["f", "t"], p = [0.999, 0.001]
            )
        poke.shiny = sh[shiny]
        return poke

    async def on_ready(self):
        if not hasattr(self, "site"):
            self.site = app
            self.loop.create_task(
                app.run_task(
                    host = "0.0.0.0",
                    port = 8080
                )
            )
        print(self.user, "is ready!")

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message, cls = helper.CommandContext)
        await self.invoke(ctx)

    async def get_application_context(self, interaction: discord.Interaction):
        return await super().get_application_context(interaction, cls = helper.ApplicationContext)

    # Blacklist related stuff to be added later

