import discord
from discord.ext import commands, tasks
import json
import os
from dotenv import load_dotenv
import random
import asyncio
import motor.motor_asyncio
from utils.mongo import Document
from discord.ext.buttons import Paginator

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

bot = commands.Bot(command_prefix = get_prefix,case_insensitive=True, activity=discord.Activity(type=discord.ActivityType.watching, name="Pokemon"), status=discord.Status.dnd, intents=discord.Intents.all(), description='Best pokemon bot ever!')
#bot.remove_command("help")
bot.owner_ids = [859996173943177226, 551257232143024139]

@bot.listen()
async def on_ready():
    print(f"{bot.user} is ready!")
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    bot.db = bot.mongo["DATA"]
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

@bot.listen()
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'p!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@bot.listen()
async def on_guild_remove(guild):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes.pop(str(guild.id))
    except:
        return

# Battle Command
@bot.command()
async def battle(ctx, member : discord.Member):
    if not member.bot:
        await ctx.reply("Command coming soon.")

    else:
        await ctx.reply("You cannot battle a bot!")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
bot.load_extension("jishaku")

#help
@bot.slash_command()
async def help(ctx, command: str = None, category: str = None):
    helpEm = discord.Embed(title = "PikaPi's Help Menu", description = f"Do /help <command> to get more info abt that command and /help <category> to get more info about a category!", colour = 0x9CCFFF)
    helpEm.set_thumbnail(url = bot.user.display_avatar.url)
    helpEm.set_footer(icon_url = ctx.author.display_avatar.url, text = f"Requested by {ctx.author}")

    if command is None:
        if category is None:
            cogs_desc = ""
            for cog in bot.cogs:
                cogs_desc += f"`{cog}` {bot.cogs[cog].__doc__}\n"
            helpEm.add_field(name = "Cogs", value = cogs_desc, inline=False)
            await ctx.send(embed = helpEm)
            return

    if category:
        if command:
            await ctx.send("Sorry! You can only select either command or category!")
        if not command:
            try:
                cogname = category.lower()
                cogname = cogname.capitalize()
                cog = bot.get_cog(name = f"{cogname}")
                commands = cog.get_commands()
            except:
                await ctx.send(f"Cog called {cogname} was not found! Please do /help to view the list of available cogs!")
                return
            for cmd in commands:
                helpEm.add_field(name = f"{cmd.name}", value = f"**Usage:** `p!{cmd.name} {cmd.signature}`")
            await ctx.send(embed = helpEm)
            return

    if command:
        if category is None:
            try:
                cmd = bot.get_command(name = f"{command}")
            except:
                await ctx.send(f"Sorry! That command wasn't found! Please do /help <cogname> to view the list of available commands each cog has!")
                return
            helpEm.add_field(name = f"Command: {cmd.name}", value = f"**Usage:** `p!{cmd.name} {cmd.signature}`")
            await ctx.send(embed = helpEm)

# latency

@bot.slash_command(name = "ping")
async def slashping(ctx):
    """🏓 Shows PikaPi's ping"""
    bot_ping = round(bot.latency * 1000)
    pingEm = discord.Embed(title="Pong!", description="", colour = discord.Color.blurple())
    pingEm.add_field(name="Bot Ping", value=f"🏓 {bot_ping}ms", inline=False)
    await ctx.send(embed = pingEm)

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

bot.run(TOKEN)