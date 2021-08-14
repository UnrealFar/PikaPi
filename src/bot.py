import json
import os

import discord
from discord.ext import commands
from discord.ext.commands import *
from dotenv import load_dotenv

# import mongodb


load_dotenv()

async def get_prefix(self, ctx: Context) -> str:
    """Gets the Bot prefix from a file according to the guild the Bot is in."""
    # TODO Convert to MongoDB
    if not os.path.exists("./src/data/prefixes.json"):
            with open("./src/data/prefixes.json", "w") as f:
                json.dump({"0": "c!", f"{ctx.guild.id}": "c!"}, f, indent = 4)
    with open("./src/data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return str(prefixes[str(ctx.guild.id)])

async def error(ctx: Context, em: discord.Embed, err: str):
    """Gets the error message and displays a short-notice error message, before removing it 5 seconds after."""
    if em is None:
        em = discord.Embed()
    em.description = err
    await ctx.send(embed=em, delete_after=5.0)
    await ctx.message.delete(delay=5.0)

PERMISSION: list[str] = ["859996173943177226", "268199041542651904", "862304475506933770", "710034974450909185", "870508479977246792"] # ThePikaPi, skirtsandflirts, Draco, Dark King, Sam
TOKEN: str = os.environ['TOKEN']
bot: Bot = commands.Bot(command_prefix=(get_prefix), case_insensitive=True,  activity=discord.Activity(type=discord.ActivityType.playing, name="Discord | Loading..."), status=discord.Status.idle, intents=discord.Intents.all(), description='Development Bot for PikaPi Bot.')
bot.remove_command("help")

@bot.event
async def on_guild_join(guild):
    channel = guild.system_channel
    if channel is not None:
        em = discord.Embed(title="Thank you for adding me to the server!", description="")
        em.add_field(name="", value="If you have'nt already started, do c!start and then c!pick to pick your starter pokémon.")
        em.add_field(name="Configure the bot", value="c!setprefix <new preifix> to set a custom bot prefix for the server! (default: c!)")
        em.add_field(name="Links", value="[Join the PikaPi server!](https://dsc.gg/thepikapi) | [Add the bot to your server!](https://dsc.gg/pikapi)")
        await channel.send(embed=em)
    
    # TODO Convert to MongoDB
    """Event for when the Bot joins a guild."""
    with open('./src/data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "c!"
    with open('./src/data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
    


@bot.event
async def on_guild_remove(guild):
    """Event for when the Bot gets removed from a guild."""
    # TODO Convert to MongoDB
    with open('./src/data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))


@bot.event
async def on_ready():
    """Event for when the Bot is ready."""
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers! | c!cmds"))
    print(f"{bot.user} is ready!")

# TODO Only load the Cog after MongoDB has been set up.
# bot.load_extension("cogs.economy")
bot.load_extension("cogs.help")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.pokemon")
# TODO Only load the Cog after MongoDB has been set up.
# bot.load_extension("cogs.support")

bot.run(TOKEN)
