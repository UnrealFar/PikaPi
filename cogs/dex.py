from discord.ext import commands
import discord

from bot import PikaPi
from helper import ApplicationContext
from models import Pokemon

JA_FLAG = "🇯🇵"
EN_FLAG = "🇬🇧"
DE_FLAG = "🇩🇪"
FR_FLAG = "🇫🇷"

class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot: PikaPi = bot

    @discord.commands.slash_command(
        name = "pokedex",
    )
    async def pokedex(
        self,
        ctx: ApplicationContext,
        pokemon: discord.Option(
            str,
            "The name of the Pokemon to search for!"
        )
    ):
        """Search the Pokedex for a praticular Pokemon!"""
        pokemon = pokemon.lower()
        if pokemon.startswith("shiny "):
            pokemon = pokemon[6:]
            sh = True
        else:
            sh = False
        poke = await self.bot.get_pokemon(
            {
                "$or": [
                    {"slug": pokemon},
                    {"names.en": pokemon},
                    {"names.ja": pokemon},
                    {"names.fr": pokemon},
                    {"names.de": pokemon},
                    {"names.jar": pokemon}
                ]
            }
        )
        if not poke:
            return await ctx.respond(f"A Pokemon called {pokemon} was not found!")
        poke.shiny = sh
        title = poke.names.get("en", pokemon).title()
        if poke.shiny:
            title = f"✨ {title}"

        em = discord.Embed(
            title = title,
            colour = discord.Colour.gold()
        )
        em.add_field(
            name = "Names",
            value = self.get_names(poke)
        )
        stats = self.get_stats(poke)
        em.add_field(
            name = "Base Stats",
            value = stats
        )
        ap = poke.appearance
        em.add_field(
            name = "Appearance",
            value = f"Height: {ap.get('height')}\nWeight: {ap.get('weight')}"
        )
        em.add_field(
            name = "Region",
            value = poke.region.title()
        )
        em.add_field(
            name = "Types",
            value = "\n".join((p.title() for p in poke.types))
        )
        em.add_field(
            name = "Pokedex ID",
            value = poke.dex
        )
        if getattr(poke, "event", False):
            em.add_field(
                name = "Event",
                value= "Yes"
            )


        img = await poke.get_image()
        em.set_image(url = "attachment://pokemon.png")
        await ctx.respond(embed = em, file = img)

    def get_stats(self, poke: Pokemon) -> str:
        s = poke.base_stats
        return f"""
        **HP**: {s.get('hp')}
        **Attack**: {s.get('atk')}
        **Defence**: {s.get('df')}
        **Sp. Attack**: {s.get('satk')}
        **Sp. Defence**: {s.get('sdf')}
        """

    def get_names(self, poke: Pokemon) -> str:
        ns = poke.names
        ret = str()
        ret += f"{EN_FLAG} {ns.get('en')}\n"
        if ns.get("ja"):
            ret += f"{JA_FLAG} {ns.get('ja')}\n"
        else:
            ret += f"{JA_FLAG} {ns.get('en')}\n"
        if ns.get("jar"):
            ret += f"{JA_FLAG} {ns.get('jar')}\n"
        else:
            ret += f"{JA_FLAG} {ns.get('ja') if ns.get('ja') else ns.get('en')}\n"
        if ns.get("de"):
            ret += f"{DE_FLAG} {ns.get('de')}\n"
        else:
            ret += f"{DE_FLAG} {ns.get('en')}\n"
        if ns.get("fr"):
            ret += f"{FR_FLAG} {ns.get('fr')}\n"
        else:
            ret += f"{FR_FLAG} {ns.get('en')}\n"
        return ret.title()

def setup(bot):
    bot.add_cog(Pokedex(bot))
