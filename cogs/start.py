from discord.ext import commands
import discord
from bot import get_prefix
import os
import json
import random
import requests

class Start(commands.Cog):
    """Start your amazing journey!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Start your awesome journey!")
    async def start(self, ctx):
        prefix = get_prefix(self.bot, ctx.message)
        
        em = discord.Embed(title="Welcome to Pikapi!", description=f"Pick a starter Pokemon with `{prefix}pick <pokemon>`")
        em.add_field(name="GEN 1 (KANTO)", value="Bulbasaur · Charmander · Squirtle", inline=False)
        em.add_field(name="GEN 2 (JHOTO)", value="Chikorita · Cyndaquil · Totodile", inline=False)
        em.add_field(name="GEN 3 (HOENN)", value="Treecko · Torchic · Mudkip", inline=False)
        em.add_field(name="GEN 4 (SINNOH)", value="Turtwig ·  Chimchar · Piplup", inline=False)
        em.add_field(name="GEN 5 (UNOVA)", value="Snivy · Tepig · Oshawott", inline=False)
        em.add_field(name="GEN 6 (KALOS)", value="Chespin · Fennekin · Froakie", inline=False)
        em.add_field(name="GEN 7 (ALOLA)", value="Rowlet · Litten · Popplio", inline=False)
        em.add_field(name="GEN 8 (GALAR)", value="Grookey · Scorbunny · Sobble", inline=False)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.default)
    async def pick(self, ctx, *, pokemon : str):
        prefix = get_prefix(self.bot, ctx.message)

        if os.path.exists("caught.json"):

            with open("caught.json", "r") as f:
                data = json.load(f)

            if str(ctx.author.id) in data:
                await ctx.reply(f"You already have a starter pokemon! Use `{prefix}pokemon` to view it!")
                return

            with open("starters.json", "r+") as f:
                data = json.load(f)
                
                if pokemon.lower() not in data:
                    await ctx.reply(f"Sorry, but I couldn't find that starter pokemon. Try `{prefix}start` to see the available starter pokemon's!")
                    return

            statReq = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}")
            nick = ""
            lvl = 5
            stats = statReq.json()["stats"]
            hp_stat = int(stats[0]["base_stat"])
            atk_stat = int(stats[1]["base_stat"])
            df_stat = int(stats[2]["base_stat"])
            spd_stat = int(stats[5]["base_stat"])

            with open("caught.json", "r") as f:
                choice = json.load(f)

            statD = {"name": pokemon.lower(), "lvl": lvl, "hp": hp_stat, "nick": nick, "atk": atk_stat, "df": df_stat, "spd": spd_stat}
            starterDict = {1 : statD}
            choice[str(ctx.author.id)] = starterDict

            with open("caught.json", "w") as f:
                json.dump(choice, f, indent = 4)
                await ctx.reply(f"{pokemon.capitalize()} was selected as your starter pokemon!")

def setup(bot):
    bot.add_cog(Start(bot))
