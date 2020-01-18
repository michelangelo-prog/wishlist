# web/tests/test_hello_world.py
import unittest

from web.tests.component.mixins import UserBaseTestCase


class TestHelloWorldBlueprint(UserBaseTestCase):
    def test_hello_world(self):
        uri = "/helloworld"
        response = self.client.get(uri, headers=self.headers)

        self.assertEqual(200, response.status_code)
        expected_json = {"message": "Hello World!"}
        self.assertEqual(expected_json, response.json)


if __name__ == "__main__":
    unittest.main()
