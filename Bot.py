import asyncio
import os
import sys

import discord
from discord.ext import commands

tokenFile = open("./", "r")
TOKEN = tokenFile.readline()
tokenFile.close()

INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=1030956690968944751&permissions=8&scope=bot'

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


def author_is_me(ctx):
    return ctx.author.id == 303222966580412416


@bot.command()
@commands.check(author_is_me)
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")


@bot.command()
@commands.check(author_is_me)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.command()
@commands.check(author_is_me)
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")


@bot.command()
@commands.check(author_is_me)
async def unMute(ctx, member: discord.Member):
    await member.edit(mute=False)


@bot.command()
@commands.check(author_is_me)
async def timeOut(ctx, member: discord.Member):
    await member.edit(mute=True)
    await asyncio.sleep(120)
    await member.edit(mute=False)


@bot.command()
@commands.check(author_is_me)
async def bgon(ctx):
    await ctx.send("Cya neeerds, im out")
    await bot.change_presence(status=discord.Status.offline, activity=None)
    await bot.close()
    await sys.exit()


async def loadCogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(filename, "loaded")


async def main():
    bot.remove_command("help")
    await loadCogs()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
