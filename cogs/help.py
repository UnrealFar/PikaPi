import discord
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup

help = SlashCommandGroup("help", "The help command")

class Help(commands.Cog, name="Help command"):
    """Category that holds the help command!"""

    def __init__(self, bot):
        self.bot = bot

    @help.command(name = "all")
    async def _general_help(self, ctx):
        helpEm = discord.Embed(
            title = "PikaPi's Help Menu",
            description = f"""
            Do `/help command <command>` to get more info about a command!
            Do `/help category <category>` to get more info about a category!
            """,
            colour = 0x9CCFFF
        )
        helpEm.set_thumbnail(url = bot.user.display_avatar.url)
        helpEm.set_footer(icon_url = ctx.author.display_avatar.url, text = f"Requested by {ctx.author}")

        for cogname in self.bot.cogs:
            cog = self.bot.get_cog(cogname)
            cmds = ""
            for cmd in cog.commands:
                cmds += f"`{cmd.name}` "
            helpEm.add_field(
                name = cogname.capitalize(),
                value = f"""
                *{cog.description}*
                {cmds}
                """
            )
        
        await ctx.respond(embed = helpEm)

    @help.command(name = "command")
    async def _command_help(self, ctx, command: str):
        helpEm = discord.Embed(
            title = "PikaPi's Help Menu",
            description = f"""
            Do `/help command <command>` to get more info about a command!
            Do `/help category <category>` to get more info about a category!
            """,
            colour = 0x9CCFFF
        )
        helpEm.set_thumbnail(url = bot.user.display_avatar.url)
        helpEm.set_footer(icon_url = ctx.author.display_avatar.url, text = f"Requested by {ctx.author}")

        try:
            cmd = bot.get_command(name = f"{command}")
        except:
            await ctx.respond(f"Sorry! That command wasn't found! Please do /help <cogname> to view the list of available commands each cog has!")
            return
        helpEm.add_field(name = f"Command: {cmd.name}", value = f"**Usage:** `/{cmd.name} {cmd.signature}`")
        await ctx.respond(embed = helpEm)

    @help.command(name = "category")
    async def _cog_help(self, ctx, category):
            try:
                cogname = category.lower()
                cogname = cogname.capitalize()
                cog = bot.get_cog(name = f"{cogname}")
                commands = cog.get_commands()
            except:
                return await ctx.respond(f"Cog called {cogname} was not found! Please do /help to view the list of available cogs!")
            for cmd in commands:
                helpEm.add_field(name = f"{cmd.name}", value = f"**Usage:** `/{cmd.name} {cmd.signature}`")
            await ctx.respond(embed = helpEm)

def setup(bot):
    bot.add_cog(Help(bot))
    bot.add_application_command(help)