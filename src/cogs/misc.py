import discord
from discord.ext import commands
from discord.ext.commands import *
import json
import time

class Misc(commands.Cog):
    def __init__(self, client):
        '''Misc Cog containing commands under the Misc category.'''
        self.client = client
    
    @commands.command()
    @has_permissions(administrator=True)
    async def setprefix(self, ctx: Context, prefix="c!"):
        '''Sets the Bot prefix.'''
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f"The prefix for this server has been set to **{prefix}**")
    
    
    @commands.command()
    @has_permissions(administrator=True)
    async def setbotstatus(self, ctx: Context, *, botstatus='Loki on Disney+'):
        '''Set the Bot's "Watching" status.'''
        if ctx.guild.id == 871048037768790016:
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{botstatus}"))
            await ctx.send(f"Bot status set to **{botstatus}**")
        else:
            await ctx.send("This command can only be executed in the main server")
    
    
    @commands.command()
    async def ping(self, ctx: Context):
        '''Pong!'''
        start_time = time.time()
        await ctx.send("Testing ping...")
        end_time = time.time()
        bot_ping = round(self.client.latency * 1000)
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
        
    
    @commands.command(name="Invite", description="Invite PikaPi!")
    async def invite(self, ctx: Context):
        '''Displays links to invite PikaPi to a server, and to the official Discord server in an Embed.'''
        em = discord.Embed(title="", description="")
        em.add_field(name="Invite PikaPi to your server!", value="https://discord.com/oauth2/authorize?client_id=871051341248737290&scope=bot&permissions=8", inline=False)
        em.add_field(name="Join PikaPi's official Discord server!", value="https://top.gg/servers/871048037768790016", inline=False)
        await ctx.send(embed=em)
    
    @has_permissions(manage_messages=True)
    @commands.command(name="csv", description="Grab the .CSV file from the bot and send it.")
    async def csv(self, ctx: Context):
        '''Grab the .CSV file from the bot and send it.'''
        msg = await ctx.send(content="This will disappear in 2 seconds!", file=discord.File(r"user_info.csv"))
        await msg.delete(delay=2.0)
        await ctx.message.delete(delay=2.0)


def setup(client):
    client.add_cog(Misc(client))