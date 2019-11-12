# web/tests/test_user.py
import unittest

from web.tests.component.mixins import BaseTestCase, UserMixin


class TestUserBlueprint(UserMixin, BaseTestCase):
    def test_user_registration(self):
        json = {"email": "olej@o2.pl", "password": "useruser"}

        response = self.send_register_user(json=json)

        self.assertEqual(201, response.status_code)
        expected_json = {"info": "User successfully created."}
        self.assertEqual(expected_json, response.json)


if __name__ == "__main__":
    unittest.main()
