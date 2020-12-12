import discord

import member
from discord_utils import find_guild_in, find_channel_id_in, get_guild_members_as_string_from, choose_member_from, \
    find_role
from model.topic import Topic


class TopicService:
    def __init__(self):
        self.topics = []

    def add(self, topic_title):
        self.topics.append(Topic("", topic_title))
        return self.topics

    def all(self):
        return self.topics

    def find(self, title):
        found_topics = [t for t in self.topics if t.title == title]
        return found_topics[0]