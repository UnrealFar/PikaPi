import json
import os

import discord
from bot import error, get_prefix
from discord.ext.commands import *


class Pokemon(Cog, name="Pokemon"):
    def __init__(self, bot):
        """Cog containing commands under the Pokemon category."""
        self.bot = bot
        # TODO Convert to MongoDB
        if not os.path.exists("./src/data/user_info.json"):   
            with open("./src/data/user_info.json", "w") as f:
                json.dump({"users": {"0": {"starter": "", "pokemon": []}}}, f, indent = 4)
        if not os.path.exists("./src/data/pokemon.json"):   
            with open("./src/data/pokemon.json", "w") as f:
                # TODO mongodb all pokemon from api
                json.dump({}, f, indent = 4)
    
    @command(name="start", description="Start your awesome journey!")
    @cooldown(rate=1, per=5)
    async def start(self, ctx: Context):
        """Displays all starting pokemon in an Embed."""
        em=discord.Embed()
        em.description = f"Pick a starter Pokemon with {await get_prefix(self.bot, ctx)}pick <pokemon>"
        em.add_field(name="GEN 1 (KANTO)", value="Bulbasaur · Charmander · Squirtle", inline=False)
        em.add_field(name="GEN 2 (JHOTO)", value="Chikorita · Cyndaquil · Totodile", inline=False)
        em.add_field(name="GEN 3 (HOENN)", value="Treecko · Torchic · Mudkip", inline=False)
        em.add_field(name="GEN 4 (SINNOH)", value="Turtwig · Chimchar · Piplup", inline=False)
        em.add_field(name="GEN 5 (UNOVA)", value="Snivy · Tepig · Oshawott", inline=False)
        em.add_field(name="GEN 6 (KALOS)", value="Chespin · Fennekin · Froakie", inline=False)
        em.add_field(name="GEN 7 (ALOLA)", value="Rowlet · Litten · Popplio", inline=False)
        em.add_field(name="GEN 8 (GALAR)", value="Grookey · Scorbunny · Sobble", inline=False)
        await ctx.send(embed=em)
    
    
    @command(name="pick", description="Pick your starter pokemon!")
    @cooldown(rate=1, per=5)
    async def pick(self, ctx: Context, pokemon: str):
        """Locks in a starter pokemon for that user."""
        # TODO Convert to MongoDB
        with open("./src/data/pokemon.json", "r") as f:
            data = json.load(f)
            em = discord.Embed()
            if pokemon.lower() not in data["starters"]:
                await error(ctx, em, "That is not a valid starter pokemon!")
                return
        with open("./src/data/user_info.json", "r+") as f:
            data = json.load(f)
            userid = str(ctx.author.id)
            if userid not in data["users"]:
                data["users"][userid] = {"starter": pokemon.lower(), "pokemon": [pokemon.lower()]}
                f.seek(0)
                json.dump(data, f, indent = 4)
                em.description = f"Congratulations! You have picked {pokemon.capitalize()} as your starter pokemon!"
            else:
                await error(ctx, em, "You have already started your journey!")
                return
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Pokemon(bot))
