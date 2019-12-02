import unittest

from web.tests.component.mixins import BaseTestCase, UserMixin, FriendshipMixin
from web.tests.factories import UserFactory


class TestFriendshipBlueprint(UserMixin, FriendshipMixin, BaseTestCase):
    def test_user_can_send_invitation_to_another_user(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__then_user_get_201_when_invitation_has_been_successfully_send()

    def test_user_receive_invitaion_from_another_user_when_user_sent_invitation(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_check_invitations_from_another_users()
        self.__then_invition_from_first_user_is_waiting()

    def test_second_user_can_accept_invitation_from_first_user(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__then_second_user_get_201_when_invitation_has_been_successfully_accepted()

    # def test_second_user_can_decline_invitation_from_first_user(self):
    #     self.__given_three_registered_users()
    #     self.__when_first_user_send_invitation_to_second_user()
    #     self.__when_second_user_decline_invitation_from_user()
    #     self.__then_user_get_204_when_invitation_has_been_successfully_declined()

    def test_when_second_user_accept_invitation_and_have_friend(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__when_second_user_check_if_have_any_friends()
        self.__then_second_user_have_friend()

    def test_user_accept_invitation_from_first_user_and_first_user_have_friend(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__when_first_user_check_if_have_any_friends()
        self.__then_first_user_have_friend()

    # def test_when_user_delete_friend_from_friendships(self):
    #     self.__given_three_registered_users()
    #     self.__when_first_user_send_invitation_to_second_user()
    #     self.__when_second_user_accept_invitation_from_first_user()

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
        self.response = self.sent_invitation_to_user(headers=self.headers[0], json=json)

    def __when_second_user_check_invitations_from_another_users(self):
        self.response = self.get_invitations_from_users(headers=self.headers[1])

    def __when_second_user_accept_invitation_from_first_user(self):
        json = {"username": self.user_data[0]["username"]}
        self.response = self.sent_accept_invitation(headers=self.headers[1], json=json)

    def __when_second_user_check_if_have_any_friends(self):
        self.response = self.get_list_of_friends(headers=self.headers[1])

    def __when_first_user_check_if_have_any_friends(self):
        self.response = self.get_list_of_friends(headers=self.headers[0])

    def __then_user_get_201_when_invitation_has_been_successfully_send(self):
        self.assertEqual(201, self.response.status_code)

    def __then_invition_from_first_user_is_waiting(self):
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, len(self.response.json["users"]))
        self.assertEqual(self.user_data[0]["username"], self.response.json["users"][0])

    def __then_second_user_get_201_when_invitation_has_been_successfully_accepted(self):
        self.assertEqual(201, self.response.status_code)

    def __then_second_user_have_friend(self):
        response_json = self.response.json
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, len(response_json["users"]))
        self.assertEqual(self.user_data[0]["username"], response_json["users"][0])

    def __then_first_user_have_friend(self):
        response_json = self.response.json
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, len(response_json["users"]))
        self.assertEqual(self.user_data[1]["username"], response_json["users"][0])


if __name__ == "__main__":
    unittest.main()
