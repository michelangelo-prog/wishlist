# web/server/tests/base.py
from flask_testing import TestCase

from web.domain import APP_SETTINGS, create_app, db
from web.domain.models.blacklisttokens import BlacklistToken
from web.domain.models.users import User
from web.tests.factories import UserFactory


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object(APP_SETTINGS["Test"])
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = UserFactory(
            username="PanTestowy", email="testowy@email.pl", password="takieSobiehaslo1"
        )
        self.user = User(**self.user_data)
        db.session.add(self.user)
        db.session.commit()
        self.valid_user_token = self.user.encode_auth_token().decode("UTF-8")
        self.headers = {
            "Authorization": f"Bearer {self.valid_user_token}",
            "Accept": "application/json",
        }


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


class FriendshipMixin:
    def send_invitation_to_user(self, **kwargs):
        uri = "/api/v1/friendships/invitations"
        return self.client.post(uri, **kwargs)

    def get_invitations_from_users(self, **kwargs):
        uri = "/api/v1/friendships/invitations/pending"
        return self.client.get(uri, **kwargs)

    def send_accept_invitation(self, **kwargs):
        uri = "/api/v1/friendships/invitations"
        return self.client.put(uri, **kwargs)

    def send_decline_invitation(self, **kwargs):
        uri = "/api/v1/friendships/invitations"
        return self.client.delete(uri, **kwargs)

    def get_list_of_friends(self, **kwargs):
        uri = "api/v1/friendships/all"
        return self.client.get(uri, **kwargs)

    def send_delete_freindship(self, **kwargs):
        uri = "/api/v1/friendships/delete"
        return self.client.delete(uri, **kwargs)
