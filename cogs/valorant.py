import asyncio
import json
import random

import discord
import requests
from discord.ext import commands

tokenFile = open("./token2", "r")
TENORKEY = tokenFile.readline()
tokenFile.close()

CKEY = 'discordbot'
EMOJIS = ["💛", "🟡", "🟨", "🌻", "☀"]


class valorantCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {"players": 5, "chanses": 2,
                         "reaction_procentage": 60, "time_out": 120}
        self.players = []

    @commands.command()
    async def start(self, ctx):
        self.players.append([ctx.author, 0])

        await ctx.message.delete()
        await ctx.send(f'@everyone {self.settings["players"]}-stack?')

        gif = gifRandomFrom("game-time")
        embed = gifEmbed(author=ctx.author, title="Gibb?", gif=gif)
        embed.description = "React to take a spot!"
        embed = await ctx.send(embed=embed)

        commandCog = self.bot.get_cog('valorantEvents')
        commandCog.gameTimeMsgId = embed.id
        await embed.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    async def reset(self, ctx):
        self.players.clear()
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    async def settings(self, ctx, *args: str):
        for a in args:
            k, v = a.split('=')
            if k in self.settings:
                self.settings[k] = int(v)
            else:
                await ctx.message.add_reaction("\N{THUMBS DOWN SIGN}")

        await ctx.send(self.settings)


class valorantEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gameTimeMsgId: int
        self.gameMsgId: int

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        commandCog = self.bot.get_cog('valorantCommands')
        settings = commandCog.settings
        players = commandCog.players
        message = reaction.message

        # Returns if the reaction was from the bot
        if member == self.bot.user:
            return

        elif message.id == self.gameTimeMsgId:

            # If the user reacts with some random emoji it gets deleted
            if reaction.emoji != "👍":
                await message.remove_reaction(reaction.emoji, member)
                return

            players.append([member, 0])
            if reaction.count == settings["players"]:

                # Ignores old players
                players = players[len(players)-settings["players"]:]

                # All players here, delete gameTimeMsg
                msg = await message.channel.fetch_message(message.id)
                await msg.delete()

                # Send gameMsg
                strMessage = createMessage(players)
                message = await message.channel.send(strMessage)
                self.gameMsgId = message.id

                # Reacts to msg so players can just click on the reaction to react themself
                for i in range(len(players)):
                    await message.add_reaction(EMOJIS[i])

        elif message.id == self.gameMsgId:

            # If the user reacts with some random emoji it gets deleted
            if reaction.emoji not in EMOJIS:
                await message.remove_reaction(reaction.emoji, member)
                return

            else:
                i = 0
                for reaction in message.reactions:

                    # If the amount of votes(reactions) fulfill the requierd procentage to give 'yellow card'. reactions / players >= reaction_procentage
                    if (reaction.count - 1) / settings["players"] * 100 >= settings["reaction_procentage"]:

                        # Players 'yellow card' increases with 1
                        players[i][1] += 1

                        # Check if the player should be dealt a 'red card' instead of yellow
                        if players[i][1] >= settings["chanses"]:  # Red card

                            gif = gifRandomFrom("silenced")
                            embed = gifEmbed(
                                author=players[i][0], title="Silence!", gif=gif)
                            embed = await message.channel.send(embed=embed)

                            # Player gets muted and unmuted after 'time_out' amount of seconds
                            await players[i][0].edit(mute=True)
                            await asyncio.sleep(settings["time_out"])
                            await players[i][0].edit(mute=False)

                            await embed.delete()

                            # Resets 'yellow cards'
                            players[i][1] = 0

                        else:                                   # Yellow card
                            gif = gifRandomFrom("warned")
                            embed = gifEmbed(
                                author=players[i][0], title="Warning!", gif=gif)
                            embed = await message.channel.send(embed=embed)

                            # Shows 'yellow card' gif for 5 seconds
                            await asyncio.sleep(5)
                            await embed.delete()

                        # Resets the reactions on that player
                        for player in players:
                            await message.remove_reaction(reaction.emoji, player[0])

                    i += 1


async def setup(bot):
    await bot.add_cog(valorantCommands(bot))
    await bot.add_cog(valorantEvents(bot))


def createMessage(players):
    """ Creates gameMsg content """
    msg = ["I am keeping track : )\n"]

    for p, e in zip(players, EMOJIS):   # Works like two for loops
        msg.append(f"{e} {p[0].mention}")

    strMessage = "".join(msg).replace('[', '').replace(']', '')
    return strMessage


def gifFrom(search, limit=50):
    """ Grabs gifs from tenor """
    r = requests.get(
        f"https://tenor.googleapis.com/v2/search?q={search}&key={TENORKEY}&client_key={CKEY}limit={limit}")
    gifs = json.loads(r.content)["results"]
    return gifs


def gifRandomFrom(search, limit=50):
    """ Random gif from search """
    gifs = gifFrom(search, limit)
    gif = random.choice(gifs)["media_formats"]["gif"]["url"]
    return gif


def gifEmbed(author, title, gif):
    """ Template for gif embed """
    embed = discord.Embed(colour=discord.Colour.from_rgb(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    embed.set_author(name=author)
    embed.title = title
    embed.set_image(url=gif)
    embed.set_footer(text="Via Tenor")
    return embed
