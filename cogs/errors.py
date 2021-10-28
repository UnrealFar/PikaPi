from discord.ext import commands
from discord.commands import commands as cmds
import discord

class Errors(commands.Cog):
    """Handles errors while executing commands!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("⌛")
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do dat!")
            ctx.command.reset_cooldown(ctx)
            return
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have permission to do dat!")
            ctx.command.reset_cooldown(ctx)
            return
        if isinstance(error, commands.NotOwner):
            await ctx.send("This is an owner only command!")
            ctx.command.reset_cooldown(ctx)
            return
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            await ctx.send(error)
            ctx.command.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, cmds.CommandOnCooldown):
            await ctx.respond("You are on a cooldown!")
            return
        if isinstance(error, cmds.MissingPermissions):
            await ctx.respond("You don't have permission to do dat!")
            return
        if isinstance(error, cmds.BotMissingPermissions):
            await ctx.respond("I don't have permission to do dat!")
            return
        if isinstance(error, cmds.NotOwner):
            await ctx.respond("This is an owner only command!")
            return
        if isinstance(error, cmds.CommandNotFound):
            return
        else:
            await ctx.respond(error)

def setup(bot):
    bot.add_cog(Errors(bot))
