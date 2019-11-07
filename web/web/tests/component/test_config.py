# web/tests/test_config.py
import os

from flask import current_app

from web.tests.component.mixins import BaseTestCase


class TestDevelopmentConfig(BaseTestCase):
    def create_app(self):
        app = super().create_app()
        app.config.from_object("web.domain.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        self.assertFalse(current_app.config["TESTING"])
        self.assertFalse(current_app.config["WTF_CSRF_ENABLED"])
        self.assertFalse(current_app is None)


class TestTestingConfig(BaseTestCase):
    def create_app(self):
        app = super().create_app()
        app.config.from_object("web.domain.config.TestingConfig")
        return app

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
        self.assertFalse(current_app.config["WTF_CSRF_ENABLED"])


class TestProductionConfig(BaseTestCase):
    def create_app(self):
        app = super().create_app()
        app.config.from_object("web.domain.config.ProductionConfig")
        return app

    def test_app_is_production(self):
        self.assertFalse(current_app.config["TESTING"])
        self.assertTrue(current_app.config["WTF_CSRF_ENABLED"])

    def test_secret_key_has_been_set(self):
        self.assertTrue(current_app.secret_key, os.getenv("SECRET_KEY"))
