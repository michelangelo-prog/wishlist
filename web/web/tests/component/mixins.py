# web/server/tests/base.py
from flask_testing import TestCase

from web.domain import db, create_app, APP_SETTINGS
from web.domain.models.users import User
from web.domain.models.blacklisttokens import BlacklistToken
from web.tests.factories import UserFactory


class BaseTestCase(TestCase):
    def create_app(self, app_settings="Test"):
        app = create_app()
        app.config.from_object(APP_SETTINGS[app_settings])
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.user_data = UserFactory(
            username="PanTestowy", email="testowy@email.pl", password="takieSobiehaslo1"
        )
        self.user = User(**self.user_data)
        db.session.add(self.user)
        db.session.commit()
        self.valid_user_token = self.user.encode_auth_token()
        self.headers = {
            "Authorization": f"Bearer {self.valid_user_token}",
            "Accept": "application/json",
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserMixin:
    def send_register_user(self, **kwargs):
        uri = "/api/v1/users/register"
        return self.client.post(uri, **kwargs)

    def send_login_user(self, **kwargs):
        uri = "/api/v1/users/login"
        return self.client.post(uri, **kwargs)

    def send_logout_user(self, **kwargs):
        uri = "api/v1/users/logout"
        return self.client.post(uri, **kwargs)

    def blacklist_token(self, token):
        blacklisttoken = BlacklistToken(token=token)
        db.session.add(blacklisttoken)
        db.session.commit()
