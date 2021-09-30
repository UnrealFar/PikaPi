from discord.ext import commands
import discord
import json
import asyncio
import bot

class Owner(commands.Cog):
    """Commands for the owner!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        """Enables/Disables a command!"""
        command = self.bot.get_command(command)

        if command is None:
            return await ctx.send("I can't find a command with that name!")

        elif ctx.command == command:
            return await ctx.send("You cannot disable this command")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} **`{command.qualified_name}`**!")

def setup(bot):
    bot.add_cog(Owner(bot))
