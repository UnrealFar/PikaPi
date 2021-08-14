import json

import discord
from bot import PERMISSION, error
from discord.ext.commands import *


class Support(Cog, name="Support"):
    def __init__(self, bot):
        """Cog containing commands under the Support category."""
        self.bot = bot

    @command(name="editcoins", description="Add money to a person's wallet!")
    @cooldown(rate=1, per=2)
    async def editcoins(self, ctx: Context, user: discord.Member, amount: int, account: str = None):
        """Edits a User's Wallet or Bank."""
        em = discord.Embed()
        
        if str(ctx.author.id) in PERMISSION:
            if account is None:
                account = "bank"
            # TODO Convert to MongoDB
            with open(r".\src\data\economy.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)][account] += amount
                f.seek(0)
                json.dump(data, f, indent=4)
            if amount < 0:
                em.add_field(name="Successful!", value=f"Removed `{-amount}` PikaCoins from {user.mention}'s {account}.")
            else:
                em.add_field(name="Successful!", value=f"Added `{amount}` PikaCoins to {user.mention}'s {account}.")
            await ctx.send(embed = em)
        else:
            await error(ctx, em, "You don't have access to this command!")
            return

def setup(bot):
    bot.add_cog(Support(bot))
