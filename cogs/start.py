from discord.ext import commands
from discord.commands import slash_command
import discord
import os
import json
import random
import requests

class Start(commands.Cog):
    """Start your amazing journey!"""

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def start(self, ctx):
        """Start your awesome journey!"""
        em = discord.Embed(title="Welcome to Pikapi!", description=f"Pick a starter Pokemon with `/pick <pokemon>`")
        em.add_field(name="GEN 1 (KANTO)", value="Bulbasaur · Charmander · Squirtle", inline=False)
        em.add_field(name="GEN 2 (JHOTO)", value="Chikorita · Cyndaquil · Totodile", inline=False)
        em.add_field(name="GEN 3 (HOENN)", value="Treecko · Torchic · Mudkip", inline=False)
        em.add_field(name="GEN 4 (SINNOH)", value="Turtwig ·  Chimchar · Piplup", inline=False)
        em.add_field(name="GEN 5 (UNOVA)", value="Snivy · Tepig · Oshawott", inline=False)
        em.add_field(name="GEN 6 (KALOS)", value="Chespin · Fennekin · Froakie", inline=False)
        em.add_field(name="GEN 7 (ALOLA)", value="Rowlet · Litten · Popplio", inline=False)
        em.add_field(name="GEN 8 (GALAR)", value="Grookey · Scorbunny · Sobble", inline=False)
        await ctx.respond(embed=em)

    @slash_command()
    async def pick(self, ctx, pokemon : str):
        if ctx.guild is None:
            return await ctx.send("You can pick your starter pokemon only in a guild!")

        acc_check = await self.bot.pokedata.get_all()
        checks = []
        counter = 0

        if not acc_check:
            pass

        for i in acc_check:
            checkdata = acc_check[counter]["_id"]
            counter += 1
            checks.append(checkdata)

        if ctx.author.id in checks:
            return await ctx.respond(f"You have already started your journey! Please do `/pokemon` to view your pokemon!")

        with open("starters.json", "r+") as f:
            sdata = json.load(f)
                
        if pokemon.lower() not in sdata:
            return await ctx.respond(f"Sorry, but I couldn't find that starter pokemon. Try `/start` to see the available starter pokemon's!")

        statReq = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}")
        nick = "Starter"
        count = 1
        lvl = 5
        stats = statReq.json()["stats"]
        hp_stat = int(stats[0]["base_stat"])
        atk_stat = int(stats[1]["base_stat"])
        df_stat = int(stats[2]["base_stat"])
        spd_stat = int(stats[5]["base_stat"])
        pokemon = pokemon.lower()

        with open("counter.json", "r") as g:
            pcounter = json.load(g)

        count = count + int(pcounter["pokecounter"])
        pcounter["pokecounter"] = count

        with open("counter.json", "w") as g:
            json.dump(pcounter, g, indent = 4)

        statD = {"name": pokemon, "pNum": count, "lvl": lvl, "hp": hp_stat, "nick": nick, "atk": atk_stat, "df": df_stat, "spd": spd_stat} 
        starterDict = {"_id": ctx.author.id, "p1": {"stats": statD}}
        await self.bot.pokedata.insert(starterDict)
        bal = {"_id": ctx.author.id, "balance": {"coins": 100, "shards": 0}}
        await self.bot.db["economy"].insert_one(bal)
        await ctx.respond(f"You have chosen {pokemon} as your starter pokemon!")

def setup(bot):
    bot.add_cog(Start(bot))
