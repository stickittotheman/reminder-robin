import random
from typing import List

import discord
from discord import Guild
from more_itertools import first_true

import role
from member import Member


def find_guild_in(guild_name, guilds: List[Guild]) -> Guild:
    return first_true(guilds, None, lambda guild: guild.name == guild_name)


def find_channel_id_in(channel_name, guilds: List[Guild]):
    for guild in guilds:
        for channel in guild.channels:
            if channel.name == channel_name:
                channel_id = channel.id
                # print(channel.name + ' - ' + str(channel_id))
                return channel_id


def get_guild_members_as_string_from(guild):
    return '\n - '.join([member.name for member in guild.members])


def print_members(user_name, guild):
    print(
        f'{user_name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = get_guild_members_as_string_from(guild)

    print(f'Guild Members:\n - {members}')


def choose_member_from(members: List[Member]):
    return random.choice(members)


def find_role(role_name, roles: List[discord.Role]) -> discord.Role:
    return first_true(roles, None, lambda a_role: a_role.name == role_name)

