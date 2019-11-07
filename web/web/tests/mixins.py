# web/server/tests/base.py


from flask_testing import TestCase

from web.domain import db, create_app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("web.domain.config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
