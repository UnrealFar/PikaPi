from discord.ext import commands
import discord

class Errors(commands.Cog):
    """The description for Errors goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: commands.CommandError):
        embed = discord.Embed()
        if isinstance(error, commands.NSFWChannelRequired):    
            await ctx.send("This command can only be excecuted in an NSFW channel!")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("⌛")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do dat!")
        if isinstance(error, commands.BotMissingPermissions):
            embed.description("I don't have permission to do dat!")
            await ctx.send(embed = embed)
        if isinstance(error, commands.NotOwner):
            embed.description("This is an owner only command!")
            await ctx.send(embed = embed)
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            await ctx.send(error)

def setup(bot):
    bot.add_cog(Errors(bot))
