import json
import os

import discord
from discord.ext import commands
from discord.ext.commands import *
from dotenv import load_dotenv

load_dotenv()

def get_prefix(ctx: Context) -> str:
    """Gets the Bot prefix from a file according to the guild the Bot is in."""
    if not os.path.exists("./src/data/prefixes.json"):
            with open("./src/data/prefixes.json", "w") as f:
                json.dump({"0": "c!", f"{ctx.guild.id}": "c!"}, f, indent = 4)
    with open("./src/data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(ctx.guild.id)]

# TODO Get the User's Banner colour.
# USER_COLOUR = discord.Colour.from_rgb() # Use this in conjunction with the User Banner colour to set for personalised embeds.
PERMISSION = ["268199041542651904", "859996173943177226"]
TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix=(get_prefix), case_insensitive=True,  activity=discord.Activity(type=discord.ActivityType.playing, name="Discord | Loading..."), status=discord.Status.idle, intents=discord.Intents.all(), description='Development Bot for PikaPi Bot.')
bot.remove_command("help")


@bot.event
async def on_command_error(ctx: Context, exception: CommandError):
    """Event for when a command produces an error."""
    em = discord.Embed()
    em.description = str(exception)
    await ctx.send(embed=em, delete_after=5.0)
    await ctx.message.delete(delay=5.0)

@bot.event
async def on_guild_join(guild):
    """Event for when the Bot joins a guild."""
    with open('./src/data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "c!"
    with open('./src/data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)


@bot.event
async def on_guild_remove(guild):
    """Event for when the Bot gets removed from a guild."""
    with open('./src/data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))


@bot.event
async def on_ready():
    """Event for when the Bot is ready."""
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers! | c!cmds"))
    print(f"{bot.user} is ready!")
    
bot.load_extension("cogs.economy")
bot.load_extension("cogs.help")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.pokemon")

bot.run(TOKEN)
