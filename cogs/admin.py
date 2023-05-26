import asyncio
import colorsys
import json
import os
import datetime
import textwrap
import time
import traceback
from contextlib import redirect_stdout
from io import BytesIO, StringIO
from typing import Union
import mystbin

import discord
import psutil
from discord.ext import commands
from PIL import Image

import db

Blacklistable = Union[discord.Guild, discord.User, discord.Member]


class Admin(commands.Cog):
    """Bot owner stuff."""

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self._last_result = None
        self.bin_client = mystbin.Client()

    async def send_or_paste(self, ctx, output):
        if len(output) > 1980:
            output = self.cleanup_code(output)
            paste = await self.bin_client.create_paste(filename="PIKAPI_PY_BOT_OUTPUT.py", content=output)
            await ctx.send(str(paste))
        else:
            await ctx.send(output)
        

    def cleanup_code(self, content: str) -> str:
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])

        # remove `foo`
        return content.strip("` \n")

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.config.OWNER_IDS


    @commands.command(aliases=["bl"])
    async def blacklist(self, ctx, thing: Blacklistable):
        self.bot.blacklist.append(thing.id)
        await ctx.tick()

    @commands.command(aliases=["ubl"])
    async def unblacklist(self, ctx, thing: Blacklistable):
        self.bot.blacklist.remove(thing.id)
        await ctx.tick()

    @commands.command(hidden=True, name="eval")
    async def _eval(self, ctx: commands.Context, *, body: str):
        """Evaluates a code"""

        body = self.cleanup_code(body)
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
            "db": db,
            "config": self.bot.config,
        }

        env.update(globals())
        stdout = StringIO()

        to_compile = f'async def _eval_command_exec_func_():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await self.send_or_paste(ctx, f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["_eval_command_exec_func_"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await self.send_or_paste(ctx, f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            token = self.bot.config.TOKEN
            value = str(stdout.getvalue())
            if ret is None:
                if value:
                    value = value.replace(token, "[token omitted]")
                    await self.send_or_paste(ctx, f"\n{value}\n")
            else:
                ret = str(ret).replace(token, "[token omitted]")
                self._last_result = ret
                await self.send_or_paste(ctx, f"\n{value}{ret}\n")
            try:
                await ctx.tick()
            except Exception:
                pass

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx) -> None:
        """Leaves the current guild."""
        assert ctx.guild is not None
        await ctx.guild.leave()

    @commands.command()
    async def load(self, ctx, *, module: str) -> None:
        """Loads a module."""
        module = f"cogs.{module}"

        try:
            await self.bot.load_extension(module)
        except commands.ExtensionError as err:
            await ctx.send(f"{err.__class__.__name__}: {err}")
        else:
            await ctx.tick()

    @commands.command()
    async def unload(self, ctx, *, module: str) -> None:
        """Unloads a module."""
        module = f"cogs.{module}"

        try:
            await self.bot.unload_extension(module)
        except commands.ExtensionError as err:
            await ctx.send(f"{err.__class__.__name__}: {err}")
            await ctx.tick(False)
        else:
            await ctx.tick()

    @commands.command(name="reload")
    async def _reload(self, ctx, *, module: str) -> None:
        """Reloads a module."""
        module = f"cogs.{module}"

        try:
            await self.bot.reload_extension(module)
            await ctx.tick()
        except commands.ExtensionNotLoaded:
            await self.bot.load_extension(module)
            await ctx.tick()
        except commands.ExtensionError as err:
            await ctx.send(f"{err.__class__.__name__}: {err}")
            await ctx.tick(False)
            return

    @commands.command()
    async def suspend(self, ctx, user: discord.User, *, reason=None):
        account = await db.Account.filter(id=user.id).first()
        if account:
            account.suspended = True
            account.suspension_reason = reason
            account.suspended_untl = discord.utils.utcnow() + datetime.timedelta(days=1)
        await ctx.tick()

    @commands.command()
    async def unsuspend(self, ctx, user: discord.User):
        account = await db.Account.filter(id=user.id).first()
        if account:
            account.suspended = False
            account.suspension_reason = None
            account.suspended_untl = discord.utils.min
        await ctx.tick()

    @commands.command(hidden=True)
    # Credit: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/stats.py#L716-L798
    async def health(self, ctx: commands.Context):
        HEALTHY = discord.Colour(value=0x43B581)
        UNHEALTHY = discord.Colour(value=0xF04947)
        WARNING = discord.Colour(value=0xF09E47)
        total_warnings = 0
        description = [f"Socket Events Received: {len(self.bot.received)}"]

        embed = discord.Embed(title="Bot Health Report", colour=HEALTHY)

        all_tasks = asyncio.all_tasks(loop=self.bot.loop)
        event_tasks = [t for t in all_tasks if "discord.py" in t.get_name() and not t.done()]
        if len(event_tasks) > 2:  # Usually it has 2 message event tasks not done
            total_warnings += 1
            embed.color = WARNING

        cogs_directory = os.path.dirname(__file__)
        tasks_directory = os.path.join("discord", "ext", "tasks", "__init__.py")
        inner_tasks = [t for t in all_tasks if cogs_directory in repr(t) or tasks_directory in repr(t)]

        bad_inner_tasks = ", ".join(hex(id(t)) for t in inner_tasks if t.done() and t._exception)
        total_warnings += bool(bad_inner_tasks)
        embed.add_field(name="Inner Tasks", value=f'Total: {len(inner_tasks)}\nFailed: {bad_inner_tasks or "None"}')
        embed.add_field(name="Events Waiting", value=f"Total: {len(event_tasks)}", inline=False)

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(name="Process", value=f"{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU", inline=False)

        global_rate_limit = not self.bot.http._global_over.is_set()
        description.append(f"Global Rate Limit: {global_rate_limit}")

        if global_rate_limit or total_warnings >= 9:
            embed.colour = UNHEALTHY

        embed.set_footer(text=f"{total_warnings} warning(s)")
        embed.description = "\n".join(description)
        await ctx.send(embed=embed)

    @commands.command(name="resetcolourcache", aliases=["rcc"])
    async def reset_colour_cache(self, ctx: commands.Context):
        with open("colour_cache.json", "w") as f:
            f.truncate(0)
            f.write("{}")

        iterations: int = len(await db.Species.all())
        embed = discord.Embed(
            title="Resetting Colour Cache",
            description=f"Iterations: `{iterations}`\nMin. Estimated Time: `{round(2.5 * iterations)}s`\nMax. Estimated Time: `{round(3 * iterations)}s`",
            color=discord.Color.blurple(),
        )
        await ctx.reply(embed=embed)

        start_time = time.time()

        id = 1
        cache = json.load(open("colour_cache.json", "r"))

        async def get_average_colour(url) -> tuple[int, int, int]:
            global cache
            async with self.bot.session.get(url) as resp:
                read_data = await resp.read()
                image = Image.open(BytesIO(read_data))

            width, height = image.size
            pixel_count = width * height
            rgb = [0, 0, 0]

            for y in range(height):
                for x in range(width):
                    r, g, b, a = image.getpixel((x, y))
                    rgb[0] += r
                    rgb[1] += g
                    rgb[2] += b

            saturation_multiplyer = 1.5

            avg_colour = tuple(sum_value // pixel_count for sum_value in rgb)
            hls = colorsys.rgb_to_hls(*avg_colour)
            rgb = colorsys.hls_to_rgb(hls[0], saturation_multiplyer * hls[1], hls[2])
            colour = tuple(255 if v > 255 else int(v) for v in rgb)
            return colour

        colour_cache = []

        while True:
            pokemon = await db.Species.filter(id=id).first()
            if not pokemon:
                embed = discord.Embed(
                    title="Completed Colour Caching",
                    description=f"Now caching `{id}` colours.",
                    color=discord.Color.green(),
                )
                await ctx.reply(embed=embed)
                break

            colour = await get_average_colour(pokemon.image_url)
            colour_cache.append((str(pokemon.id), colour))
            print(f"[COLOUR CACHE] Completed iteration #{id} - {pokemon.name_en}")

            id += 1

        for id_, colour in colour_cache:
            cache[str(id_)] = colour

        with open("colour_cache.json", "w") as f:
            json.dump(cache, f)

        embed = discord.Embed(
            title="Colour Caching Successful",
            description=f"Total Time Taken: `{round((time.time() - start_time) // 60)} minutes`",
            color=discord.Color.blurple(),
        )
        return await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
