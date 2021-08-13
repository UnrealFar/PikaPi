import csv
import json
from bot import PERMISSION

import discord
from discord.ext.commands import *


class Misc(Cog, name="Misc"):
    def __init__(self, bot):
        """Cog containing commands under the Misc category."""
        self.bot = bot
    
    @command(name="setprefix", description="Set the Bot prefix for your server!")
    @cooldown(rate=1, per=0.5)
    @has_permissions(administrator=True)
    async def setprefix(self, ctx: Context, prefix="c!"):
        """Sets the Bot prefix for the server."""
        with open('./src/data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('./src/data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f"The prefix for this server has been set to **{prefix}**")
    
    
    @command(name="ping", description="Test the Bot latency!", aliases=["latency"])
    @cooldown(rate=1, per=0.5)
    async def ping(self, ctx: Context):
        """Pong!"""
        websocket_latency = round(self.bot.latency * 1000)
        if websocket_latency <= 100:
            bpsignal = "<:online:874181086312280064>"
        elif websocket_latency >= 101:
            bpsignal = "<:idle:874181495886065664>"
        elif websocket_latency >= 300:
            bpsignal = "<:dnd:874181456472182864>"
        em = discord.Embed(title="Pong!", description="", colour = discord.Color.blurple())
        em.add_field(name="Websocket Latency", value=f"{bpsignal} {websocket_latency}ms", inline=False)
        await ctx.send(embed = em)
    
    
    @command(name="csv", description="Grab the .csv file from the bot and send it.")
    @cooldown(rate=1, per=0.5)
    async def csv(self, ctx: Context):
        """Grab the .csv file from the bot and send it."""
        if str(ctx.author.id) not in PERMISSION:
            return
        with open("./src/data/user_info.json") as f:
            data = json.load(f)
        with open("./src/data/user_info.csv", "w", newline="") as f:
            headers = ["USER", "STARTER", "POKEMON"]
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for user in data["users"]:
                    writer.writerow(dict(USER="ID_"+user, STARTER=data["users"][user]["starter"], POKEMON=data["users"][user]["pokemon"]))
        message = await ctx.send(content="This will disappear in 2 seconds!", file=discord.File("./src/data/user_info.csv"))
        await message.delete(delay=2.0)
        await ctx.message.delete(delay=2.0)


def setup(bot):
    bot.add_cog(Misc(bot))
