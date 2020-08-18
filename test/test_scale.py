import unittest
from datetime import time
from unittest import TestCase

from assertpy import assert_that
from timebetween import is_time_between

from discord_utils import choose_member_from, find_role, sanitize_env_vars, SAFE_KEYS
from member import Member
from role import Role
from scale import desired_heroku_scale_for


class TestScale(TestCase):
    def test_scale(self):
        start = time(7, 0)
        end = time(19, 0)

        test_time = time(11, 0)

        assert_that(desired_heroku_scale_for(test_time, start, end)).is_equal_to(1)

    def test_time(self):
        start = time(7, 0)
        end = time(19, 0)

        inside_of_interval = time(11, 0)
        outside_of_interval = time(20, 0)
        assert_that(is_time_between(inside_of_interval, start, end)).is_true()
        assert_that(is_time_between(outside_of_interval, start, end)).is_false()


if __name__ == '__main__':
    unittest.main()
