# Imports

import io
import csv
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
from dotenv import load_dotenv
from cogs.catch import setup

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
bot.remove_command("help")

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
    prefixes[str(guild.id)] = 'c!'
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

@bot.event
async def on_message(msg):
    spawnper = random.randrange(1, 30)
    prefix = get_prefix(bot, msg)
    pokerange = random.randrange(1, 898)    

    pokemon = f"https://raw.githubusercontent.com/poketwo/data/master/images/{pokerange}.png"

    if spawnper == 15:
        em = discord.Embed(title="A new pokemon appeared!", description=f"Type `{prefix}catch <pokemon>` to catch it!")
        em.set_image(url=pokemon)
        await msg.channel.send(embed=em)

    await bot.process_commands(msg)

initial_extensions = ["cogs.catch", "cogs.start"]

for extension in initial_extensions:
    bot.load_extension(extension)

# latency

@bot.slash_command(name = "ping", guild_ids = [890877039463260170])
async def slashping(ctx):
    """🏓 Shows PikaPi's ping"""
    bot_ping = round(bot.latency * 1000)
    pingEm = discord.Embed(title="Pong!", description="", colour = discord.Color.blurple())
    pingEm.add_field(name="Bot Ping", value=f"🏓 {bot_ping}ms", inline=False)
    await ctx.send(embed = pingEm)

bot.run(TOKEN)