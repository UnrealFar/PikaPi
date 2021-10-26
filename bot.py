import asyncio
import json
import os
import random
import time

import discord
import motor.motor_asyncio
from discord.ext import commands, tasks
from discord.ext.buttons import Paginator
from dotenv import load_dotenv
from jishaku.help_command import MinimalEmbedPaginatorHelp

from utils.mongo import Document

load_dotenv()

TOKEN = os.getenv("TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
DEFAULT_PREFIX = "p!"

async def get_prefix(bot, message):
    if message.guild is None:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)

    try:
        data = await bot.prefixes.find(message.guild.id)
        if not data or "prefix" not in data:
            return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)

    except:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)

class PikaPi(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix,
            case_insensitive = True,
            activity = discord.Activity(
                type = discord.ActivityType.watching,
                name = f"pokemon!"
                ),
            status = discord.Status.dnd,
            intents = discord.Intents.all(),
            description = "Best Pokemon bot ever!",
            shard_count = 1
        )

        self.owner_ids = [859996173943177226, 551257232143024139, 552097487347777536]

bot = PikaPi()
bot.remove_command("help")

@bot.listen()
async def on_ready():
    print("Logging in...")
    await asyncio.sleep(3)
    start = f"Logged in as {bot.user} with ID: {bot.user.id}\n----------\nServer count: {len(bot.guilds)}\n----------\nShard count: {bot.shard_count}"
    print(start)
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    bot.db = bot.mongo["DATA"]
    bot.pokedata = Document(bot.db, "admin")
    bot.command_usage = Document(bot.db, "command_usage")
    bot.prefixes = Document(bot.db, "prefixes")

@bot.listen()
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(f"<@!{bot.user.id}>"):
        data = await bot.prefixes.get_by_id(message.guild.id)

        if not data or "prefix" not in data:
            prefix = DEFAULT_PREFIX

        else:
            prefix = data["prefix"]

        await message.channel.send(f"My prefix in this server is {prefix}")

# latency
@bot.slash_command(name = "ping")
async def slashping(ctx):
    """🏓 Shows PikaPi's ping"""
    bot_ping = round(bot.latency * 1000)
    start_time = time.monotonic()
    await bot.mongo.admin.command("ping")
    end_time = time.monotonic()
    db_ping = int((end_time - start_time) * 1000)
    pingEm = discord.Embed(title="Pong!", description="", colour = discord.Color.blurple())
    pingEm.add_field(name = "Bot Ping", value = f"🏓 **{bot_ping} ms**", inline = False)
    pingEm.add_field(name = "Database ping", value = f"🏓 **{db_ping} ms**")
    await ctx.respond(embed = pingEm)

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("Confirmed!", ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelled!", ephemeral=True)
        self.value = False
        self.stop()

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except:
            pass

bot.help_command = MinimalEmbedPaginatorHelp()
bot.run(TOKEN)
