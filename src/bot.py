# bot.py
from datetime import datetime

from discord.ext import commands

import discord_utils
from bot_config import initialize_bot_config
from bot_service import BotService


bot = commands.Bot(command_prefix='!')
bot_config = initialize_bot_config(datetime.now())
bot_service = BotService(bot, bot_config)


@bot.event
async def on_ready():
    await greet()


async def greet():
    bot_channel_id = bot_service.find_channel_id(bot_config.bot_channel_name)
    bot_channel = await bot.fetch_channel(bot_channel_id)
    await bot_channel.send("chirp chirp!")


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
    await ctx.send(bot_config.bot_name)


@bot.command()
async def env(ctx):
    await ctx.send(discord_utils.safe_env_vars())


@bot.command()
async def health(ctx):
    await ctx.send(discord_utils.health(bot_config))

if __name__ == '__main__':
    discord_utils.output(f"Starting bot: {bot_config.bot_name}")
    discord_utils.output(f"Entering guild: {bot_config.guild_name}")
    STARTED_AT = datetime.now()

    bot.run(bot_config.token)

