import unittest

import pytest

from web.tests.component.mixins import BaseTestCase, FriendshipMixin, UserMixin
from web.tests.factories import UserFactory


class TestFriendshipBlueprint(UserMixin, FriendshipMixin, BaseTestCase):
    def test_user_can_send_invitation_to_another_user(self):
        self.__given_two_registered_users()
        self.json = self.__prepare_dict_with_username(self.users_data[1]["username"])
        self.__when_user_send_invitation(
            action_user_headers=self.users_data[0]["headers"], json=self.json
        )
        self.__then_user_get_201_when_invitation_has_been_successfully_sent()

    def __given_two_registered_users(self):
        self.users_data = self.create_users(number_of_users=2)

    def create_users(self, number_of_users):
        users_data = [UserFactory.build() for i in range(number_of_users)]

        for user_data in users_data:
            self.register_user(user_data)
            login_response = self.login_user(user_data)
            user_header = self.__prepare_user_header(login_response.json["token"])
            user_data["headers"] = user_header

        return users_data

    def register_user(self, user_data):
        response = self.send_register_user(json=user_data)
        self.assertEqual(201, response.status_code)
        return response

    def login_user(self, user_data):
        json = self.__prepare_login_json(user_data)
        response = self.send_login_user(json=json)
        self.assertEqual(201, response.status_code)
        return response

    def __prepare_login_json(self, user_data):
        return {"email": user_data["email"], "password": user_data["password"]}

    def __prepare_user_header(self, token):
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    def __prepare_dict_with_username(self, username):
        return {"username": username}

    def __when_user_send_invitation(self, action_user_headers=None, json=None):
        self.response = self.send_invitation_to_user(
            headers=action_user_headers, json=json
        )

    def __then_user_get_201_when_invitation_has_been_successfully_sent(self):
        self.assertEqual(201, self.response.status_code)
        expected_json = {"status": "success"}
        self.assertEqual(expected_json, self.response.json)

    def test_return_400_when_user_send_invitation_twice(self):
        self.__given_two_users_and_one_sent_invitation()
        self.json = self.__prepare_dict_with_username(self.users_data[1]["username"])
        self.__when_user_send_invitation(
            action_user_headers=self.users_data[0]["headers"], json=self.json
        )
        self.__then_user_get_400_with_error()

    def __given_two_users_and_one_sent_invitation(self):
        self.users_data = self.create_users(number_of_users=2)
        self.send_invitation(
            action_user_data=self.users_data[0], to_user_data=self.users_data[1]
        )

    def send_invitation(self, action_user_data, to_user_data):
        json = self.__prepare_dict_with_username(to_user_data["username"])
        response = self.send_invitation_to_user(
            headers=action_user_data["headers"], json=json
        )
        self.assertEqual(201, response.status_code)

    def __then_user_get_400_with_error(self):
        self.assertEqual(400, self.response.status_code)
        expected_json = {"error": "Bad Request"}
        self.assertEqual(expected_json, self.response.json)

    def test_return_400_when_user_send_invitation_to_not_existing_user(self):
        self.__given_two_registered_users()
        self.json = self.__prepare_dict_with_username("Test")
        self.__when_user_send_invitation(
            action_user_headers=self.users_data[0]["headers"], json=self.json
        )
        self.__then_user_get_400_with_error()

    def test_return_400_when_user_send_invitation_without_json(self):
        self.__given_two_registered_users()
        self.__when_user_send_invitation(
            action_user_headers=self.users_data[0]["headers"]
        )
        self.__then_user_get_400_with_error()

    def test_return_400_when_send_invitation_with_additional_data_in_json(self):
        self.__given_two_registered_users()
        self.json = self.__prepare_dict_with_username(self.users_data[1]["username"])
        self.json["test"] = "test"
        self.__when_user_send_invitation(
            action_user_headers=self.users_data[0]["headers"], json=self.json
        )
        self.__then_user_get_400_with_error()

    def test_return_400_when_send_invitation_with_invalid_data_in_json(self):
        self.__given_two_registered_users()
        self.__when_user_send_invitation(
            action_user_headers=self.users_data[0]["headers"], json={"test": "test"}
        )
        self.__then_user_get_400_with_error()

    def test_return_400_when_user_send_invitation_to_friend(self):
        self.__given_user_with_friend()
        self.json = self.__prepare_dict_with_username(self.users_data[1]["username"])
        self.__when_user_send_invitation(
            action_user_headers=self.users_data[0]["headers"], json=self.json
        )
        self.__then_user_get_400_with_error()

    def __given_user_with_friend(self):
        self.users_data = self.create_users(number_of_users=2)

        for user_data in self.users_data[1:]:
            self.send_invitation(
                action_user_data=user_data, to_user_data=self.users_data[0]
            )
            self.accept_invitation(
                action_user_data=self.users_data[0], from_user_data=user_data
            )

    def test_user_can_list_invitations_for_acceptance(self):
        self.__given_two_users_and_one_sent_invitation()
        self.__when_user_check_if_have_invitations_from_another_users(
            action_user_header=self.users_data[1]["headers"]
        )
        self.__then_return_200_and_one_pending_invitation()

    def __when_user_check_if_have_invitations_from_another_users(
        self, action_user_header
    ):
        self.response = self.get_invitations_from_users(headers=action_user_header)

    def __then_return_200_and_one_pending_invitation(self):
        self.assertEqual(200, self.response.status_code)
        expected_json = {"results": [{"username": self.users_data[0]["username"]}]}
        self.assertEqual(expected_json, self.response.json)

    def test_get_empty_pending_list_when_user_have_no_invitation_to_accept(self):
        self.__given_two_registered_users()
        self.__when_user_check_if_have_invitations_from_another_users(
            action_user_header=self.users_data[1]["headers"]
        )
        self.__then_return_200_and_empty_pending_invitation_list()

    def __then_return_200_and_empty_pending_invitation_list(self):
        self.assertEqual(200, self.response.status_code)
        expected_json = {"results": []}
        self.assertEqual(expected_json, self.response.json)

    @pytest.mark.skip(reason="TODO")
    def test_check_invitations_which_user_sent(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_check_invitations_which_user_sent_when_no_invitations_have_been_sent(self):
        pass

    def test_user_accept_invitation_from_another_user(self):
        self.__given_two_users_and_one_sent_invitation()
        self.json = self.__prepare_dict_with_username(self.users_data[0]["username"])
        self.__when_user_accept_invitation(
            action_user_header=self.users_data[1]["headers"], json=self.json
        )
        self.__then_user_get_200_and_json_with_success_status()

    def __when_user_accept_invitation(self, action_user_header=None, json=None):
        self.response = self.send_accept_invitation(
            headers=action_user_header, json=json
        )

    def __then_user_get_200_and_json_with_success_status(self):
        self.assertEqual(200, self.response.status_code)
        expected_json = {"status": "success"}
        self.assertEqual(expected_json, self.response.json)

    def test_return_400_if_want_to_accept_not_existing_invitation(self):
        self.__given_two_registered_users()
        self.json = self.__prepare_dict_with_username(self.users_data[0]["username"])
        self.__when_user_accept_invitation(
            action_user_header=self.users_data[1]["headers"], json=self.json
        )
        self.__then_user_get_400_with_error()

    def test_return_400_if_want_to_accept_not_existing_user(self):
        self.__given_two_users_and_one_sent_invitation()
        self.json = self.__prepare_dict_with_username("TEST")
        self.__when_user_accept_invitation(
            action_user_header=self.users_data[1]["headers"], json=self.json
        )
        self.__then_user_get_400_with_error()

    def test_return_400_when_user_want_to_accept_user_but_send_more_data_in_json(self):
        self.__given_two_users_and_one_sent_invitation()
        self.json = self.__prepare_dict_with_username(self.users_data[0]["username"])
        self.json["test"] = "TEST"
        self.__when_user_accept_invitation(
            action_user_header=self.users_data[1]["headers"], json=self.json
        )
        self.__then_user_get_400_with_error()

    def test_return_400_when_user_want_to_accept_without_json(self):
        self.__given_two_users_and_one_sent_invitation()
        self.__when_user_accept_invitation(
            action_user_header=self.users_data[1]["headers"]
        )
        self.__then_user_get_400_with_error()

    def test_user_have_four_friends(self):
        self.__given_user_with_four_friends()
        self.__when_user_check_if_have_any_friends(
            action_user_header=self.users_data[0]["headers"]
        )
        self.__then_user_get_list_with_four_friends()

    def __given_user_with_four_friends(self):
        self.users_data = self.create_users(number_of_users=5)

        for user_data in self.users_data[1:]:
            self.send_invitation(
                action_user_data=user_data, to_user_data=self.users_data[0]
            )
            self.accept_invitation(
                action_user_data=self.users_data[0], from_user_data=user_data
            )

    def accept_invitation(self, action_user_data, from_user_data):
        json = self.__prepare_dict_with_username(from_user_data["username"])
        response = self.send_accept_invitation(
            headers=action_user_data["headers"], json=json
        )
        self.assertEqual(200, response.status_code)

    def __when_user_check_if_have_any_friends(self, action_user_header):
        self.response = self.get_list_of_friends(headers=action_user_header)

    def __then_user_get_list_with_four_friends(self):
        self.assertEqual(200, self.response.status_code)
        json = self.response.json
        self.assertEqual(4, len(json["results"]))

        for user_data, result in zip(self.users_data[1:], json["results"]):
            self.assertEqual(user_data["username"], result["username"])

    def test_user_have_one_friend(self):
        self.__given_user_with_four_friends()
        self.__when_user_check_if_have_any_friends(
            action_user_header=self.users_data[1]["headers"]
        )
        self.__then_user_have_one_friend()

    def __then_user_have_one_friend(self):
        self.assertEqual(200, self.response.status_code)
        json = self.response.json
        self.assertEqual(1, len(json["results"]))
        self.assertEqual(self.users_data[0]["username"], json["results"][0]["username"])

    def test_when_user_have_no_friends(self):
        self.__given_two_registered_users()
        self.__when_user_check_if_have_any_friends(
            action_user_header=self.users_data[1]["headers"]
        )
        self.__then_user_have_no_friends()

    def __then_user_have_no_friends(self):
        self.assertEqual(200, self.response.status_code)
        json = self.response.json
        self.assertEqual(0, len(json["results"]))

    def test_user_can_decline_inviation(self):
        self.__given_two_users_and_one_sent_invitation()
        self.action_user_headers = self.users_data[1]["headers"]
        self.json = self.__prepare_dict_with_username(self.users_data[0]["username"])
        self.__when_user_decline_invitation(
            action_user_headers=self.action_user_headers, json=self.json
        )
        self.__then_user_get_200_and_json_with_success_status()

    def __when_user_decline_invitation(self, action_user_headers, json):
        self.response = self.send_decline_invitation(
            headers=action_user_headers, json=json
        )

    def test_user_have_no_waiting_invitation_when_decline_invitation(self):
        self.__given_user_who_decline_invitation()
        self.__when_user_check_if_have_invitations_from_another_users(
            action_user_header=self.users_data[1]["headers"]
        )
        self.__then_return_200_and_empty_pending_invitation_list()

    def __given_user_who_decline_invitation(self):
        self.users_data = self.create_users(number_of_users=2)
        self.send_invitation(
            action_user_data=self.users_data[0], to_user_data=self.users_data[1]
        )
        self.decline_invitation(
            action_user_data=self.users_data[1], to_user_data=self.users_data[0]
        )

    def decline_invitation(self, action_user_data, to_user_data):
        json = self.__prepare_dict_with_username(to_user_data["username"])
        response = self.send_decline_invitation(
            headers=action_user_data["headers"], json=json
        )
        self.assertEqual(200, response.status_code)

    @pytest.mark.skip(reason="TODO")
    def test_user_who_sent_invitation_can_decline_invitation(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_user_who_declined_own_invitation_have_no_pending_invitations(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_user_have_no_pending_invitation_when_action_user_decline_invitation(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_user_delete_friend_from_friends(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_deleted_user_not_in_list_of_friends(self):
        pass


if __name__ == "__main__":
    unittest.main()
