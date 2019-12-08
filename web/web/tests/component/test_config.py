# web/tests/test_config.py
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from web.domain import APP_SETTINGS, create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object(APP_SETTINGS["Development"])
        return app

    def test_app_is_development(self):
        self.assertFalse(current_app.config["TESTING"])
        self.assertFalse(current_app.config["WTF_CSRF_ENABLED"])
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(APP_SETTINGS["Test"])
        return app

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
        self.assertFalse(current_app.config["WTF_CSRF_ENABLED"])
        self.assertFalse(current_app is None)


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object(APP_SETTINGS["Production"])
        return app

    def test_app_is_production(self):
        self.assertFalse(current_app.config["TESTING"])
        self.assertTrue(current_app.config["WTF_CSRF_ENABLED"])
        self.assertFalse(current_app is None)

    def test_secret_key_has_been_set(self):
        self.assertTrue(
            current_app.secret_key, os.getenv("SECRET_KEY", default="my_precious")
        )


if __name__ == "__main__":
    unittest.main()
