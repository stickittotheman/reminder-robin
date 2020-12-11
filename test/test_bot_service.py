import inspect
import unittest
from datetime import time, datetime
from unittest import TestCase

from assertpy import assert_that
from discord.ext import commands
from timebetween import is_time_between

from bot_config import BotConfig, initialize_bot_config
from bot_service import BotService
from discord_utils import choose_member_from, find_role, sanitize_env_vars, SAFE_KEYS, current_configuration, \
    SAFE_CONFIG_VARS, sanitize_config, health
from member import Member
from model.topic import Topic
from role import Role

test_config = BotConfig("discord token", "guild name", "bot name", "started at", "heroku key")

bot = commands.Bot(command_prefix='!')
service = BotService(bot, test_config)


class TestBotService(TestCase):
    def test_add_topic(self):
        service.add_topic("expected")

        topics = service.all_topics()

        assert_that(topics[0].title).is_equal_to("expected")

    def test_build_formatted_list_of_topics(self):
        expectedTopic = Topic("", "expected")

        service.add_topic(expectedTopic.title)

        topics = service.all_topics()

        assert_that(topics).contains(expectedTopic)


if __name__ == '__main__':
    unittest.main()
