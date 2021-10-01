from discord.ext import commands
import discord

class Config(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "prefix",
        aliases = ["setprefix", "serverprefix", "guildprefix"]
        )
    @commands.has_permissions(administrator = True)
    async def setprefix(self, ctx, newprefix: str = "p!"):
        """Change the bot's prefix for the guild!"""
        await self.bot.prefixes.upsert({"_id": ctx.guild.id, "prefix": newprefix})
        await ctx.send(f"PikaPi's prefix for this server has been successfully set to **`{newprefix}`**")

def setup(bot):
    bot.add_cog(Config(bot))
