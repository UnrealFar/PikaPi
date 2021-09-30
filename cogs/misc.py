from discord.ext import commands
import discord
import bot

class Misc(commands.Cog):
    """Miscellaneous commands that do not fit anywhere else"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if await self.bot.command_usage.find(ctx.command.qualified_name) is None:
            await self.bot.command_usage.upsert({"_id": ctx.command.qualified_name, "usage_count": 1})

        else:
            await self.bot.command_usage.increment(ctx.command.qualified_name, "usage_count", 1)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def usage(self, ctx):
        """Shows usage stats for PikaPi's commands!"""
        data = await self.bot.command_usage.get_all()
        command_map = {item["_id"]: item["usage_count"] for item in data}

        total_commands_run = sum(command_map.values())
        sorted_list = sorted(command_map.items(), key = lambda x: x[1], reverse = True)

        pages = []
        cmd_per_page = 10

        for i in range(0, len(sorted_list), cmd_per_page):
            message = ""
            next_commands = sorted_list[i: i + cmd_per_page]

            for item in next_commands:
                use_percent = item[1] / total_commands_run
                message += f"***{item[0]}***: Total uses: ***`{item[1]}`*** **`{use_percent}`**\n"

            pages.append(message)

        await bot.Pag(title = "Command usage statistics", colour = discord.Colour.dark_blue(), entries = pages, length = 1).start(ctx)

def setup(bot):
    bot.add_cog(Misc(bot))
