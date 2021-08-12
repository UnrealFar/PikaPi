import csv
import discord
from discord.ext import commands
from discord.ext.commands import *
import json
import os

def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

class Pokemon(commands.Cog):
    def __init__(self, client):
        '''Pokemon Cog containing commands under the Pokemon category.'''
        self.client = client
    
    @commands.command(name="Start", description="Start your awesome journey!")
    async def start(self, ctx):
        '''Displays all starting pokemon in an Embed.'''
        em=discord.Embed(name="Welcome to Chuckmon!", description=f"Pick a starter Pokemon with {get_prefix(self.client, ctx)}pick <pokemon>")
        em.add_field(name="GEN 1 (KANTO)", value="Bulbasaur · Charmander · Squirtle", inline=False)
        em.add_field(name="GEN 2 (JHOTO)", value="Chikorita · Cyndaquil · Totodile", inline=False)
        em.add_field(name="GEN 3 (HOENN)", value="Treecko · Torchic · Mudkip", inline=False)
        em.add_field(name="GEN 4 (SINNOH)", value="Turtwig · Chimchar · Piplup", inline=False)
        em.add_field(name="GEN 5 (UNOVA)", value="Snivy · Tepig · Oshawott", inline=False)
        em.add_field(name="GEN 6 (KALOS)", value="Chespin · Fennekin · Froakie", inline=False)
        em.add_field(name="GEN 7 (ALOLA)", value="Rowlet · Litten · Popplio", inline=False)
        em.add_field(name="GEN 8 (GALAR)", value="Grookey · Scorbunny · Sobble", inline=False)
        await ctx.send(embed=em)
    
    @commands.command(name="Pick", description="Pick your starter pokemon!")
    async def pick(self, ctx: Context, arg: str):
        '''Locks in a starter pokemon for that user.'''
        if not os.path.exists("user_info.json"):   
            with open("user_info.json", "w") as f:
                json.dump({"users": {}}, f)
        if not os.path.exists("pokemon.json"):   
            with open("pokemon.json", "w") as f:
                json.dump({"pokemon": [],"starters": []}, f)
        with open("pokemon.json", "r+") as f:
            data = json.load(f)
            if arg.lower() not in data["starters"]:
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


def setup(client):
    client.add_cog(Pokemon(client))