# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot_service import BotService

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SRE_CHANNEL_NAME = 'site-reliability-stuff'
BOT_CHANNEL_NAME = 'bot_testing'
BOT_NAME = "coco local"
SRE_ROLE_NAME = "Site Reliability"
bot = commands.Bot(command_prefix='!')
bot_service = BotService(bot, GUILD, SRE_ROLE_NAME)


@bot.event
async def on_ready():
    await greet()


async def greet():
    bot_channel_id = bot_service.find_channel_id(BOT_CHANNEL_NAME)
    bot_channel = await bot.fetch_channel(bot_channel_id)
    await bot_channel.send("chirp chirp!")


# @bot.command()
# async def choose(ctx):
#     member: discord.Member = bot_service.choose_member()
#
#     response = f'I choose you pickachu: {member.display_name}'
#     await ctx.send(response)

@bot.command()
async def choose(ctx):
    response = bot_service.handle_choose_member_from()
    await ctx.send(response)


@bot.command()
async def robin_says(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def which(ctx):
    await ctx.send(BOT_NAME)

if __name__ == '__main__':
    print("starting bot")
    print(f"Entering guild: {GUILD}")
    bot.run(TOKEN)

