import json
import os
import random

import discord
from discord.ext.commands import *


class Economy(Cog, name="Economy"):
    def __init__(self, bot):
        """Cog containing commands under the Economy category."""
        self.bot = bot
        if not os.path.exists("./src/data/economy.json"):
            with open("./src/data/economy.json", "w") as f:
                json.dump({"0": {"wallet": 0, "bank": 0}}, f, indent = 4)
    
    async def check_bank(self, ctx: Context):
        """Creates entries for new users."""
        with open("./src/data/economy.json", "r") as f:
            data = json.load(f)
            user_id = str(ctx.author.id)
            if user_id not in data:
                data[user_id] = {"wallet": 0, "bank": 0}
            with open("./src/data/economy.json", "w") as f:
                json.dump(data, f, indent = 4)


    @command(name="balance", description="Check your Balance.", aliases=["bank", "bal"])
    @cooldown(rate=1, per=0.5)
    async def balance(self, ctx: Context):
        """Check user's balance."""
        await self.check_bank(ctx)
        with open("./src/data/economy.json", "r") as f:
            data = json.load(f)
        user_id = str(ctx.author.id)
        em = discord.Embed()
        em.colour = discord.Colour.green()
        em.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwebstockreview.net%2Fimages%2Fcongress-clipart-bill-law-8.png&f=1&nofb=1")
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        em.add_field(name="Wallet", value=data[user_id]["wallet"])
        em.add_field(name="Bank", value=data[user_id]["bank"])
        await ctx.send(embed=em)
    
    
    @command(name="deposit", description="Deposit all your PikaCoins from your wallet into your Bank!")
    @cooldown(rate=1, per=5)
    async def deposit(self, ctx: Context, amount: int):
        """Deposit all the PikaCoins from the Wallet to the Bank."""
        await self.check_bank(ctx)
        
        with open("./src/data/economy.json", "r") as f:
            data = json.load(f)
        
        user_id = str(ctx.author.id)
        wallet = data[user_id]["wallet"]
        bank = data[user_id]["bank"]
        
        em = discord.Embed()
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        em.description = f"You just deposited {amount} PikaCoins into your Bank! Your Bank balance is now: `{bank + amount}`!"
        em.colour = discord.Colour.green()
        
        if wallet < amount:
            em.description = "Your wallet isn't that big! Try depositing a smaller amount."
            em.colour = discord.Colour.red()
            message = await ctx.send(embed=em)
            await message.delete(delay=5.0)
            await ctx.message.delete(delay=5.0)
            return
        
        bank += wallet
        wallet -= amount
        
        await ctx.send(f"Wallet={wallet} and Bank={bank}")
        
        with open("./src/data/economy.json", "w") as f:
            f.seek(0)
            json.dump(data, f, indent=4)
        
        await ctx.send(embed=em)
    
    
    @command(name="beg", description="Beg for some money!")
    @cooldown(rate=1, per=10.0, type=BucketType.user)
    async def beg(self, ctx: Context):
        """Beg for some money! Have a chance to win big."""
        await self.check_bank(ctx)
        result = random.random()
        em = discord.Embed()
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        if result >= 0.75:
            win_amount = random.randint(1, 25000)
            with open("./src/data/economy.json", "r+") as f:
                data = json.load(f)
                data[str(ctx.author.id)]["wallet"] = win_amount
                f.seek(0)
                json.dump(data, f, indent=4)
            if win_amount <= 1000:
                em.description = f"You won {win_amount} PikaCoins!"
            elif win_amount <= 10000:
                em.description = f"You won {win_amount} PikaCoins! You are now rolling in money. :moneybag:"
            else:
                em.description = f"You won {win_amount} PikaCoins! Who gives out this much money? :bank:"
            em.colour = discord.Colour.green()
        else:
            em.colour = discord.Colour.red()
            em.description = "You won absolutely nothing."
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Economy(bot))
