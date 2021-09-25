from discord.ext import commands
import discord

import json

class Catch(commands.Cog):
    """The description for Catch goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokemon(self, ctx):
        with open("selected-starter.json", "r") as f:
            starter = json.load(f)

        pokemon = ""
        
        starter = starter.get(str(ctx.author.id), pokemon)

        # with open("caught.json", "r") as f:

        #  caught = json.load(f)

        # caught = caught.get(str(ctx.author.id), # missing arg)

        # await ctx.reply(caught)

        em = discord.Embed(title="**Your Pokemon**", description=f"Here is a list of {ctx.author.name}'s pokemon!", color=0xffff00)

        em.add_field(name="Starter", value=f"{starter.capitalize()}", inline=False)

        await ctx.reply(embed=em)

def setup(bot):
    bot.add_cog(Catch(bot))
