from discord.ext import commands
from discord.commands import slash_command, Option
from discord.commands import commands as cmds
import discord
import aiohttp
import random
import asyncio
import io
import json

class Catch(commands.Cog):
    """Catch commands"""

    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}
        self.bot.uncaught = {}

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if msg.guild is None:
            return

        spawnper = random.randrange(1, 30)

        if spawnper == 3:
            pRange = random.randrange(1, 898)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://pokeapi.co/api/v2/pokemon-species/{pRange}") as req:
                    rarC = await req.json()
            pLegC = rarC["is_legendary"]
            pMytC = rarC["is_mythical"]
            lc = [1, 5]
            mc = [1, 7]
            if pLegC == "true":
                lc = random.choice(lc)
                if lc != 3:
                    return
            if pMytC == "true":
                mc = random.choice(mc)
                if mc != 2:
                    return
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
            self.bot.uncaught[f"{msg.channel.id}"] = f"{pName.lower()}"

            if fledP is not None:
                fledStr = f"A wild {fledP} fled! A new wild pokemon has appeared!"

            em = discord.Embed(title = f"{fledStr}", description = f"Type `/catch <pokemon>` to catch it!")
            em.set_image(url = "attachment://pokemon.png")
            await msg.channel.send(file = img, embed = em)

    @slash_command()
    async def catch(self, ctx, pokemon: str):
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(' ', '-')
        author_id = ctx.author.id

        try:
            tbc = self.bot.uncaught[f"{ctx.channel.id}"]
        except:
            await ctx.respond("There are no wild pokemon! Please note that wild pokemon are reset on bot restart!")
            return

        if pokemon != tbc:
            await ctx.respond("That's the wrong pokemon!")
            return


        checkdata = await self.bot.db["pokedata"].find_one({"_id": ctx.author.id})

        if not checkdata:
            return await ctx.respond("You haven't started your journey yet! Please do `/start` to start your journey!")

        if len(checkdata) == 21:
            if ctx.author.id not in self.bot.owner_ids:
                return await ctx.respond("You can catch only 20 pokemon! Please release a pokemon to catch another one!")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}") as req:
                statReq = await req.json()
        nick = ""
        count = 1
        lvl = random.randrange(5, 21)
        try:
            stats = statReq["stats"]
        except:
            return await ctx.respond(f"Pokemon called {pokemon} was not found!")
        hp_stat = int(stats[0]["base_stat"])
        atk_stat = int(stats[1]["base_stat"])
        df_stat = int(stats[2]["base_stat"])
        spd_stat = int(stats[5]["base_stat"])

        with open("counter.json", "r") as g:
            pcounter = json.load(g)

        count = count + int(pcounter["pokecounter"])
        pcounter["pokecounter"] = count
        pid = len(checkdata) - 1

        with open("counter.json", "w") as g:
            json.dump(pcounter, g, indent = 4)

        statD = {"name": pokemon, "pNum": count, "lvl": lvl, "hp": hp_stat, "nick": nick, "atk": atk_stat, "df": df_stat, "spd": spd_stat}
        await self.bot.pokedata.update_by_id({"_id": ctx.author.id, f"p{count}": {"stats": statD}})
        bal = await self.bot.db["economy"].find_one({"_id": ctx.author.id})
        if bal is None:
            await self.bot.economy.insert({"_id": ctx.author.id, "balance": {"coins": 130, "shards": 0}})
        if bal:
            old_coins = bal["balance"]["coins"]
            old_shards = bal["balance"]["shards"]
            new_coins = int(old_coins) + 15
            _id = bal["_id"]
            balance = {"balance": {"coins": new_coins, "shards": old_shards}}
            await self.bot.db["economy"].update_one({"_id": _id}, {"$set": balance})
        tbc = tbc.replace("-", " ")
        await ctx.respond(f"Congratulations {ctx.author.mention}! You caught a level **{lvl}** {tbc.capitalize()}!\nAdded 15 coins to your balance!")
        self.bot.uncaught.pop(f"{ctx.channel.id}")

    @slash_command(name = "hint")
    async def _hint(self, ctx):
        """Get a hint of the pokemon that spawned!"""
        cooldown_check = None
        try:
            cooldown_check = self.cooldowns[ctx.channel.id]
        except:
            pass
        if cooldown_check is not None:
            return await ctx.respond("You are on a cooldown!")
        try:
            pokemonname = self.bot.uncaught[f"{ctx.channel.id}"]
        except:
            return await ctx.respond("There are no wild pokemon!")
        hint = ""
        for letter in pokemonname:
            if random.randint(0, 3) == 1:
                hint += letter
            else:
                hint += "_"
        await ctx.respond(f"The spawned pokemon is **`{hint}`**")
        self.cooldowns[ctx.channel.id] = 7
        await asyncio.sleep(7)
        try:
            del self.cooldowns[ctx.channel.id]
        except:
            pass

def setup(bot):
    bot.add_cog(Catch(bot))
