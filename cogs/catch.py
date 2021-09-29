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

        spawnper = random.randrange(1, 51)
        
        prefix = get_prefix(self.bot, msg)

        if spawnper == 15:
            pRange = random.randrange(1, 898)
            rarC = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pRange}")
            pLegC = rarC.json()["is_legendary"]
            pMytC = rarC.json()["is_mythical"]
            lc = [1, 5]
            mc = [1, 3]
            if pLegC == "true":
                lc = random.choice(lc)
                if lc != 3:
                    return
            if pMytC == "true":
                mc = random.choice(mc)
                if mc != 2:
                    return
            req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pRange}")
            pName = req.json()["name"].capitalize()
            pImg = f"https://raw.githubusercontent.com/poketwo/data/master/images/{pRange}.png"
            fledStr = "A wild pokemon just appeared!"
            try:
                uncaught.pop(f"{msg.channel.id}")
            except:
                pass
            uncaught[f"{msg.channel.id}"] = f"{pName.lower()}"

            em = discord.Embed(title = f"{fledStr}", description = f"Type `{prefix}catch <pokemon>` to catch it!")
            em.set_image(url = pImg)
            await msg.channel.send(embed = em)

    @commands.command(aliases = ["c"])
    @commands.cooldown(1, 1, commands.BucketType.channel)
    async def catch(self, ctx, *, pokemon: str):
        prefix = get_prefix(self.bot, ctx.message)
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(' ', '-')

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

            statReq = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}")
            nick = ""
            count = 1
            lvl = random.randrange(5, 21)
            stats = statReq.json()["stats"]
            hp_stat = int(stats[0]["base_stat"])
            atk_stat = int(stats[1]["base_stat"])
            df_stat = int(stats[2]["base_stat"])
            spd_stat = int(stats[5]["base_stat"])

            with open("counter.json", "r") as g:
                pcounter = json.load(g)

            count = count + int(pcounter["pokecounter"])
            pcounter["pokecounter"] = count

            d = c[str(ctx.author.id)]
            counter = len(d) + 1
            statD = {"name": tbc.lower(), "perm_id": count, "nick": nick, "lvl": lvl, "hp": hp_stat, "atk": atk_stat, "df": df_stat, "spd": spd_stat}
            pokeDict = {counter : statD}
            c[str(ctx.author.id)].update(pokeDict)

            with open("caught.json", "w") as f:
                json.dump(c, f)

            with open("counter.json", "w") as g:
                json.dump(pcounter, g, indent = 4)

            await ctx.send(f"Congratulations {ctx.author.mention}! You caught a level **{lvl}** {tbc.capitalize()}")
            uncaught.pop(f"{ctx.channel.id}")

def setup(bot):
    bot.add_cog(Catch(bot))
