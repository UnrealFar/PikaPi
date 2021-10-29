import discord
from discord.ext import commands, tasks
import random
import aiohttp
import requests
import io

class Incense(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.incenses = {903619675940859904: 9999999}

    @commands.Cog.listener()
    async def on_ready(self):
        self.incenseloop.start()

    @tasks.loop(seconds = 30)
    async def incenseloop(self):
        incenses = list(self.bot.incenses)
        for channelid in incenses:
            channel = self.bot.get_channel(int(channelid))

            pRange = random.randrange(1, 898)
            rarC = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pRange}")
            pLegC = rarC.json()["is_legendary"]
            pMytC = rarC.json()["is_mythical"]
            lc = [1, 5]
            mc = [1, 3]
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://pokeapi.co/api/v2/pokemon/{pRange}") as req:
                    req = await req.json()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://raw.githubusercontent.com/poketwo/data/master/images/{pRange}.png") as img_url:
                    imgbytes = io.BytesIO(await img_url.content.read())
            pName = req["name"].capitalize()
            img = discord.File(imgbytes, filename = "pokemon.png")
            fledStr = "A wild pokemon just appeared!"
            fledP = None
            try:
                fledP = self.bot.uncaught.pop(f"{msg.channel.id}")
            except:
                pass
            self.bot.uncaught[f"{channelid}"] = f"{pName.lower()}"

            if fledP is not None:
                fledStr = f"A wild {fledP} fled! A new wild pokemon has appeared!"

            em = discord.Embed(title = f"{fledStr}", description = f"Type `/catch <pokemon>` to catch it!")
            em.set_image(url = "attachment://pokemon.png")
            remaining = self.bot.incenses[channelid]
            em.set_footer(text = f"Remaining: {remaining - 1}")
            try:
                await channel.send(file = img, embed = em)
            except:
                pass
            self.bot.incenses[channelid] = remaining - 1
            if self.bot.incenses[channelid] == 0:
                del self.bot.incenses[channelid]

def setup(bot):
    bot.add_cog(Incense(bot))