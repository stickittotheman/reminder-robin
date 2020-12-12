import discord

import member
from discord_utils import find_guild_in, find_channel_id_in, get_guild_members_as_string_from, choose_member_from, \
    find_role


class BotService:
    def __init__(self, bot, bot_config):
        self.bot = bot
        self.bot_config = bot_config
        self.topics = []

    def find_guild(self):
        guilds = self.bot.guilds
        return find_guild_in(self.bot_config.guild_name, guilds)

    def find_channel_id(self, channel_name):
        guilds = self.bot.guilds
        return find_channel_id_in(channel_name, guilds)

    def get_guild_members(self):
        guild = self.find_guild()
        return get_guild_members_as_string_from(guild)

    def choose_member(self) -> member.Member:
        members = self.find_guild().members
        return choose_member_from(members)

    def choose_member_from(self, role_name) -> member.Member:
        roles = self.find_guild().roles
        role = find_role(role_name, roles)
        members = role.members
        return choose_member_from(members)

    def handle_choose_member_from(self) -> str:
        choosen_member: discord.Member = self.choose_member_from(self.bot_config.sre_role_name)

        return f'I choose you pickachu: <@{choosen_member.id}>'
