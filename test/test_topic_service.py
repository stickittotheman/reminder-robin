import unittest
from unittest import TestCase

from assertpy import assert_that
from discord.ext import commands

from bot_config import BotConfig
from model.topic import Topic
from topic_service import TopicService

test_config = BotConfig("discord token", "guild name", "bot name", "started at", "heroku key")

bot = commands.Bot(command_prefix='!')
topic_service = TopicService()


class TestTopicService(TestCase):
    def test_get_topic_by_display_id(self):
        topic_service.clear()
        topic_service.add("t1")
        topics = topic_service.add("t2")

        topic1 = topics[0]
        topic1.display_id = 1

        topic2 = topics[1]
        topic2.display_id = 2

        next_topic = topic_service.get_next_topic(topic1)

        assert_that(next_topic.title).is_equal_to("t2")
        assert_that(next_topic.display_id).is_equal_to(2)

    def test_build_formatted_list_of_topics(self):
        expectedTopic = Topic("expected", "", "", "")

        topic_service.add(expectedTopic.title)

        topics = topic_service.all()

        assert_that(topics).contains(expectedTopic)


if __name__ == '__main__':
    unittest.main()
