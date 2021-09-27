from discord.ext import commands
import discord
import requests
import json

class Pokedex(commands.Cog):
    """Pokedex Stuff"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "pokedex", aliases = ["d", "dex"])
    async def pokedex(self, ctx, *, pokemon):
        resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        try:
            pname = resp.json()["name"].capitalize()
        except:
            await ctx.send(f"Pokemon called **`{pokemon}`** doesn't exist!")
            return
        pID = resp.json()["id"]
        pImg = f"https://raw.githubusercontent.com/poketwo/data/master/images/{pID}.png"
        ptypes = resp.json()["types"]
        ptype1 = ptypes[0]["type"]["name"].capitalize()
        try:
            ptype2 = ptypes[1]["type"]["name"].capitalize()
        except:
            ptype2 = ""
        try:
            ptype3 = ptypes[2]["type"]["name"].capitalize()
        except:
            ptype3 = ""
        try:
            ptype4 = ptypes[3]["type"]["name"].capitalize()
        except:
            ptype4 = ""
        pheight = resp.json()["height"]
        pheight = float(pheight / 10)
        pweight = resp.json()["weight"]
        pweight = float(pweight / 10)
        dexEm = discord.Embed(title = f"#{pID} {pname}", colour = discord.Colour.dark_blue())
        dexEm.add_field(name = "Types", value = f"{ptype1}\n{ptype2}\n{ptype3}\n{ptype4}", inline = False)
        dexEm.add_field(name = "Appearance", value = f"**Height**: {pheight}m\n**Weight**: {pweight}kg", inline = False)
        dexEm.set_image(url = pImg)
        await ctx.send(embed = dexEm)

def setup(bot):
    bot.add_cog(Pokedex(bot))
