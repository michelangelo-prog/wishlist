# web/tests/test_user.py
import unittest

from web.tests.component.mixins import UserBaseTestCase, UserMixin
from web.tests.factories import UserFactory

from web.domain.helpers import check_if_token_valid
from web.domain.models.users import User


class TestUserBlueprint(UserMixin, UserBaseTestCase):
    def test_correct_registration(self):
        data = UserFactory.build()
        response = self.send_register_user(json=data)

        self.assertEqual(201, response.status_code)
        expected_json = {
            "status": "fail",
            "message": "User successfully created.",
        }
        self.assertEqual(expected_json, response.json)

    def test_return_400_when_try_to_register_already_existing_username(self):
        data = UserFactory.build()
        self.send_register_user(json=data)
        response = self.send_register_user(json=data)
        self.assertEqual(400, response.status_code)

    def test_return_400_when_register_user_without_username(self):
        data = UserFactory.build()
        del data["username"]

        response = self.send_register_user(json=data)
        self.assertEqual(400, response.status_code)

    def test_return_400_when_register_user_without_email(self):
        data = UserFactory.build()
        del data["email"]

        response = self.send_register_user(json=data)
        self.assertEqual(400, response.status_code)

    def test_return_400_when_register_user_without_password(self):
        data = UserFactory.build()
        del data["password"]

        response = self.send_register_user(json=data)
        self.assertEqual(400, response.status_code)

    def test_return_400_when_register_user_without_data(self):
        data = UserFactory.build()
        del data["email"], data["password"], data["username"]

        response = self.send_register_user(json=data)
        self.assertEqual(400, response.status_code)

    def test_correct_login(self):
        response = self.send_login_user(json=self.user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue(check_if_token_valid(response.json["token"]))

    def test_return_401_when_unregistered_user_try_login(self):
        data = UserFactory.build()
        response = self.send_login_user(json=data)
        expected_json = {
            "status": "fail",
            "message": "Invalid user data.",
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_user_try_login_without_password(self):
        del self.user_data["password"]
        response = self.send_login_user(json=self.user_data)
        expected_json = {
            "status": "fail",
            "message": "Invalid user data.",
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_user_try_login_without_email_and_password(self):
        del self.user_data["email"], self.user_data["password"]
        response = self.send_login_user(json=self.user_data)
        expected_json = {
            "status": "fail",
            "message": "Invalid user data.",
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_correct_logout(self):
        response = self.send_logout_user(headers=self.headers)
        expected_json = {
            "status": "success",
            "message": "Successfully logged out.",
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_unregistered_user_try_logout(self):
        user_data = UserFactory.build()
        user = User(**user_data)
        token = user.encode_auth_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        response = self.send_logout_user(headers=headers)

        expected_json = {
            "message": "Invalid token. Registeration and / or authentication required",
            "authenticated": False,
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_user_try_logout_and_token_blacklisted(self):
        self.blacklist_token(self.valid_user_token)
        response = self.send_logout_user(headers=self.headers)
        expected_json = {
            "message": "Expired token. Reauthentication required.",
            "authenticated": False,
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_401_when_user_try_logout_and_not_headers_provided(self):
        response = self.send_logout_user()
        expected_json = {
            "message": "Invalid token. Registeration and / or authentication required",
            "authenticated": False,
        }
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_json, response.json)


if __name__ == "__main__":
    unittest.main()
