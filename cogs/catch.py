from discord.ext import commands
import discord
import requests
import random
from bot import get_prefix

import json

uncaught = {}

class Catch(commands.Cog):
    """Catch commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if msg.guild is None:
            return

        spawnper = random.randrange(1, 30)
        prefix = get_prefix(self.bot, msg)

        if spawnper == 15:
            pRange = random.randrange(1, 898)
            req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pRange}")
            pName = req.json()["name"].capitalize()
            pImg = f"https://raw.githubusercontent.com/poketwo/data/master/images/{pRange}.png"
            fledStr = "A wild pokemon just appeared!"
            try:
                fledStr = f"The wild {uncaught[msg.channel.id]} has fled! A new wild pokemon just appeared!"
                uncaught.pop(f"{msg.channel.id}")
            except:
                pass
            uncaught[f"{msg.channel.id}"] = f"{pName.lower()}"

            em = discord.Embed(title = f"{fledStr}", description = f"Type `{prefix}catch <pokemon>` to catch it!")
            em.set_image(url = pImg)
            await msg.channel.send(embed = em)

    @commands.command(aliases = ["c"])
    async def catch(self, ctx, *, pokemon: str):
        prefix = get_prefix(self.bot, ctx.message)
        pokemon = pokemon.lower()

        try:
            tbc = uncaught[f"{ctx.channel.id}"]
        except:
            await ctx.reply("There are no wild pokemon! ||Please note that wild pokemon are reset on bot restart!||")
            return

        if pokemon != tbc:
            await ctx.send("That's the wrong pokemon!")
            return

        if pokemon == tbc:
            with open("caught.json", "r") as f:
                c = json.load(f)

            if str(ctx.author.id) not in c:
                await ctx.reply(f"You haven't started yet! Use `{prefix}start` to start!")
                return

            d = c[str(ctx.author.id)]
            counter = len(d) + 1
            pokeDict = {counter : f"{tbc.lower()}"}
            c[str(ctx.author.id)].update(pokeDict)

            with open("caught.json", "w") as f:
                json.dump(c, f, indent=4)

            await ctx.send(f"Congratulations {ctx.author.mention}! You caught a {tbc.capitalize()}")
            uncaught.pop(f"{ctx.channel.id}")

def setup(bot):
    bot.add_cog(Catch(bot))
