import unittest
from unittest import TestCase

from assertpy import assert_that
from discord.ext import commands

from bot_config import BotConfig
from model.topic import Topic
from progress_bar_wrapper import ProgressBar, getting_str_out
from topic_service import TopicService
from widgets import Bar, ETA, ReverseBar


class TestProgressBar(TestCase):
    def test_getting_str_out(self):
        getting_str_out()


if __name__ == '__main__':
    unittest.main()
