import discord
from discord.ext import commands
import random

class commandcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        embed.set_author(name="Commands")

        embed.add_field(name=".help", value="Shows this message", inline=False)
        embed.add_field(name=".vibecheck", value="Online/offline members", inline=False)
        embed.add_field(name=".clear", value="clears 3 msg:s change with amount, .clear amount", inline=False)
        embed.add_field(name=".start", value="Run before 5-stack : D", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def vibecheck(self, ctx):
        guild_id = ctx.guild.id
        server = self.bot.get_guild(guild_id)

        online = 0
        offline = 0

        for m in server.members:
            if str(m.raw_status) != "offline":
                online += 1
        offline = server.member_count - online

        await ctx.send(f"```Online: {online}\nOffline: {offline}```")

    @commands.command()
    async def clear(self, ctx, amount=3):
        amount += 1
        await ctx.channel.purge(limit=amount)


async def setup(bot):
    await bot.add_cog(commandcog(bot))