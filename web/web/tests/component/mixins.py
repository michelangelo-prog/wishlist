# web/server/tests/base.py


from flask_testing import TestCase

from web.domain import db, create_app, APP_SETTINGS
from web.domain.models.users import User


class BaseTestCase(TestCase):
    def create_app(self, app_settings="Test"):
        app = create_app()
        app.config.from_object(APP_SETTINGS[app_settings])
        return app

    def setUp(self):
        db.create_all()
        self.user_data = {"email": "testowy@email.pl", "password": "takieSobiehaslo1"}
        user = User(**self.user_data)
        db.session.add(user)
        db.session.commit()

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
