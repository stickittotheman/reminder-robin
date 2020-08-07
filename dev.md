Reminder Robin Dev Notes

Well testing async stuff is tricky...

Best guess at that path would be to try...

https://pypi.org/project/dpytest/

then the test might look something like...
which could then leverage the dpytest

```
import os
import unittest
from unittest import TestCase

import discord
from assertpy import assert_that
from dotenv import load_dotenv

from discord_wrapper import DiscordWrapper

load_dotenv('../src/.env')


class TestDiscordWrapper(TestCase):
    discord_wrapper = None
    client = None

    def setUp(self):
        token = os.getenv('DISCORD_TOKEN')
        guild = os.getenv('DISCORD_GUILD')

        self.client = discord.Client()
        # self.client.run(token)
        self.client.login(token)
        self.client.connect()

        self.discord_wrapper = DiscordWrapper(self.client, guild)

    def test_choose_member(self):
        member = self.discord_wrapper.choose_member()
        assert_that(member.name).is_equal_to('')

    def tearDown(self):
        self.client.logout()


if __name__ == '__main__':
    unittest.main()
```
