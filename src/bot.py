import discord
from discord.ext import commands
from discord.ext.commands import *
import json
#from dotenv import load_dotenv
#load_dotenv()
#TOKEN = os.environ['TOKEN']
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]
client = commands.Bot(command_prefix=(get_prefix), case_insensitive=True,  activity=discord.Activity(type=discord.ActivityType.watching, name="Loki on Disney+"), status=discord.Status.idle, intents=discord.Intents.all(), description='Best pokemon bot ever!')
client.remove_command("help")

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'c!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))


@client.event
async def on_ready():
    print(f"{client.user} is ready!")


client.load_extension("cogs.economy")
client.load_extension("cogs.misc")
client.load_extension("cogs.pokemon")

client.run("ODYxODI1NTM1MDAwNDQ0OTQ4.YOPbkw.3pWMgyaELb6XA-tEkOzfpySAmqM")