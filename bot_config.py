import os

from dotenv import load_dotenv

SRE_CHANNEL_NAME = 'site-reliability-stuff'
BOT_CHANNEL_NAME = 'bot_testing'
SRE_ROLE_NAME = 'Site Reliability'


class BotConfig:
    def __init__(self, token, guild_name, bot_name, started_at, sre_role_name=SRE_ROLE_NAME,
                 sre_channel_name=SRE_CHANNEL_NAME, bot_channel_name=BOT_CHANNEL_NAME):
        self.token = token
        self.guild_name = guild_name
        self.bot_name = bot_name
        self.started_at = started_at
        self.sre_role_name = sre_role_name
        self.sre_channel_name = sre_channel_name
        self.bot_channel_name = bot_channel_name


def initialize_bot_config(started_at) -> BotConfig:
    load_dotenv()

    token = os.getenv('DISCORD_TOKEN')
    guild_name = os.getenv('DISCORD_GUILD')
    bot_name = os.getenv('BOT_NAME')

    bot_config = BotConfig(token, guild_name, bot_name, started_at)
    return bot_config


