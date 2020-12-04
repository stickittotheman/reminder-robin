import inspect
import unittest
from datetime import time
from unittest import TestCase

from assertpy import assert_that
from timebetween import is_time_between

from bot_config import BotConfig
from discord_utils import choose_member_from, find_role, sanitize_env_vars, SAFE_KEYS, current_configuration, \
    SAFE_CONFIG_VARS, sanitize_config, health
from member import Member
from role import Role

test_config = BotConfig("discord token", "guild name", "bot name", "started at", "heroku key")


class TestDiscordUtils(TestCase):
    def test_time(self):
        start = time(7, 0)
        end = time(19, 0)

        inside_of_interval = time(11, 0)
        outside_of_interval = time(20, 0)
        assert_that(is_time_between(inside_of_interval, start, end)).is_true()
        assert_that(is_time_between(outside_of_interval, start, end)).is_false()

    def test_choose_member(self):
        m1 = Member("foo")
        m2 = Member("Bar")
        m3 = Member("Baz")

        members = [m1, m2, m3]
        member = choose_member_from(members)
        assert_that([member.display_name for member in members]).contains(member.display_name)

    def test_find_role(self):
        r1 = Role("foo")
        r2 = Role("Bar")
        r3 = Role("Baz")

        roles = [r1, r2, r3]
        found_role = find_role(r2.name, roles)
        assert_that([role.name for role in roles]).contains(found_role.name)

    def test_sanitize_env_vars(self):
        fake_env_vars = {'DISCORD_TOKEN': 'some token', 'BOT_NAME': 'awesome bot', 'DISCORD_GUILD': 'The Guild'}

        result = sanitize_env_vars(fake_env_vars, SAFE_KEYS)

        assert_that(result.keys()).contains('DISCORD_GUILD')
        assert_that(result.keys()).contains('BOT_NAME')
        assert_that(result.keys()).does_not_contain('DISCORD_TOKEN')

    def test_sanitize_config(self):
        result = sanitize_config(test_config, SAFE_CONFIG_VARS)

        assert_that(result.keys()).contains('bot_name')
        assert_that(result.keys()).does_not_contain('discord_token')
        assert_that(result.keys()).does_not_contain('heroku_api_key')

    def test_get_current_configuration(self):
        result = current_configuration(test_config)
        expected = """{'bot_channel_name': 'bot_testing',
    'bot_name': 'bot name',
    'guild_name': 'guild name',
    'sre_channel_name': 'site-reliability-stuff',
    'sre_role_name': 'Site Reliability',
    'started_at': 'started at'}"""
        assert_that(inspect.cleandoc(result)).is_equal_to(inspect.cleandoc(expected))

    def test_health(self):
        expected = """Bot name: bot name
Started at: started at
Bot Env: {}
Bot Config: {'bot_channel_name': 'bot_testing',
 'bot_name': 'bot name',
 'guild_name': 'guild name',
 'sre_channel_name': 'site-reliability-stuff',
 'sre_role_name': 'Site Reliability',
 'started_at': 'started at'}"""
        assert_that(health(test_config)).is_equal_to(expected)


if __name__ == '__main__':
    unittest.main()
