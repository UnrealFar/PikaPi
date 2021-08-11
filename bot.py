import csv
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import Context
import json
import time
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ['TOKEN']
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]
client = commands.Bot(command_prefix=(get_prefix), case_insensitive=True,  activity=discord.Activity(type=discord.ActivityType.watching, name="Loki on Disney+"), status=discord.Status.idle, intents=discord.Intents.all(), description='Best pokemon bot ever!')
client.remove_command("help")

#setprefix(server admins only)
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

@client.command()
@has_permissions(administrator=True)
async def setprefix(ctx, prefix="c!"):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f"The prefix for this server has been set to **{prefix}**")

#setstatus(mainserveradminsonly)
@client.command()
@has_permissions(administrator=True)
async def setbotstatus(ctx, *, botstatus='Loki on Disney+'):
    if ctx.guild.id == 871048037768790016:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{botstatus}"))
        await ctx.send(f"Bot status set to **{botstatus}**")
    else:
        await ctx.send("This command can only be executed in the main server")

#ping
@client.command()
async def ping(ctx: commands.Context):
    start_time = time.time()
    await ctx.send("Testing ping...")
    end_time = time.time()
    bot_ping = round(client.latency * 1000)
    api_ping = round((end_time - start_time) * 1000)
    if bot_ping <= 100:
        bpsignal = "<:online:874181086312280064>"
    elif bot_ping >=101:
        bpsignal = "<:idle:874181495886065664>"
    elif bot_ping>=300:
        bpsignal = "<:dnd:874181456472182864>"
    if api_ping <= 100:
        apisignal = "<:online:874181086312280064>"
    elif api_ping >=101:
        apisignal = "<:idle:874181495886065664>"
    elif api_ping >= 300:
        apisignal = "<:dnd:874181456472182864>"
    pingEm = discord.Embed(title="Pong!", description="", colour = discord.Color.blurple())
    pingEm.add_field(name="Bot Ping", value=f"{bpsignal}  {bot_ping}ms", inline=False)
    pingEm.add_field(name="API Ping", value=f"{apisignal} {api_ping}ms", inline=False)
    await ctx.send(embed = pingEm)

#Start Journey
@client.command(name="Start", description="Start your awesome journey!")
async def start(ctx):
    em=discord.Embed(name="Welcome to Chuckmon!", description=f"Pick a starter Pokemon with {get_prefix}pick <pokemon>")
    em.add_field(name="GEN 1 (KANTO)", value="Bulbasaur · Charmander · Squirtle", inline=False)
    em.add_field(name="GEN 2 (JHOTO)", value="Chikorita · Cyndaquil · Totodile", inline=False)
    em.add_field(name="GEN 3 (HOENN)", value="Treecko · Torchic · Mudkip", inline=False)
    em.add_field(name="GEN 4 (SINNOH)", value="Turtwig · Chimchar · Piplup", inline=False)
    em.add_field(name="GEN 5 (UNOVA)", value="Snivy · Tepig · Oshawott", inline=False)
    em.add_field(name="GEN 6 (KALOS)", value="Chespin · Fennekin · Froakie", inline=False)
    em.add_field(name="GEN 7 (ALOLA)", value="Rowlet · Litten · Popplio", inline=False)
    em.add_field(name="GEN 8 (GALAR)", value="Grookey · Scorbunny · Sobble", inline=False)
    await ctx.send(embed=em)
    
#pick
@client.command(name="Pick", description="Pick your starter pokemon!")
async def pick(ctx: Context, arg: str):
    if not os.path.exists("user_info.json"):   
        with open("user_info.json", "w") as f:
            json.dump({"users": {}}, f)
    if not os.path.exists("pokemon.json"):   
        with open("pokemon.json", "w") as f:
            json.dump({"pokemon": [],"starters": []}, f)
    with open("pokemon.json", "r+") as f:
        data = json.load(f)
        if arg.lower() not in data["starters"]:
            print(data)
            print(data["starters"])
            await ctx.send("This is not a valid starter pokemon!")
            return
    with open("user_info.json", "r+") as f:
        data = json.load(f)
        userid = str(ctx.author.id)
        if userid not in data["users"]:
            data["users"][userid] = {"starter": arg.lower(), "pokemon": []}
            f.seek(0)
            json.dump(data, f)
            await ctx.send(f"Congratulations! You have picked {arg.capitalize()} as your starter pokemon!")
        else:
            await ctx.send("You have already started your journey!")
            return
        with open("user_info.json") as f:
            data = json.load(f)
        with open("user_info.csv", "w", newline="") as f:
            print(data["users"])
            headers = ["USER", "STARTER", "POKEMON"]
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for user in data["users"]:
                    writer.writerow(dict(USER="ID_"+user, STARTER=data["users"][user]["starter"], POKEMON=data["users"][user]["pokemon"]))

# INVITE COMMAND
@client.command(name="Invite", description="See the invite link for PikaPi!")
async def invite(ctx: Context):
    em = discord.Embed
    em.description = "https://discord.com/oauth2/authorize?client_id=871051341248737290&scope=bot&permissions=8"
    ctx.send(embed=em)

#ready
@client.event
async def on_ready():
    print(f"{client.user} is ready!")

client.run(TOKEN)