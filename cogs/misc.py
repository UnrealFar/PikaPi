import time

import discord
from discord import app_commands
from discord.ext import commands

import constants
import db


class Misc(commands.Cog):
    """Misc Cog"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello")
    async def hello(self, i):
        await i.response.send_message("Hello I am bot made for pokemon by:\n\nfarrr#6470\nSengolda#7250\nMeerkat#1665")

    async def normal_cleanup_strat(self, i, search):
        count = 0
        async for m in i.channel.history(limit=search):
            if m.author.id == self.bot.user.id:
                try:
                  await m.delete()
                except discord.NotFound:
                    continue
                else:
                    count += 1

        return count

    async def owner_cleanup_strat(self, i, search):
        def check(m):
            return m.author.id == self.bot.user.id or m.content.startswith(
                "r."
            ) # only owner-only commands are not slash commands

        count = 0
        async for m in i.channel.history(limit=search):
            if check(m):
                try:
                  await m.delete()
                except discord.NotFound:
                    continue
                else:
                    count += 1

        return count

    @app_commands.command(name="cleanup")
    async def _cleanup(self, i, amount: int):
        """Cleans up after using bot's commands"""
        is_owner = i.user.id in self.bot.config.OWNER_IDS
        if is_owner:
            strat = self.owner_cleanup_strat
        else:
            strat = self.normal_cleanup_strat
        if i.channel.permissions_for(i.user).manage_messages:
            search = min(max(2, amount), 1000)
        if is_owner:
            search = amount
        else:
            search = min(max(2, amount), 25)
        result = await strat(i, search=search)
        await i.response.send_message(f"Deleted {result} {'messages' if result != 1 else 'message'}", ephemeral=True)

    @app_commands.describe(starter="The pokemon to start your journey with!")
    @app_commands.command(name="register")
    async def register(self, i: discord.Interaction, starter: constants.STARTERS):
        """Create a PikaPi account!"""

        acc = await db.Account.filter(id=i.user.id).first()

        if acc:
            return await i.response.send_message("You already have an account!")

        acc = await db.Account.create(id=i.user.id, balance=100, selected_id=1, created_at=discord.utils.utcnow())
        species = await db.Species.filter(id=int(starter.value)).first()
        poke = await species.catch(acc)
        await poke.save()
        await i.response.send_message("Welcome to the world of pokemon!")

    @app_commands.command()
    async def ping(self, i):
        """View the bot's ping"""
        async with i.channel.typing():
            pings = []
            number = 0

            await i.response.send_message("🏓 pong!")

            latency_ms = self.bot.latency * 1000
            pings.append(latency_ms)

            discord_start = time.monotonic()
            await self.bot.session.get("https://discord.com/api/v10")
            discord_end = time.monotonic()
            discord_ms = (discord_end - discord_start) * 1000
            pings.append(discord_ms)

            for ms in pings:
                number += ms
            average = number / len(pings)

        new_message = "**WebSocket:** {}ms\n**Discord API:** {}ms\n**Average**:   {}ms".format(
            round(latency_ms, 2), round(discord_ms, 2), round(average, 2)
        )
        await i.edit_original_response(content=new_message)

    @app_commands.command()
    async def invite(self, i):
        """Invite PikaPi to your server"""
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.external_emojis = True
        perms.send_messages = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        perms.add_reactions = True
        em = discord.Embed(color=discord.Color.orange())
        em.title = "Thanks for wanting to invite me, you can using this link"
        em.url = discord.utils.oauth_url(self.bot.application_id, permissions=perms)
        await i.response.send_message(embed=em)

    @app_commands.command()
    async def uptime(self, i):
        """Uptime of PikaPi"""
        delta = discord.utils.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await i.response.send_message(f"I've been alive for (my uptime): {days}d {hours}h {minutes}m {seconds}s")

    @commands.command(hidden=True)
    async def help(self, ctx):
        await ctx.send("This bot uses slash commands just type / and you can see everything the bot has")


async def setup(bot):
    await bot.add_cog(Misc(bot))
