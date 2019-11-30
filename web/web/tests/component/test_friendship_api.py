import unittest

from web.tests.component.mixins import BaseTestCase, UserMixin, FriendshipMixin
from web.tests.factories import UserFactory


class TestFriendshipBlueprint(UserMixin, FriendshipMixin, BaseTestCase):
    def test_user_can_send_invitation_to_another_user(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__then_second_user_has_invitation_from_first_user()

    def __given_three_registered_users(self):
        self.user_data = [UserFactory.build() for i in range(3)]
        self.headers = []

        for data in self.user_data:
            self.send_register_user(json=data)
            login_response = self.send_login_user(json=data)
            token = login_response.json["token"]
            header = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
            self.headers.append(header)

    def __when_first_user_send_invitation_to_second_user(self):
        json = {"username": self.user_data[1]["username"]}
        self.send_invitation_to_user(headers=self.headers[0], json=json)

    def __then_second_user_has_invitation_from_first_user(self):
        response = self.get_invitations_from_users(headers=self.headers[1])
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json)
        self.assertEqual(self.user_data[0]["username"], response.json["users"][0])


if __name__ == "__main__":
    unittest.main()
