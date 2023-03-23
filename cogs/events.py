import discord
from discord.ext import commands

class eventcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is online")
        activity = discord.Activity(type=discord.ActivityType.listening, name=".help")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found, try .help")


async def setup(bot):
    await bot.add_cog(eventcog(bot))
    