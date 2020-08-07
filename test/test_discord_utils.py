import unittest
from unittest import TestCase

from assertpy import assert_that

from discord_utils import choose_member_from, find_role
from member import Member
from role import Role


class TestDiscordUtils(TestCase):
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


if __name__ == '__main__':
    unittest.main()
