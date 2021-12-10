from nextcord.ext import commands


class ErrorHandler(commands.Cog):
    """A cog for global error handling."""

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: commands.CommandError):
        """A global error handler cog."""

        if isinstance(error, commands.CommandNotFound):
            return  # Return because we don't want to show an error for every command not found
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
             
        elif isinstance(error, commands.MissingPermissions):
            perms=[p for p in error.missing_permissions]
            p=",".join(perms)
            message = f"You must have **{p}** permissions to run this command!"
        elif isinstance(error, commands.UserInputError):
            message = "Something about your input was wrong, please check your input and try again!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"A required arguement that is missing!"    
        else:
            raise error
             
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)
def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))