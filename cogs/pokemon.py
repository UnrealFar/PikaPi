import colorsys
import json
from io import BytesIO
from urllib.parse import quote_plus
from urllib.request import urlopen

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from PIL import Image

import constants
import db
import pokeflags


class Pokemon(commands.Cog):
    def __init__(self, bot: commands.Bot, /) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name = "pokedex")
    async def pokedex(self, interaction: discord.Interaction, name: str | None = None, id: int | None = None):
        if not name and not id:
            return await interaction.response.send_message("You need to specify the pokemon's name or ID!", ephemeral=True)

        await interaction.response.defer()
        pokemon: db.Species | None = None

        if name:
            name = name.lower().strip()
            if name.startswith('shiny'):
                name = name[6:]
                name = name.strip().title()
                is_sh = True
            else: is_sh = False
            pokemon = (
                await db.Species.filter(name_en=name).first()
                or await db.Species.filter(name_ja=name).first()
                or await db.Species.filter(name_jar=name).first()
                or await db.Species.filter(name_jat=name).first()
                or await db.Species.filter(name_de=name).first()
                or await db.Species.filter(name_fr=name).first()
            )
        elif id:
            pokemon = await db.Species.filter(id=id).first()

        if not pokemon:
            embed = discord.Embed(
                title = f"Could not find pokemon by {'name' if name else 'ID'}: `{name or id}`", color = discord.Color.red()
            )
            return await interaction.followup.send(embed = embed, ephemeral = True)

        async def _create_embed(pokemon: db.Species) -> discord.Embed:
    
            cache = self.bot.colour_cache
    
            if str(pokemon.id) not in cache:
                image = Image.open(BytesIO(urlopen( pokemon.shiny_image_url if is_sh else pokemon.image_url).read()))
                width, height = image.size
                pixel_count = width * height
                rgb = [0, 0, 0]
    
                for y in range(height):
                    for x in range(width):
                        r, g, b, a = image.getpixel((x, y))
                        rgb[0] += r
                        rgb[1] += g
                        rgb[2] += b
    
                saturation_multiplier = 1.5
    
                avg_colour = tuple(sum_value // pixel_count for sum_value in rgb)
                hls = colorsys.rgb_to_hls(*avg_colour)
                rgb = colorsys.hls_to_rgb(hls[0], saturation_multiplier * hls[1], hls[2])
                colour = tuple(255 if v > 255 else int(v) for v in rgb)
                with open("colour_cache.json", "w") as f:
                    cache[pokemon.id] = colour
                    json.dump(cache, f)
            else:
                colour = cache[str(pokemon.id)]
    
            embed = discord.Embed(
                title=f"{'Shiny ' if is_sh else ''}{pokemon.name_en.title()} - #{pokemon.dex}",
                url=f"https://pokemon.fandom.com/wiki/{quote_plus(pokemon.name_en)}",
                color=discord.Color.from_rgb(*colour),
            )
            embed.set_image(url=pokemon.shiny_image_url if is_sh else  pokemon.image_url)
    
            pokeflag_types = pokeflags.Types(int(pokemon.types))._get_enabled_flags()
            embed.add_field(
                name=f"Types ({len(pokeflag_types)})",
                value="\n".join([f"{db.get_type_emoji(type_)}  `{type_.title()}`" for type_ in pokeflag_types]),
            )
    
            embed.add_field(name="Rarity", value=f'`{("normal", "legendary", "mythical")[pokemon.rarity].title()}`')
            embed.add_field(name="Capture Rate", value=f"`{round((pokemon.capture_rate * 100) / 256, 2)}%`")
    
            embed.add_field(
                name="Appearance",
                value=f"**Height:** `{pokemon.height / 10}m`\n" + f"**Weight:** `{pokemon.weight / 10}kg`",
            )
    
            embed.add_field(name="Region", value=f"`{constants.REGIONS[pokemon.region].capitalize()}`")
    
            embed.add_field(name="Catchable", value="`Yes`" if pokemon.capture_rate else "`No`")
            discord.Embed(
                title=f"{pokemon.name_en.title()} - #{pokemon.dex}",
                url=f"https://pokemon.fandom.com/wiki/{quote_plus(pokemon.name_en)}",
                color=discord.Color.from_rgb(*colour),
            )
            embed.add_field(
                name="Statistics",
                value=f"**HP:** `{pokemon.hp}`\n"
                + f"**Attack:** `{pokemon.attack}`\n"
                + f"**Defense:** `{pokemon.defense}`\n"
                + f"**Sp. Atk:** `{'N/A' if not pokemon.special_attack else pokemon.special_attack}`\n"
                + f"**Sp. Def:** `{'N/A' if not pokemon.special_defense else pokemon.special_defense}`\n"
                + f"**Speed:** `{pokemon.speed}`\n",
            )
    
            newline = "\n"
            embed.add_field(
                name="Names",
                value=newline.join([f"{v} `{getattr(pokemon, k)}`" for k, v in constants.LANGUAGE_EMOJIS.items()]),
            )

            return embed

        async def _edit_embed(interaction: discord.Interaction, message: discord.Message, id_: int) -> None:
            await interaction.response.defer()
            
            pokemon = await db.Species.filter(id = id_).first()
            embed = await _create_embed(pokemon)

            view = View(timeout = None)
            previous_button = Button(label = "◀️", disabled = pokemon.id == 1)
            next_button = Button(label = "▶️", disabled = pokemon.id == len(await db.Species.all()))
    
            view.add_item(previous_button)
            view.add_item(next_button)
            
            embed = await _create_embed(pokemon)
            result = await message.edit(embed = embed, view = view)
            
            previous_button.callback = lambda i: _edit_embed(i, result, pokemon.id - 1)
            next_button.callback = lambda i: _edit_embed(i, result, pokemon.id + 1)

        view = View(timeout = None)
        previous_button = Button(label = "◀️", disabled = pokemon.id == 1)
        next_button = Button(label = "▶️", disabled = pokemon.id == len(await db.Species.all()))

        view.add_item(previous_button)
        view.add_item(next_button)
        
        embed = await _create_embed(pokemon)
        result = await interaction.followup.send(embed = embed, view = view)
        
        previous_button.callback = lambda i: _edit_embed(i, result, pokemon.id - 1)
        next_button.callback = lambda i: _edit_embed(i, result, pokemon.id + 1)

async def setup(bot):
    await bot.add_cog(Pokemon(bot))
