from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if getattr(ctx, "local_handled", None):
            return

        ignored = (commands.CommandOnCooldown, commands.NotOwner)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("No command like that exists")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"Command `{ctx.command}` has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f"The command `{ctx.command}` cannot be used in Private Messages.")

        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f"Bad argument: {error}")

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(str(error))

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(
                f'I cannot complete this command, you are missing the following permission{"" if len(error.missing_permissions) == 1 else "s"}: {", ".join(error.missing_permissions)}'
            )

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(
                f'I cannot complete this command, I am missing the following permission{"" if len(error.missing_permissions) == 1 else "s"}: {", ".join(error.missing_permissions)}'
            )

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send("Sorry, you cannot use this command")
        else:
            pass  # TODO: Add this shit


async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))
