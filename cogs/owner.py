from discord.ext import commands
import discord
import json
import asyncio
import os
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

    @commands.command()
    @commands.is_owner()
    async def reloadall(self, ctx):
        async with ctx.typing():
            for ext in os.listdir("./cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.reload_extension(f"cogs.{ext[:-3]}")
                        await ctx.send(f"Realoaded {ext[:-3]}!")
                        await asyncio.sleep(1)
                    except Exception as e:
                        await ctx.send(e)
                        return
            await ctx.send("Done reloading all cogs :)")

def setup(bot):
    bot.add_cog(Owner(bot))
