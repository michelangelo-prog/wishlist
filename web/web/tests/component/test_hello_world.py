# web/tests/test_hello_world.py
import unittest

from web.tests.component.mixins import BaseTestCase


class TestHelloWorldBlueprint(BaseTestCase):
    def test_hello_world(self):
        uri = "/helloworld"
        response = self.client.get(uri, headers=self.headers)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
