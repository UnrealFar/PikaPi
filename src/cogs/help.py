import discord
from bot import get_prefix
from discord.ext.commands import *


class Help(Cog, name="Help"):
    def __init__(self, bot):
        """Cog containing commands under the Help category."""
        self.bot = bot
    
    @command(name="help", description="Shows help information!", aliases=["invite", "cmds", "commands"])
    @cooldown(rate=1, per=2)
    async def help(self, ctx: Context, command: str = ""):
        """Shows help information."""
        # TODO Fix `help <alias>` not displaying help info properly.
        command = str(command).lower()
        em = discord.Embed()
        if command == "":
            em.title = "Help Command"
            [em.add_field(name=f"» {cog.qualified_name}", value=str([f"`{command}` " for command in cog.get_commands()]).replace("[", "").replace("'", "").replace(",", "").replace("]", ""), inline=False) for cog in self.bot.cogs.values()]
        else:
            for cmd in self.bot.commands:
                if command == cmd.qualified_name:
                    em.title = cmd.qualified_name
                    em.description = f"`{cmd.description}`"
                    em.add_field(name="Usage:", value=str(str(["`None`" if cmd.signature == "" else f"`{cmd.signature}`"]).replace("[", "").replace("'", "").replace(",", "").replace("]", "")))
                    em.add_field(name="Cooldown:", value=str(cmd.is_on_cooldown(ctx)))
                    em.add_field(name="Cog:", value=str(cmd.cog_name))
                    em.add_field(name="Aliases:", value=str(["`None`" if not cmd.aliases else [f"`{alias}` " for alias in cmd.aliases]]).replace("[", "").replace("'", "").replace(",", "").replace("]", ""))
                    break
                elif cmd.aliases != "" and command in cmd.aliases:
                    em.title = command
                    em.description = f"`{cmd.description}`"
                    em.add_field(name="Usage:", value=str(["`None`" if cmd.signature == "" else f"`{cmd.signature}`"]).replace("[", "").replace("'", "").replace(",", "").replace("]", ""))
                    em.add_field(name="Cooldown:", value=str(cmd.is_on_cooldown(ctx)))
                    em.add_field(name="Cog:", value=str(cmd.cog_name))
                    em.add_field(name="Base Command:", value=str(f"`{cmd.qualified_name}`"))
                    break
        em.colour = discord.Colour.random()
        em.set_thumbnail(url="https://media.discordapp.net/attachments/872133289375318016/874950183824273418/PikaPi.png?width=50&height=50")
        em.set_footer(text=f"For more information, type {await get_prefix(self.bot, ctx)}help <command> or {await get_prefix(self.bot, ctx)}help <alias>!")
        em.add_field(name="Links", value="[GitHub](https://github.com/ThePikaPi/PikaPi/) | [PikaPi Discord Server](https://dsc.gg/thepikapi) | [Invite PikaPi to your server!](https://dsc.gg/pikapi)", inline=False)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))
