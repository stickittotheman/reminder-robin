from typing import List, Optional

import discord

import member
from discord_utils import find_guild_in, find_channel_id_in, get_guild_members_as_string_from, choose_member_from, \
    find_role
from emoji_wrapper import get_count_for_emoji, BALLOT_BOX
from model.topic import Topic


def get_vote_count(msg):
    return get_count_for_emoji(msg, BALLOT_BOX)


class TopicService:
    def __init__(self):
        self.ctx = None
        self.topics: List[Topic] = []

    def add(self, topic_title):
        self.topics.append(Topic(topic_title, "", "", "", ""))
        return self.topics

    def all(self):
        return self.topics

    def clear(self):
        return self.topics.clear()

    def find(self, title):
        found_topics = [t for t in self.topics if t.title == title]
        return found_topics[0]

    def get_topic_by_display_id(self, display_id):
        found_topics = [t for t in self.topics if t.display_id == int(display_id)]
        return found_topics[0]

    def get_next_topic(self, topic) -> Optional[Topic]:
        next_topic_id = int(topic.display_id) + 1
        if len(self.topics) <= next_topic_id:
            return self.get_topic_by_display_id()
        return None
