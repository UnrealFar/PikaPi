from discord.ext import commands
import discord

from typing import List

invite = discord.ui.Button(
    label = "Invite",
    style = discord.ButtonStyle.link,
    url = "https://bit.ly/PikaPiBot"
)

class HelpView(discord.ui.View):
    def __init__(self, help_cog, embed):
        super.__init__(self, timeout = 60)
        self.help_cog: HelpCog = help_cog
        self.embed: discord.Embed = embed
        self.all_pages = (0,)
        self.add_item(invite)

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.name = "Help"
        self.bot: commands.Bot = bot

    @discord.commands.slash_command(
        name = "help",
        description = "PikaPi's help command!",
        #guild_ids = (873181946786762804,)
    )
    async def help(
        self,
        ctx,
        command: discord.Option(
            str,
            required = False
        )
    ):
        if command:
            found = False
            for cmd in await self.get_all_commands():
                if cmd.name == command:
                    found = True
                    break
            if not found:
                await ctx.respond(
                    embed = discord.Embed(
                        description = f"Couldn't find a command called {command}"
                    )
                )
            else:
                await ctx.respond(
                    embed = discord.Embed(
                        title = "Command Help",
                        description = f"""
                        **Name:** `{cmd.name}`
                        **Description:** {cmd.description}
                        **Usage:** `{self.get_command_usage(cmd)}`
                        """
                    )
                )

    def get_command_usage(
        self,
        command: discord.ApplicationCommand
    ):
        od = command._get_signature_parameters()
        it = [i for i in od if (i != "self") and ("ctx" not in i)]
        return f"/{command.name} {' '.join((f'<{e}>' for e in it))}"

    async def get_all_cogs(self) -> List[commands.Cog]:
        return [v for k, v in self.bot.cogs]

    async def get_all_commands(self) -> List[discord.ApplicationCommand]:
        return list(self.bot.walk_application_commands())
    

def setup(bot):
    bot.add_cog(HelpCog(bot))
