from discord.ext import commands
import discord
from discord import app_commands
from db import Account

class Accounts(commands.Cog):
    """Pokemon accounts"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def account(self, i, user: discord.User | None = None):
        user = user or i.user
        user_poke_account = Account.get_or_create(id=user.id)
        await i.response.send_message(user_poke_account.balance)
        
        

async def setup(bot):
    await bot.add_cog(Accounts(bot))
