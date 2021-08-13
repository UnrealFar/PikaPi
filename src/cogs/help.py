import discord
from discord.ext import commands
from discord.ext.commands import *


class Help(commands.Cog, name="Help"):
    def __init__(self, bot):
        """Cog containing commands under the Help category."""
        self.bot = bot
    
    @commands.command(name="help", description="Shows help information!", aliases=["invite", "cmds", "commands"])
    @commands.cooldown(rate=1, per=0.5)
    async def help(self, ctx: Context):
        """Shows help information."""
        em = discord.Embed()
        em.title = "Help Menu"
        em.description = "This is PikaPi's Help Section! Feel free to read about the commands PikaPi has!"
        em.set_thumbnail(url="https://media.discordapp.net/attachments/872133289375318016/874950183824273418/PikaPi.png?width=50&height=50")
        em.colour = discord.Colour.orange()
        for cog in self.bot.cogs.values():
            temp = ""
            for command in cog.get_commands():
                temp += f"`{command}` "
            em.add_field(name=f":white_circle:  {cog.qualified_name} [{len(Cog.get_commands(cog))}]", value=temp, inline=False)
        em.add_field(name=":small_red_triangle_down:", value="[GitHub](https://github.com/ThePikaPi/PikaPi/) | [PikaPi Discord Server](https://top.gg/servers/871048037768790016) | [Invite PikaPi to your server!](https://discord.com/oauth2/authorize?client_id=871051341248737290&scope=bot&permissions=8)", inline=False)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))
