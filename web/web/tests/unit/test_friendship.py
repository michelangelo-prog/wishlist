# web/tests/unit/test_friendships.py
from web.domain.models.friendships import Friendship

from unittest import TestCase


class FriendshipTest(TestCase):
    def test_create_friendship(self):
        status = 1
        friendship = Friendship(status=status)

        assert status == friendship.status
