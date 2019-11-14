# web/tests/test_user.py
import unittest

from web.tests.component.mixins import BaseTestCase, UserMixin

from web.tests.factories import UserFactory


class TestUserBlueprint(UserMixin, BaseTestCase):
    def test_correct_registration(self):
        data = UserFactory.build()
        response = self.send_register_user(json=data)

        self.assertEqual(201, response.status_code)
        expected_json = {"info": "User successfully created."}
        self.assertEqual(expected_json, response.json)

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

    def test_return_400_when_register_user_without_email_and_password(self):
        data = UserFactory.build()
        del data["email"], data["password"]

        response = self.send_register_user(json=data)
        self.assertEqual(400, response.status_code)

    def test_correct_login(self):
        response = self.send_login_user(json=self.user_data)
        self.assertEqual(201, response.status_code)


if __name__ == "__main__":
    unittest.main()
