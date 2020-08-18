from dataclasses import dataclass

import discord


@dataclass
class Member:
    display_name: str

    @staticmethod
    def from_discord_member(discord_member: discord.Member):
        return Member(display_name=discord_member)

