from discord.ext import commands
import discord
import googletrans

class Utilities(commands.Cog):
    def __init__(self, bot):
        #Another useless typehint.
        self.bot: commands.Bot = bot
        self.translator: googletrans.Translator = googletrans.Translator()

    @discord.commands.slash_command(
        name = "translate",
        guild_ids = (873181946786762804,)
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

def setup(bot):
    bot.add_cog(Utilities(bot))
