import json
import os
from typing import Union

import discord
from discord.ext.commands import *


class Help(Cog, name="Help"):
    def __init__(self, bot):
        """Cog containing commands under the Help category."""
        self.bot = bot
    
    def get_prefix(self, ctx: Context):
        """Gets the Bot prefix from a file according to the guild the Bot is in."""
        if not os.path.exists("./src/data/prefixes.json"):   
                with open("./src/data/prefixes.json", "w") as f:
                    json.dump({"0": "c!", f"{ctx.guild.id}": "c!"}, f, indent = 4)
        with open("./src/data/prefixes.json", "r") as f:
            prefixes = json.load(f)
        return prefixes[str(ctx.guild.id)]
    
    @command(name="help", description="Shows help information!", aliases=["invite", "cmds", "commands"])
    @cooldown(rate=1, per=0.5)
    async def help(self, ctx: Context, args: Union[str, None]):
        """Shows help information."""
        em = discord.Embed()
        em.set_thumbnail(url="https://media.discordapp.net/attachments/872133289375318016/874950183824273418/PikaPi.png?width=50&height=50")
        if isinstance(args, str):
            commands = self.bot.commands
            for command in commands:
                if args in command.qualified_name:
                    em.title = command.qualified_name
                    em.description = f"`{command.description}`"
                    em.add_field(name="Usage:", value=command.usage)
                    em.add_field(name="Cooldown:", value=command.is_on_cooldown(ctx))
                    em.add_field(name="Cog:", value=command.cog_name)
                    em.add_field(name="Aliases:", value=command.aliases)
        else:
            for cog in self.bot.cogs.values():
                temp = ""
                for command in cog.get_commands():
                    temp += f"`{command}` "
                em.title = f"Help Menu [prefix: `{self.get_prefix(ctx)}`]"
                em.description = "This is PikaPi's Help Section! Feel free to read about the commands PikaPi has!"
                em.add_field(name=f":white_circle:  {cog.qualified_name} [{len(Cog.get_commands(cog))}]", value=temp, inline=False)
        em.add_field(name=":small_red_triangle_down:", value="[GitHub](https://github.com/ThePikaPi/PikaPi/) | [PikaPi Discord Server](https://top.gg/servers/871048037768790016) | [Invite PikaPi to your server!](https://discord.com/oauth2/authorize?client_id=871051341248737290&scope=bot&permissions=8)", inline=False)
        await ctx.send(embed=em)
            


def setup(bot):
    bot.add_cog(Help(bot))
