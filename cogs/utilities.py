from discord.ext import commands
import discord, inspect, os
import googletrans
from typing import Union

from bot import PikaPi
from helper import ApplicationContext

class Utilities(commands.Cog):
    def __init__(self, bot):

        self.bot: PikaPi = bot
        self.translator: googletrans.Translator = googletrans.Translator()

    @discord.commands.slash_command(
        name = "translate",
    )
    async def translate(
        self,
        ctx,
        message: str
    ):
        try:
            translated = await self.bot.loop.run_in_executor(None, self.translator.translate, str(message))
        except Exception as e:
            return await ctx.respond(
                f"Uh oh! An error was encountered: {e.__class__.__name__}: {e}"
            )

        em = discord.Embed(title = "Translated!", colour = discord.Colour.red())
        src = googletrans.LANGUAGES.get(translated.src, "(auto-detected)").title()
        dest = googletrans.LANGUAGES.get(translated.dest, "unknown").title()
        em.add_field(name = f"From {src}", value = translated.origin, inline = False)
        em.add_field(name = f"To {dest}", value = translated.text, inline = False)
        await ctx.respond(embed = em)

    @discord.commands.slash_command(
        name = "source",
        guild_ids = (873181946786762804,)
    )
    async def source(
        self,
        ctx: ApplicationContext,
        command: discord.Option(
            str,
            "The command who's source code is to be found.",
            required = False
        )
    ):
        """Get the source code for the bot or a specific command!"""
        emoji = '<:githubwhite:804344724621230091>'
        s_url = "https://github.com/TheFarGG/PikaPi"
        branch = "master"
        if not command:
            embed = discord.Embed(
                title = f"{emoji} Source {emoji}"
            )
            embed.url = s_url
            return await ctx.respond(embed = embed)

        command = command.replace(".", " ")
        obj: Union[discord.ApplicationCommand, commands.Command] = None
        obj = self.bot.get_application_command(command)
        if not obj:
            obj = self.bot.get_command(command)

        if not obj:
            return await ctx.respond(f"Couldn't find a command called {command}")

        cb = getattr(obj, "__callback__", getattr(obj, "callback"))
        src = cb.__code__
        m = cb.__module__
        fn = src.co_filename

        ls, fln = inspect.getsourcelines(src)
        if m.startswith("discord"):
            location = m.replace(".", "/") + ".py"
            s_url = "https://github.com/Pycord-Developmet/Pycord"
        elif m.startswith("jishaku"):
            location = m.replace(".", "/") + ".py"
            s_url = "https://github.com/Sengolda/Jishkucord"
        else:
            location = os.path.relpath(fn).replace("\\", "/")

        dest = f"{s_url}/blob/{branch}/{location}#L{fln}-L{fln + len(ls) - 1}"
        embed = discord.Embed(
            title = f"Source code for {command}",
            description = f"Click [here]({dest}) for the source code!"
        )
        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(Utilities(bot))
