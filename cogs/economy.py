import discord
from json import load
from discord.ext import commands
from discord.commands import slash_command, Option

with open("shop.json", "r") as s:
    shop = load(s)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name = "balance")
    async def _balance(
        self, 
        ctx
    ):
        account = self.bot.db["economy"].find_one({"_id": ctx.author.id})

        if account is None:
            acc = await self.bot.db["pokedata"].find_one({"_id": ctx.author.id})

            if acc is None:
                return await ctx.respond("You do not have an account! Please do `/start` to start your journey!")
            else:
                await self.bot.economy.insert({"_id": ctx.author.id, "balance": {"coins": 100, "shards": 0}})

        account = await self.bot.db["economy"].find_one({"_id": ctx.author.id})

        coins = account["balance"]["coins"]
        shards = account["balance"]["shards"]

        balEm = discord.Embed(
            title = f"{ctx.author.name}'s balalnce",
            colour = discord.Colour.red()
        )
        balEm.set_thumbnail(url = ctx.author.display_avatar.url)
        balEm.add_field(name = "Coins", value = coins, inline = False)
        balEm.add_field(name = "Shards", value = shards)

        await ctx.respond(embed = balEm)

    @slash_command()
    async def shop(
        self,
        ctx,
        page: Option(str, "Specific page of the shop", required = False, choices = [page for page in shop])
    ):
        shopEm = discord.Embed(colour = discord.Colour.blue())
        shopEm.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar.url)
        account = self.bot.db["economy"].find_one({"_id": ctx.author.id})

        if account is not None:
            shopEm.set_author(f"{ctx.author}'s balance: {account['balance']['coins']}coins, {account['balance']['shards']}shards")

        if page is None:
            shopEm.title = "Shop"
            shopEm.description = "Welcome to the shop! Here you can buy various items that will help you in your journey!"
            for page in shop:
                pn = shop[page]["name"]
                pd = shop[page]["description"]
                shopEm.add_field(name = pn, value = pd)
            return await ctx.respond(embed = shopEm)

        else:
            pn = shop[page]["name"]
            pd = shop[page]["description"]
            shopEm.title = pn
            shopEm.description = pd
            for item in shop[page]["items"]:
                itemname = item
                desc = item["description"]
                cost = item["cost"]
                shopEm.add_field(name = itemname, value = f"**Description:** *{desc}*\nCost: **{cost}**coins")
            
            return await ctx.respond(embed = shopEm)

def setup(bot):
    bot.add_cog(Economy(bot))