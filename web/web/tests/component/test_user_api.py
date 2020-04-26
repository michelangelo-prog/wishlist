# web/tests/test_user.py
import unittest

from web.domain.helpers import check_if_token_valid
from web.domain.models.users import User
from web.tests.component.mixins import UserBaseTestCase, UserMixin
from web.tests.factories import UserFactory


class TestUserBlueprint(UserMixin, UserBaseTestCase):
    def test_correct_registration(self):
        data = UserFactory.build()
        response = self.send_register_user(json=data)

        self.assertEqual(201, response.status_code)
        expected_json = {"message": "User successfully created."}
        self.assertEqual(expected_json, response.json)

    def test_return_400_when_try_to_register_already_existing_username(self):
        user_data = UserFactory.build()
        self.__given_registered_user(user_data)
        self.__when_try_to_register_user_with_already_existing_data(
            username=user_data["username"]
        )
        self.__then_return_400_with_message("User with given username exists.")

    def __given_registered_user(self, data):
        self.register_user(data)

    def register_user(self, user_data):
        response = self.send_register_user(json=user_data)
        self.assertEqual(201, response.status_code)
        return response

    def __when_try_to_register_user_with_already_existing_data(self, **kwargs):
        user_data = UserFactory.build()
        user_data.update(kwargs)

        self.response = self.send_register_user(json=user_data)

    def __then_return_400_with_message(self, message):
        self.assertEqual(400, self.response.status_code)
        expected_json = {"message": message}
        self.assertEqual(expected_json, self.response.json)

    def test_return_400_when_try_to_register_already_existing_email(self):
        user_data = UserFactory.build()
        self.__given_registered_user(user_data)
        self.__when_try_to_register_user_with_already_existing_data(
            email=user_data["email"]
        )
        self.__then_return_400_with_message("User with given email exists.")

    def test_return_400_when_register_user_without_username(self):
        user_data = UserFactory.build()
        del user_data["username"]

        self.__when_register_user_data(user_data)
        self.__then_return_400()

    def __when_register_user_data(self, user_data):
        self.response = self.send_register_user(json=user_data)

    def test_return_400_when_register_user_without_email(self):
        user_data = UserFactory.build()
        del user_data["email"]

        self.__when_register_user_data(user_data)
        self.__then_return_400()

    def test_return_400_when_register_user_without_password(self):
        user_data = UserFactory.build()
        del user_data["password"]

        self.__when_register_user_data(user_data)
        self.__then_return_400()

    def test_return_400_when_register_user_without_data(self):
        user_data = UserFactory.build()
        del user_data["email"], user_data["password"], user_data["username"]

        self.__when_register_user_data(user_data)
        self.__then_return_400()

    def __then_return_400(self):
        self.assertEqual(400, self.response.status_code)

    def test_correct_login_with_username(self):
        del self.user_data["email"]
        response = self.send_login_user(json=self.user_data)
        self.__check_if_201_and_correct_token(response)

    def __check_if_201_and_correct_token(self, response):
        self.assertEqual(201, response.status_code)
        self.assertTrue(check_if_token_valid(response.json["token"]))

    def test_correct_login_with_email(self):
        del self.user_data["username"]
        response = self.send_login_user(json=self.user_data)
        self.__check_if_201_and_correct_token(response)

    def test_return_401_when_unregistered_user_try_login_with_email(self):
        data = UserFactory.build()
        del data["username"]
        response = self.send_login_user(json=data)
        self.assertEqual(401, response.status_code)

    def test_return_401_when_unregistered_user_try_login_with_username(self):
        data = UserFactory.build()
        del data["email"]
        response = self.send_login_user(json=data)
        self.assertEqual(401, response.status_code)

    def test_return_400_when_unregistered_user_try_login_with_username_and_email(self):
        data = UserFactory.build()
        response = self.send_login_user(json=data)
        self.assertEqual(400, response.status_code)

    def test_return_400_when_user_try_login_with_username_and_without_password(self):
        del self.user_data["password"]
        del self.user_data["email"]
        response = self.send_login_user(json=self.user_data)
        self.assertEqual(400, response.status_code)

    def test_return_400_when_user_try_login_with_email_and_without_password(self):
        del self.user_data["password"]
        del self.user_data["username"]
        response = self.send_login_user(json=self.user_data)
        self.assertEqual(400, response.status_code)

    def test_correct_logout(self):
        response = self.send_logout_user(headers=self.headers)
        expected_json = {"message": "Successfully logged out."}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_unregistered_user_try_logout(self):
        user_data = UserFactory.build()
        user = User(**user_data)
        token = user.encode_auth_token()

        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = self.send_logout_user(headers=headers)

        expected_json = {
            "message": "Invalid token. Registeration and / or authentication required"
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_user_try_logout_and_token_blacklisted(self):
        self.blacklist_token(self.valid_user_token)
        response = self.send_logout_user(headers=self.headers)
        expected_json = {"message": "Expired token. Reauthentication required."}
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_user_try_logout_and_not_headers_provided(self):
        response = self.send_logout_user()
        expected_json = {
            "message": "Invalid token. Registeration and / or authentication required"
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)


if __name__ == "__main__":
    unittest.main()
