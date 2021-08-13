import json

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


def setup(bot):
    bot.add_cog(Misc(bot))
