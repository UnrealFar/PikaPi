import discord
from discord.ext import commands
import models
import aiohttp
import helper
import random
import os
import numpy
from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient

from webserver import app

PIKAPI_GUILD_ID = 871048037768790016

class PikaPi(commands.Bot):
    r"""The bot object.
    """
    def __init__(self):
        super().__init__(
            command_prefix = "p.",
            owner_ids = (859996173943177226, 661508161529708564),
            allowed_mentions = discord.AllowedMentions(
                roles = False,
                everyone = False,
                users = True
            )
        )

        #self.remove_command("help")

        self.helper: helper = helper
        self.token = os.environ.get("token")
        self.mongo_uri = os.environ.get("mongo_uri")

        # cache
        self.uncaught = {}

        # Load our exts here
        self.load_extension("cogs.help")
        self.load_extension("cogs.utilities")
        self.load_extension("cogs.start")
        self.load_extension("cogs.owner")
        self.load_extension("cogs.catch")
        self.load_extension("cogs.dex")
        self.load_extension("cogs.profile")
        self.load_extension("jishaku")


        # Database stuff
        db = dict()
        mongo = AsyncIOMotorClient(self.mongo_uri)
        metadata = mongo["METADATA"]
        userdata = mongo["USERDATA"]
        self.pokedata: helper.Mongo = helper.Mongo(metadata["pokemon"])
        self.accounts: helper.Mongo = helper.Mongo(userdata["accounts"])
        
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

    async def get_pokemon(self, kwargs) -> models.Pokemon:
        d = await self.pokedata.find_one(kwargs)
        if d:
            d["bot"] = self
            return models.Pokemon(d)

    async def new_pokemon(self, kwargs) -> models.Pokemon:
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
        poke.shiny = shiny if not getattr(poke, "shiny", None) else poke.shiny
        return poke

    async def spawn_pokemon(self, shiny = False, **kwargs) -> models.Pokemon:
        if "rarity" not in kwargs:
            kwargs["rarity"] = numpy.random.choice(
                ["normal", "leg", "myth", "ub"],
                p = [0.9925, 0.004, 0.001, 0.0025]
            )

        pl = [p async for p in self.pokedata.find(kwargs)]
        poke = random.choice(pl)
        poke["bot"] = self
        poke = await models.Pokemon.new_pokemon(**poke)

        if not shiny:
            sh = {"t": True, "f": False}
            shiny = numpy.random.choice(
                ["f", "t"], p = [0.999, 0.001]
            )
            poke.shiny = sh[shiny]
        else: 
            poke.shiny = shiny
        return poke

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        if not hasattr(self, "session"):
            self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        if not hasattr(self, "site"):
            self.site = app
            self.loop.create_task(
                app.run_task(
                    host = "0.0.0.0",
                    port = 8080
                )
            )
        if not hasattr(self, "loghook"):
            self.loghook = discord.Webhook.from_url(
                url = os.environ.get("loghook"),
                session = self.session,
                bot_token = self.token
            )
        print(self.user, "is ready!")

    async def on_guild_join(self, guild: discord.Guild):
        try:
            entries = await guild.audit_logs(
                limit = 10,
                action = discord.AuditLogAction.bot_add
            ).flatten()
        except:
            return
        entry = None
        for en in entries:
            if getattr(en.target, "id", None) == self.user.id:
                entry = en
                break

        if not entry:
            return
        user = entry.user
        acc = await self.get_account(user)
        if acc:
            await acc.add_bal(coins = 1000, shards = 10)
        desc = f"I was added to the guild: {guild.name} by {user}!"
        if acc:
            desc += f"\nAdded 1000 coins and 10 shards to {user}"
        await self.loghook.send(desc)

    async def on_message(self, msg: discord.Message):
        await self.spawn_from_message(msg)
        await self.process_commands(msg)

    async def spawn_from_message(self, message: discord.Message):
        if message.author.bot or (message.guild == None):
            return
        chance = numpy.random.choice(["t", "f"],p = [0.05, 0.95])
        if chance == "f":
            return
        poke = await self.spawn_pokemon()
        if not poke:
            return
        img = await poke.get_image()
        channel = message.channel
        if channel.id in self.uncaught:
            d = self.uncaught[channel.id]
            t = f"The {d.names.get('en', d.slug).title()} has fled! A new wild pokemon has appeared!"
        else:
            t = "A wild pokemon has appeared!"
        sendEm = discord.Embed(title = t,description = "Type /catch <pokemon> to catch it!",colour = discord.Colour.og_blurple())
        sendEm.set_image(url = "attachment://pokemon.png")
        try:
            await channel.send(embed = sendEm,file = img)
        except:
            pass
        else:
            self.uncaught[channel.id] = poke

    async def get_context(self, message: discord.Message, cls = None):
        return await super().get_context(message, cls = helper.CommandContext)

    async def get_application_context(self, interaction: discord.Interaction):
        return await super().get_application_context(interaction, cls = helper.ApplicationContext)

    # Blacklist related stuff to be added later

PikaPi().run()
