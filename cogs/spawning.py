from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from bot import PikaPi

import asyncio
import io
import random

import discord
from discord import app_commands
from discord.ext import commands, tasks

import db


class SpawnCog(commands.Cog):
    bot: PikaPi

    def __init__(self, bot: PikaPi):
        self.bot = bot
        self.spawn_cooldown: List[int] = list()

    async def cog_load(self):
        self.incense_spawner.start()

    async def cog_unload(self):
        self.incense_spawner.cancel()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.guild is None:
            return
        await self.spawn(message.channel)

    @tasks.loop(seconds=30)
    async def incense_spawner(self) -> None:
        await self.spawn(
            self.bot.get_guild(self.bot.PIKAPI_GUILD_ID).get_channel(self.bot.PIKAPI_INCENSE_ID), True, True, "∞"
        )
        async for r in db.Incense.all():
            guild = self.bot.get_guild(r.guild_id)
            channel = None if guild is None else guild.get_channel_or_thread(r.channel_id)
            if channel:
                if r.remaining:
                    r.remaining -= 1
                    await r.save()
                    asyncio.create_task(self.spawn(channel, True, True, r.remaining))
                else:
                    await r.delete()

    @incense_spawner.before_loop
    async def before_incense_spawner(self):
        await self.bot.wait_until_ready()

    async def get_species(self, id=None, name=None) -> db.Species:
        if name:
            return await db.Species.get(name=name)
        elif id:
            return await db.Species.get(id=id)
        crs = self.bot.capture_rates
        cr = random.choices(crs, crs)[0]
        ret = await db.Species.filter(capture_rate=cr)
        return random.choice(ret)

    async def spawn(
        self, channel: discord.TextChannel, force=False, is_incense=False, incense_remaining=None, species=None
    ):
        if not force or not is_incense:
            g_id = channel.guild.id
            if g_id in self.spawn_cooldown:
                return
            self.spawn_cooldown.append(g_id)

            async def remove_cooldown():
                await asyncio.sleep(20)
                self.spawn_cooldown.remove(g_id)

            asyncio.create_task(remove_cooldown())
            if random.randint(0, 10):
                return
        poke = None
        poke = await self.get_species(name=species)
        if not poke:
            return False

        unc = await db.Uncaught.filter(channel_id=channel.id).first()
        try:
            d = unc.name_en
            t = f"The {d.title()} has fled! A new wild pokemon has appeared!"
        except AttributeError:
            t = "A wild pokemon has appeared!"
        sendEm = discord.Embed(
            title=t, description="Use `/catch <pokemon>` to catch it!", colour=discord.Colour.og_blurple()
        )
        sendEm.set_image(url="attachment://pokemon.png")
        if is_incense:
            sendEm.set_footer(text=f"Incense spawns remaining: {incense_remaining}")
        async with self.bot.session.get(poke.image_url) as imgdata:
            img_fp = io.BytesIO(await imgdata.content.read())
        file = discord.File(filename="pokemon.png", fp=img_fp)
        try:
            await channel.send(embed=sendEm, file=file)
        except Exception:
            return False
        if unc:
            unc.species_id = poke.id
        else:
            unc = db.Uncaught(species_id=poke.id, channel_id=channel.id)
        await unc.save()
        return True

    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(name="hint")
    async def hint_cmd(self, i: discord.Interaction) -> None:
        """Get a hint for the spawned wild pokemon!"""
        if not i.guild:
            return await i.response.send_message("This command can only be used in a guild!", ephemeral=True)

        poke = (await db.Uncaught.filter(channel_id=i.channel.id).first()).name_en

        if not poke:
            await i.response.send_message("There are no wild pokemon spawned in this channel!")
        inds = [i for i, s in enumerate(poke) if s.isalpha()]
        blanks = random.sample(inds, len(inds) // 2)
        hint = "".join("_" if i in blanks else x for i, x in enumerate(poke))
        await i.response.send_message("The wild pokemon is `" + hint + "`!")

    @app_commands.command(name="catch")
    async def catch_cmd(
        self,
        i: discord.Interaction,
        guess: str,
    ):
        """Catch the wild pokemon spawned in your channel!"""
        account = await db.Account.filter(id=i.user.id).first()
        if not account:
            await i.response.send_message("Please register using `/register` before using this command!")
        unc = await db.Uncaught.filter(channel_id=i.channel.id).first()
        if not unc:
            return await i.response.send_message("No wild pokemon to catch!", ephemeral=True)
        guess = guess.lower()
        species = await db.Species.filter(id=unc.species_id).first()
        if guess in (
            species.name_en.lower(),
            species.name_en.lower(),
            species.name_ja,
            species.name_jar.lower(),
            species.name_jat.lower(),
            species.name_fr.lower(),
            species.name_de.lower(),
        ):
            return await i.response.send_message("That is the wrong pokemon!", ephemeral=True)

        shiny_chance = 1 / 4096
        if account.shiny_hunt and account.shiny_hunt == species.id:
            shiny_chance * (1 + (account.shiny_streak**0.5) / 7)

        caught = await species.catch(account, shiny=shiny_chance > random.random())

        await i.response.send_message(
            f"Congratulations! You have caught a level {caught.level} {guess.title()}! Use `/view <latest:true>` to view it!"
        )


async def setup(bot):
    await bot.add_cog(SpawnCog(bot))
