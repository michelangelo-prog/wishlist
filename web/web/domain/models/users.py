# web/domain/users.py

from web.domain import db
from web.domain.models.behaviors import IdMixin, CreateAtMixin, UpdateAtMixin

from werkzeug.security import generate_password_hash, check_password_hash

from marshmallow import Schema, fields


class User(IdMixin, CreateAtMixin, UpdateAtMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        user_data = UserSchema().load(kwargs)

        self.email = user_data.get("email")
        password = user_data.get("password")
        self.password = generate_password_hash(password, method="sha256")

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")

        if not email or not password:
            return None

        user = self.__get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def __get_user_by_email(self, email):
        return self.query.filter_by(email=email).one()

    def to_dict(self):
        return dict(id=self.id, email=self.email)


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
