from discord.ext import commands
from discord.commands import slash_command, Option
import discord
import requests
import random
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

        if spawnper == 3:
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

            em = discord.Embed(title = f"{fledStr}", description = f"Type `/catch <pokemon>` to catch it!")
            em.set_image(url = pImg)
            await msg.channel.send(embed = em)

    @slash_command(aliases = ["c"])
    @commands.cooldown(1, 1, commands.BucketType.channel)
    async def catch(self, ctx, pokemon: str):
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(' ', '-')
        author_id = ctx.author.id

        try:
            tbc = uncaught[f"{ctx.channel.id}"]
        except:
            await ctx.respond("There are no wild pokemon! Please note that wild pokemon are reset on bot restart!")
            return

        if pokemon != tbc:
            await ctx.respond("That's the wrong pokemon!")
            return


        acc_check = await self.bot.pokedata.get_all()
        checkdata = False

        for account in acc_check:
            if account["_id"] == author_id:
                checkdata = True

        if checkdata is False:
            return await ctx.respond("You haven't started your journey yet! Please do `/start` to start your journey!")

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

        with open("counter.json", "w") as g:
            json.dump(pcounter, g, indent = 4)

        statD = {"name": pokemon, "pNum": count, "lvl": lvl, "hp": hp_stat, "nick": nick, "atk": atk_stat, "df": df_stat, "spd": spd_stat}
        await self.bot.pokedata.update_by_id({"_id": ctx.author.id, f"p{count}": {"stats": statD}})
        bal = await self.bot.economy.find({"_id": ctx.author.id})
        if bal is None:
            await self.bot.economy.insert({"_id": ctx.author.id, "balance": {"coins": 130, "shards": 0}})
        elif bal:
            old_bal = bal["balance"]["coins"]
            old_shards = bal["balance"]["shards"]
            new_bal = int(old_bal) + 30
            await self.bot.economy.upsert({"_id": ctx.author.id, "balance": {"coins": new_bal, "shards": old_shards}})
        tbc = tbc.replace("-", " ")
        await ctx.respond(f"Congratulations {ctx.author.mention}! You caught a level **{lvl}** {tbc.capitalize()}!\nAdded 30 coins to your balance!")
        uncaught.pop(f"{ctx.channel.id}")

def setup(bot):
    bot.add_cog(Catch(bot))
