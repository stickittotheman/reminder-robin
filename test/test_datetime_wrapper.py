import unittest
from datetime import timedelta, datetime
from unittest import TestCase

from assertpy import assert_that

from datetime_wrapper import format_timedelta


class TestDatetimeWrapper(TestCase):
    def test_format_timedelta(self):
        future = datetime.now() + timedelta(seconds=int(90))
        delta = future - datetime.now()
        result = format_timedelta(delta)
        assert_that(result).is_equal_to("00:01:30")


if __name__ == '__main__':
    unittest.main()
