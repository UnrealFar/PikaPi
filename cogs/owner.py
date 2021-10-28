from discord.ext import commands
from discord.commands import slash_command
import discord
import json
import asyncio
import os
import requests
import bot

class Owner(commands.Cog):
    """Commands for the owner!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        """Enables/Disables a command!"""
        command = self.bot.get_command(command)

        if command is None:
            return await ctx.send("I can't find a command with that name!")

        elif ctx.command == command:
            return await ctx.send("You cannot disable this command")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} **`{command.qualified_name}`**!")

    @slash_command()
    @commands.is_owner()
    async def reloadall(self, ctx):
        async with ctx.typing():
            for ext in os.listdir("./cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.reload_extension(f"cogs.{ext[:-3]}")
                        await ctx.send(f"Realoaded {ext[:-3]}!")
                        await asyncio.sleep(1)
                    except Exception as e:
                        await ctx.send(e)
                        return
            await ctx.respond("Done reloading all cogs :)")

    @slash_command()
    @commands.is_owner()
    async def give(self, ctx, member: discord.Member,  pokemon):
        check = await self.bot.db["pokedata"].find_one({"_id": member.id})
        if check is None:
            return await ctx.respond(f"{member.mention} does not have a PikaPi account!")
        statReq = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}")
        nick = ""
        count = 1
        lvl = random.randrange(5, 21)
        try:
            stats = statReq.json()["stats"]
        except:
            return await ctx.respond(f"Pokemon called {pokemon} was not found!")
        hp_stat = int(stats[0]["base_stat"])
        atk_stat = int(stats[1]["base_stat"])
        df_stat = int(stats[2]["base_stat"])
        spd_stat = int(stats[5]["base_stat"])

        with open("counter.json", "r") as g:
            pcounter = json.load(g)

        count = count + int(pcounter["pokecounter"])
        pcounter["pokecounter"] = count

        with open("counter.json", "w") as g:
            json.dump(pcounter, g, indent = 4)

        statD = {"name": pokemon, "pNum": count, "lvl": lvl, "hp": hp_stat, "nick": nick, "atk": atk_stat, "df": df_stat, "spd": spd_stat}
        await self.bot.pokedata.update_by_id({"_id": ctx.author.id, f"p{count}": {"stats": statD}})
        await ctx.respond(f"Added a {pokemon} of level {level}")

def setup(bot):
    bot.add_cog(Owner(bot))
