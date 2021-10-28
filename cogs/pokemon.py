from discord.ext import commands
from discord.commands import slash_command
import discord
import requests
import jishaku
import json

class Pokedex(commands.Cog):
    """Pokedex Stuff"""

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name = "pokedex", aliases = ["d", "dex"])
    async def pokedex(self, ctx, pokemon):
        pokemon = pokemon.replace(" ", "-")
        resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        try:
            pname = resp.json()["name"].capitalize()
        except:
            await ctx.respond(f"Pokemon called **`{pokemon}`** doesn't exist!")
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
        rarC = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pID}")
        pLeg = rarC.json()["is_legendary"]
        pMyth = rarC.json()["is_mythical"]
        pheight = resp.json()["height"]
        pheight = float(pheight / 10)
        pweight = resp.json()["weight"]
        pweight = float(pweight / 10)
        dexEm = discord.Embed(title = f"#{pID} {pname}", colour = discord.Colour.dark_blue())
        if pLeg:
            dexEm.add_field(name = "Rarity", value = "Legendary")
        if pMyth:
            dexEm.add_field(name = "Rarity", value = "Mythical")
        dexEm.add_field(name = "Types", value = f"{ptype1}\n{ptype2}\n{ptype3}\n{ptype4}", inline = False)
        dexEm.add_field(name = "Appearance", value = f"**Height**: {pheight}m\n**Weight**: {pweight}kg", inline = False)
        dexEm.set_image(url = pImg)
        await ctx.respond(embed = dexEm)

    @slash_command(name = "pokemon",aliases = ["p"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pokemon(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        author_id = member.id

        acc_check = await self.bot.pokedata.get_all()
        data = None

        for account in acc_check:
            if account["_id"] == author_id:
                d = account
                data = []
                for p in d:
                    data.append(account[p])

        if data is None:
            return await ctx.respond("You haven't started your journey yet! Please do `/start` to start your journey!")

        pList = commands.Paginator(prefix = "", suffix = "", max_size = 350)
        counter = 0
        user_pokes = list(data)[1:]
        pokEm = discord.Embed(colour = discord.Colour.red())
        pokEm.set_thumbnail(url = member.display_avatar.url)

        for poke in user_pokes:
            counter += 1
            poke_id = counter
            poke_s = user_pokes[counter - 1]["stats"]
            poke_name = poke_s["name"]
            poke_nick = poke_s["nick"]
            poke_lvl = poke_s["lvl"]
            pList.add_line(f"`{poke_id}` - **{poke_name.capitalize()}** - {poke_nick} Lvl. {poke_lvl}\n")

        pokeEm = discord.Embed(title = f"{ctx.author}'s pokemon!", colour = discord.Colour.green())
        pokeEm.set_thumbnail(url = ctx.author.display_avatar.url)
        interface = jishaku.paginators.PaginatorEmbedInterface(ctx.bot, pList, owner = ctx.author, embed = pokeEm)
        await interface.send_to(ctx)

    @slash_command(name = "nickname", aliases = ["nick"])
    @commands.cooldown(1, 1, commands.BucketType.default)
    async def nickname(self, ctx, pokemon_id: int, newnick: str = None):
        """Give your pokemon a nickname!"""
        return await ctx.respond("Not ready for use!")
        with open("caught.json", "r") as f:
            data = json.load(f)

        if str(ctx.author.id) not in data:
            await ctx.send(f"You haven't started yet! Please use `/start` to start your journey with us!")
            return

        try:
            user_poke = data[str(ctx.author.id)][str(pokemon_id)]
            poke_name = user_poke["name"]
            poke_lvl = user_poke["lvl"]
        except:
            await ctx.send(f"Pokemon with ID {pokemon_id} wasn't found!")
            return

        if newnick is None:
            new_nick = ""
            resp = f"Your level {poke_lvl} **{poke_name}**'s nickname was reset!"

        else:
            new_nick = newnick
            resp = f"Your level {poke_lvl} **{poke_name}**'s nickname was changed to {newnick}"
        
        data[str(ctx.author.id)][str(pokemon_id)]["nick"] = new_nick
        
        with open("caught.json", "w") as f:
            json.dump(data, f, indent = 4)

        await ctx.respond(resp)

def setup(bot):
    bot.add_cog(Pokedex(bot))
