# web/server/tests/base.py


from flask_testing import TestCase

from web.domain import db, create_app, APP_SETTINGS


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object(APP_SETTINGS["Test"])
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
