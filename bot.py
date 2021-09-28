# Imports

import io
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import time
import datetime
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import random
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")

def get_prefix(bot, message):
    if message.guild != None:
        with open('prefixes.json', 'r') as f: 
            prefixes = json.load(f)
        return prefixes.get(str(message.guild.id), "p!")
    else:
        return ("p!") 

bot = commands.Bot(command_prefix=(get_prefix), case_insensitive=True,  activity=discord.Activity(type=discord.ActivityType.watching, name="Loki on Disney+"), status=discord.Status.idle, intents=discord.Intents.all(), description='Best pokemon bot ever!')
#bot.remove_command("help")

bot.owner_ids = [859996173943177226, 551257232143024139]

# On Ready

@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")

# Events

# on_guild_join

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'p!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

# on_guild_remove

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))

# Prefix 

@bot.command(name = "prefix", )
@has_permissions(administrator=True)
async def setprefix(ctx, prefix="p!"):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f"The prefix for this server has been set to **{prefix}**")


# Battle Command
@bot.command()
async def battle(ctx, member : discord.Member):
    if not member.bot:
        await ctx.reply("Command coming soon.")

    else:
        await ctx.reply("You cannot battle a bot!")

initial_extensions = ["cogs.catch", "cogs.start", "cogs.pokemon", "cogs.errors"]

for extension in initial_extensions:
    bot.load_extension(extension)

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
                helpEm.add_field(name = f"{cmd.name}", value = f"**Usage:** `c!{cmd.name} {cmd.signature}`")
            await ctx.send(embed = helpEm)
            return

    if command:
        if category is None:
            try:
                cmd = bot.get_command(name = f"{command}")
            except:
                await ctx.send(f"Sorry! That command wasn't found! Please do /help <cogname> to view the list of available commands each cog has!")
                return
            helpEm.add_field(name = f"Command: {cmd.name}", value = f"**Usage:** `c!{cmd.name} {cmd.signature}`")
            await ctx.send(embed = helpEm)

# latency

@bot.slash_command(name = "ping")
async def slashping(ctx):
    """🏓 Shows PikaPi's ping"""
    bot_ping = round(bot.latency * 1000)
    pingEm = discord.Embed(title="Pong!", description="", colour = discord.Color.blurple())
    pingEm.add_field(name="Bot Ping", value=f"🏓 {bot_ping}ms", inline=False)
    await ctx.send(embed = pingEm)

bot.run(TOKEN)