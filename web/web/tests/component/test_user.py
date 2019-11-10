# web/tests/test_user.py

from web.tests.component.mixins import BaseTestCase


class TestUserBlueprint(BaseTestCase):
    def test_user_registration(self):
        user_data = {"email": "olej@o2.pl", "password": "useruser"}

        response = self.client.post("api/v1/users/register", json=user_data)

        self.assertEqual(201, response.status_code)
        expected_json = {"info": "User successfully created."}
        self.assertEqual(expected_json, response.json)


if __name__ == "__main__":
    unittest.main()
