from typing import List

import aiohttp
import discord
import orjson
from discord.ext import commands
from tortoise import Tortoise
from webserver import app

import db

exts = ("cogs.misc", "cogs.pokemon", "cogs.spawning", "cogs.errors", "cogs.admin", "jishaku")


class PikaPiBotContext(commands.Context):
    async def tick(self, success=True):
        if success:
            await self.message.add_reaction("✅")
        else:
            await self.message.add_reaction("❌")


class PikaPi(commands.Bot):
    r"""The bot object."""

    def __init__(self, **options):
        super().__init__(
            command_prefix=("p.",),
            owner_ids=self.config.OWNER_IDS,
            max_messages=10000,
            strip_after_prefix=True,
            chunk_guilds_at_startup=False,
            intents=discord.Intents(
                guilds=True,
                members=True,
                emojis=True,
                messages=True,
                reactions=True,
                message_content=True,
            ),
            allowed_mentions=discord.AllowedMentions(
                roles=False,
                everyone=False,
                users=True,
            ),
            **options
        )

        self.remove_command("help")
        self.token = self.config.TOKEN
        self.PIKAPI_GUILD_ID = self.config.PIKAPI_GUILD_ID
        self.PIKAPI_INCENSE_ID = self.config.PIKAPI_INCENSE_ID
        self.loaded_extensions = []
        self.received = []
        with open("colour_cache.json", "r") as ccf:
            self.colour_cache = orjson.loads(ccf.read())

        # cache
        self.pokelist: List[db.Species] = []
        with open("blacklist.json", "r") as f:
            self.blacklist = orjson.loads(
                f.read()
            )  # there are not gonna be many guilds/users blacklisted so we just used json

    def run_bot(self):
        return super().run(self.token)

    @property
    def config(self):
        return __import__("config")

    async def load_dbs(self) -> None:
        await Tortoise.init(db_url="sqlite://db/database.sqlite", modules={"models": ["db"]})
        await Tortoise.generate_schemas(safe=True)
        self.capture_rates = list(set([s.capture_rate for s in (await db.Species.all())]))  # ensure they're unique

    async def load_cogs(self) -> None:
        for cog in exts:
            try:
                await self.load_extension(cog)
            except Exception as e:
                print(f"Could not load {cog} due to error: {e}")
            else:
                self.loaded_extensions.append(cog)

    async def setup_hook(self) -> None:
        await self.load_dbs()
        if not hasattr(self, "session"):
            self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop=self.loop)
        self.loghook = discord.Webhook.from_url(url=self.config.LOGHOOK, session=self.session, bot_token=self.token)
        # await self.load_dbs()
        await self.load_cogs()
        await self.tree.sync()

    async def on_ready(self) -> None:
        
        game = discord.Game("Bringing the world of pokemon to Discord!")
        await self.change_presence(status=discord.Status.online, activity=game)
        if not hasattr(self, "launch_time"):
            self.launch_time = discord.utils.utcnow()
        print(self.user, "is ready!")
        if not hasattr(self, 'app'):
            print("Webserver not made")
            self.app = app
            await aiohttp.web._run_app(app, host='0.0.0.0',port=8080)
            print("Webserver made")
    
    async def on_disconnect(self) -> None:
        with open("blacklist.json", "w") as f:
            f.write(orjson.dumps(self.blacklist).decode("utf-8"))
        if not self.session.closed:
            await self.session.close()

    async def on_socket_event_type(self, event_type):
        self.received.append(event_type)

    async def on_guild_join(self, guild: discord.Guild) -> None:
        if guild.id in self.blacklist:
            await guild.leave()
        # TODO: decide if we should add this.
        # user = guild.owner

    # desc = f"I was added to the guild: `{guild.name}`!"
    # try:
    #   async with self.account_db.execute(
    #  """UPDATE accounts
    #  SET pd = pd + 1000, shards = shards + 5
    #  WHERE id = ?
    #  """,
    # (user.id,),
    #  ):
    # await self.account_db.commit()
    #  except:
    #  desc += f"\nCouldn't reward {user} as they haven't registered yet :/"
    # else:
    #  desc += f"\nAdded 1000 coins & 10 shards to {user}"
    # await self.loghook.send(desc)

    async def on_member_join(self, member: discord.Member) -> None:
        return
        if member.guild.id == self.PIKAPI_GUILD_ID:
            try:
                async with self.account_db.execute(
                    """UPDATE accounts
                    SET pd = pd + 1000, shards = shards + 5
                    WHERE id = ?
                    """,
                    (member.id,),
                ):
                    await self.account_db.commit()
            except Exception:
                pass
            finally:
                f"Added 2000 coins & 20 shards to {member}"

    async def on_vote(self, payload: dict):
        ...

    async def get_context(self, message: discord.Message, *, cls=PikaPiBotContext) -> commands.Context:
        return await super().get_context(message, cls=cls)

    async def on_message(self, message: discord.Message):
        if message.author.id in self.blacklist:
            return

        await self.process_commands(message)


bot = PikaPi()
