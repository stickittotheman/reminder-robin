import os
import pprint
import random
import sys
from typing import List

import discord
from discord import Guild
from more_itertools import first_true

from bot_config import BotConfig
from member import Member
import logging

logging.basicConfig(level=logging.INFO)

SAFE_KEYS = ['DISCORD_GUILD', 'BOT_NAME', 'HOSTNAME', 'DYNO']
SAFE_CONFIG_VARS = [
"guild_name",
"bot_name",
"started_at",
"sre_role_name",
"sre_channel_name",
"bot_channel_name",
]


def find_guild_in(guild_name, guilds: List[Guild]) -> Guild:
    return first_true(guilds, None, lambda guild: guild.name == guild_name)


def find_channel_id_in(channel_name, guilds: List[Guild]):
    for guild in guilds:
        for channel in guild.channels:
            if channel.name == channel_name:
                channel_id = channel.id
                return channel_id


def get_guild_members_as_string_from(guild):
    return '\n - '.join([member.name for member in guild.members])


def print_members(user_name, guild):
    output(
        f'{user_name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = get_guild_members_as_string_from(guild)

    output(f'Guild Members:\n - {members}')


def choose_member_from(members: List[Member]):
    return random.choice(members)


def find_role(role_name, roles: List[discord.Role]) -> discord.Role:
    return first_true(roles, None, lambda a_role: a_role.name == role_name)


def sanitize_env_vars(env_vars, safe_keys):
    filtered_env_vars = {key: value for (key, value) in env_vars.items() if key in safe_keys}
    return filtered_env_vars


def sanitize_config(bot_config, safe_config_vars):
    filtered_env_vars = {key: bot_config.__dict__[key] for key in safe_config_vars}
    return filtered_env_vars


def safe_env_vars():
    env_vars = sanitize_env_vars(os.environ, SAFE_KEYS)
    output(env_vars)
    return env_vars


def current_configuration(bot_config: BotConfig):
    safe_config_vars = sanitize_config(bot_config, SAFE_CONFIG_VARS)
    return pprint.pformat(safe_config_vars)


def health(bot_config: BotConfig):
    bot_name_str = f"Bot name: {bot_config.bot_name}"
    started_at_str = f"Started at: {bot_config.started_at}"
    env_vars = f"Bot Env: {sanitize_env_vars(os.environ, SAFE_KEYS)}"

    output(bot_name_str)
    output(started_at_str)
    output(env_vars)

    return f"{bot_name_str}\n{started_at_str}\n{env_vars}"


def output(msg):
    # print(msg)
    # sys.stdout.flush()
    logging.info(msg)
