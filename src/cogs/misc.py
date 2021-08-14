import json

import discord
from discord.ext.commands import *


class Misc(Cog, name="Misc"):
    def __init__(self, bot):
        """Cog containing commands under the Misc category."""
        self.bot = bot
    
    @command(name="setprefix", description="Set the Bot prefix for your server!")
    @cooldown(rate=1, per=5)
    @has_permissions(administrator=True)
    async def setprefix(self, ctx: Context, prefix="c!"):
        """Sets the Bot prefix for the server."""
        # TODO Convert to MongoDB
        with open('./src/data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('./src/data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        em = discord.Embed()
        em.description = f"The prefix for this server has been set to `{prefix}`"
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        em.add_field(name="Links", value="[GitHub](https://github.com/ThePikaPi/PikaPi/) | [PikaPi Discord Server](https://dsc.gg/thepikapi) | [Invite PikaPi to your server!](https://dsc.gg/pikapi)", inline=False)
        await ctx.send(embed=em)
    
    
    @command(name="ping", description="Test the Bot latency!", aliases=["latency"])
    @cooldown(rate=1, per=5)
    async def ping(self, ctx: Context):
        """Pong!"""
        websocket_latency = round(self.bot.latency * 1000)
        if websocket_latency <= 100:
            bpsignal = "<:online:874181086312280064>"
        elif websocket_latency >= 101:
            bpsignal = "<:idle:874181495886065664>"
        elif websocket_latency >= 300:
            bpsignal = "<:dnd:874181456472182864>"
        em = discord.Embed()
        em.title="Pong!"
        em.colour = discord.Color.blurple()
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        em.add_field(name="Websocket Latency", value=f"{bpsignal} {websocket_latency}ms", inline=False)
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Misc(bot))
