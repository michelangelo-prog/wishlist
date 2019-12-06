import unittest

import pytest

from web.tests.component.mixins import BaseTestCase, UserMixin, FriendshipMixin
from web.tests.factories import UserFactory


class TestFriendshipBlueprint(UserMixin, FriendshipMixin, BaseTestCase):
    def test_user_can_send_invitation_to_another_user(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__then_user_get_201_when_invitation_has_been_successfully_send()

    @pytest.mark.skip(reason="TO DO")
    def test_user_receive_invitaion_from_another_user_when_user_sent_invitation(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_check_invitations_from_another_users()
        self.__then_invition_from_first_user_is_waiting()

    @pytest.mark.skip(reason="TO DO")
    def test_second_user_can_accept_invitation_from_first_user(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__then_second_user_get_204_when_invitation_has_been_successfully_accepted()

    @pytest.mark.skip(reason="TO DO")
    def test_second_user_can_decline_invitation_from_first_user(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_decline_invitation_from_first_user()
        self.__then_user_get_204_when_invitation_has_been_successfully_declined()

    @pytest.mark.skip(reason="TO DO")
    def test_when_second_user_accept_invitation_and_have_friend(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__when_second_user_check_if_have_any_friends()
        self.__then_second_user_have_friend()

    @pytest.mark.skip(reason="TO DO")
    def test_second_user_accept_invitation_from_first_user_and_first_user_have_friend(
        self,
    ):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__when_first_user_check_if_have_any_friends()
        self.__then_first_user_have_friend()

    @pytest.mark.skip(reason="TO DO")
    def test_when_user_delete_friend_from_friendships(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__when_second_user_delete_first_user_from_friendship()
        self.__then_user_get_204_when_friendship_has_been_deleted()

    @pytest.mark.skip(reason="TO DO")
    def test_when_user_delete_friend_and_have_only_one_friend(self):
        self.__given_three_registered_users()
        self.__when_first_user_send_invitation_to_second_user()
        self.__when_second_user_accept_invitation_from_first_user()
        self.__when_second_user_send_invitation_to_third_user()
        self.__when_third_user_accept_invitation_from_second_user()
        self.__when_second_user_delete_first_user_from_friendship()
        self.__when_second_user_check_if_have_any_friends()
        self.__then_second_user_have_third_user_in_friendships()

    def register_user(self, user_data):
        response = self.send_register_user(json=user_data)
        self.assertEqual(201, response.status_code)
        return response

    def login_user(self, user_data):
        response = self.send_login_user(json=user_data)
        self.assertEqual(201, response.status_code)
        return response

    def prepare_user_header(self, token):
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

    def __given_three_registered_users(self):
        self.user_data = [UserFactory.build() for i in range(3)]
        self.headers = []

        for user_data in self.user_data:
            self.register_user(user_data)
            login_response = self.login_user(user_data)
            user_header = self.prepare_user_header(login_response.json["token"])
            self.headers.append(user_header)

    def __when_first_user_send_invitation_to_second_user(self):
        json = {"username": self.user_data[1]["username"]}
        self.response = self.send_invitation_to_user(headers=self.headers[0], json=json)

    def __when_second_user_send_invitation_to_third_user(self):
        json = {"username": self.user_data[2]["username"]}
        self.response = self.send_invitation_to_user(headers=self.headers[1], json=json)

    def __when_second_user_check_invitations_from_another_users(self):
        self.response = self.get_invitations_from_users(headers=self.headers[1])

    def __when_second_user_accept_invitation_from_first_user(self):
        json = {"username": self.user_data[0]["username"]}
        self.response = self.send_accept_invitation(headers=self.headers[1], json=json)

    def __when_third_user_accept_invitation_from_second_user(self):
        json = {"username": self.user_data[1]["username"]}
        self.response = self.send_accept_invitation(headers=self.headers[2], json=json)

    def __when_second_user_check_if_have_any_friends(self):
        self.response = self.get_list_of_friends(headers=self.headers[1])

    def __when_first_user_check_if_have_any_friends(self):
        self.response = self.get_list_of_friends(headers=self.headers[0])

    def __when_second_user_decline_invitation_from_first_user(self):
        json = {"username": self.user_data[0]["username"]}
        self.response = self.send_decline_invitation(headers=self.headers[1], json=json)

    def __when_second_user_delete_first_user_from_friendship(self):
        json = {"username": self.user_data[0]["username"]}
        self.response = self.send_delete_freindship(headers=self.headers[1], json=json)

    def __then_user_get_201_when_invitation_has_been_successfully_send(self):
        self.assertEqual(201, self.response.status_code)
        expected_json = {"status": "success"}
        self.assertEqual(expected_json, self.response.json)

    def __then_invition_from_first_user_is_waiting(self):
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, len(self.response.json["waiting_users"]))
        self.assertEqual(
            self.user_data[0]["username"], self.response.json["waiting_users"][0]
        )

    def __then_second_user_get_204_when_invitation_has_been_successfully_accepted(self):
        self.assertEqual(204, self.response.status_code)
        expected_json = {"status": "success"}
        self.assertEqual(expected_json, self.response.json)

    def __then_second_user_have_friend(self):
        response_json = self.response.json
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, len(response_json["user_friends"]))
        self.assertEqual(
            self.user_data[0]["username"], response_json["user_friends"][0]
        )

    def __then_second_user_have_third_user_in_friendships(self):
        response_json = self.response.json
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, len(response_json["user_friends"]))
        self.assertEqual(
            self.user_data[2]["username"], response_json["user_friends"][0]
        )

    def __then_first_user_have_friend(self):
        response_json = self.response.json
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, len(response_json["user_friends"]))
        self.assertEqual(
            self.user_data[1]["username"], response_json["user_friends"][0]
        )

    def __then_user_get_204_when_invitation_has_been_successfully_declined(self):
        self.assertEqual(204, self.response.status_code)
        expected_json = {"status": "success"}
        self.assertEqual(expected_json, self.response.json)

    def __then_user_get_204_when_friendship_has_been_deleted(self):
        self.assertEqual(204, self.response.status_code)
        expected_json = {"status": "success"}
        self.assertEqual(expected_json, self.response.json)


if __name__ == "__main__":
    unittest.main()
