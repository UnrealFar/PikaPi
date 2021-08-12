import discord
from discord.ext import commands
from discord.ext.commands import *
import json

class Economy(commands.Cog):
    def __init__(self, client):
        '''Economy Cog containing commands under the Economy category.'''
        self.client = client
        
        async def open_account(user):
            
            users = await get_bank_data()
            
            if str(user.id) in users:
                return False
            else:
                users[str(user.id)] = {}
                users[str(user.id)]["wallet"] = 0
                users[str(user.id)]["bank"] = 0
            with open("bank.json", "w") as f:
                json.dump(users, f)
        
        async def get_bank_data():
            with open("bank.json", "r") as f:
                users = json.load(f)
            return users


        @commands.command(name="Balance", description="Check your Balance.")
        async def balance(self, ctx: Context):
            '''Check user's balance.'''
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()
            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]
            
            em=discord.Embed(name=f"{ctx.author.name}'s Balance:", colour=discord.Colour.green(), avatar="../res/economy/avatar.png")
            em.add_field(name="Wallet", value=wallet_amt)
            em.add_field(name="Bank", value=bank_amt)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Economy(client))