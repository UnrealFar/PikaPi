import json
import os
import random

import discord
from discord.ext import commands
from discord.ext.commands import *


class Economy(commands.Cog, name="Economy"):
    def __init__(self, bot):
        """Cog containing commands under the Economy category."""
        self.bot = bot
    
    @commands.command(name="balance", description="Check your Balance.", aliases=["bank", "bal"])
    @commands.cooldown(rate=1, per=0.5)
    async def balance(self, ctx: Context):
        """Check user's balance."""
        if not os.path.exists("./src/data/economy.json"):
            with open("./src/data/economy.json", "w") as f:
                json.dump({"0": {"wallet": 0, "bank": 0}}, f, indent = 4)
        with open("./src/data/economy.json", "r") as f:
            data = json.load(f)
        user_id = str(ctx.author.id)
        if user_id not in data:
            data[user_id] = {}
            data[user_id]["wallet"] = 0
            data[user_id]["bank"] = 0
        with open("./src/data/economy.json", "w") as f:
            f.seek(0)
            json.dump(data, f, indent = 4)
        em = discord.Embed()
        em.colour = discord.Colour.green()
        em.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwebstockreview.net%2Fimages%2Fcongress-clipart-bill-law-8.png&f=1&nofb=1")
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        em.add_field(name="Wallet", value=data[user_id]["wallet"])
        em.add_field(name="Bank", value=data[user_id]["bank"])
        await ctx.send(embed=em)
    
    
    @commands.command(name="beg", description="Beg for some money!")
    @commands.cooldown(rate=1, per=15.0, type=BucketType.user)
    async def beg(self, ctx: Context):
        """Beg for some money! Have a chance to win big."""
        result = random.random()
        em = discord.Embed()
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        if result >= 0.9:
            win_amount = random.randint(1, 50000)
            with open("./src/data/economy.json", "r+") as f:
                data = json.load(f)
                data[str(ctx.author.id)]["wallet"] = win_amount
                json.dump(data, f, indent=4)
            if win_amount <= 1000:
                em.description = f"You won {win_amount} PikaCoins!"
            elif win_amount <= 10000:
                em.description = f"You won {win_amount} PikaCoins! You are now rolling in money (literally). :money_bag:"
            elif win_amount <= 25000:
                em.description = f"You won {win_amount} PikaCoins! Who gives out this much money? :bank:"
            else:
                em.description = f"You won {win_amount} PikaCoins! You are living the life my friend. :sunglasses:"
            em.colour = discord.Colour.green()
        else:
            em.colour = discord.Colour.red()
            em.description = "You won absolutely nothing."
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Economy(bot))
