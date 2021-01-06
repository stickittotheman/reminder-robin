import os
from datetime import time

from dotenv import load_dotenv

SRE_CHANNEL_NAME = 'site-reliability-stuff'
BOT_CHANNEL_NAME = 'bot-cave'
LEAN_COFFEE_TEXT_CHANNEL = 'lean-coffee'
LEAN_COFFEE_VOICE_CHANNEL = 'LEAN Coffee'
LEAN_COFFEE_VOTE_TIME = 15

SRE_ROLE_NAME = 'Site Reliability'
START_TIME = time(7, 0)
END_TIME = time(19, 0)


class BotConfig:
    def __init__(self, discord_token, guild_name, bot_name, started_at, heroku_api_key, sre_role_name=SRE_ROLE_NAME,
                 sre_channel_name=SRE_CHANNEL_NAME, bot_channel_name=BOT_CHANNEL_NAME, start_time=START_TIME,
                 end_time=END_TIME, lean_coffee_text=LEAN_COFFEE_TEXT_CHANNEL,
                 lean_coffee_voice=LEAN_COFFEE_VOICE_CHANNEL, lean_coffee_continue_vote_time=LEAN_COFFEE_VOTE_TIME):
        self.discord_token = discord_token
        self.guild_name = guild_name
        self.bot_name = bot_name
        self.started_at = started_at
        self.heroku_api_key = heroku_api_key
        self.sre_role_name = sre_role_name
        self.sre_channel_name = sre_channel_name
        self.bot_channel_name = bot_channel_name
        self.start_time = start_time
        self.end_time = end_time
        self.lean_coffee_text = lean_coffee_text
        self.lean_coffee_voice = lean_coffee_voice
        self.lean_coffee_continue_vote_time = lean_coffee_continue_vote_time


def initialize_bot_config(started_at) -> BotConfig:
    load_dotenv()

    token = os.getenv('DISCORD_TOKEN')
    guild_name = os.getenv('DISCORD_GUILD')
    bot_name = os.getenv('BOT_NAME')
    heroku_api_key = os.getenv('HEROKU_API_KEY')

    bot_config = BotConfig(token, guild_name, bot_name, started_at, heroku_api_key)
    return bot_config
