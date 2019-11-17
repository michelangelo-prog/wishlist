# web/domain/users.py

from flask import current_app

from web.domain import db
from web.domain.models.behaviors import IdMixin, CreateAtMixin, UpdateAtMixin

from werkzeug.security import generate_password_hash, check_password_hash

from marshmallow import Schema, fields

import jwt
from datetime import datetime, timedelta


class User(IdMixin, CreateAtMixin, UpdateAtMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        user_data = UserSchema().load(kwargs)

        self.email = user_data.get("email")
        password = user_data.get("password")
        self.password = generate_password_hash(password, method="sha256")

    def to_dict(self):
        return dict(id=self.id, email=self.email)

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")

        if not email or not password:
            return None

        user = cls.get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).one()

    @classmethod
    def decode_auth_token(cls, token):
        return jwt.decode(token, current_app.config["SECRET_KEY"])

    def encode_auth_token(self):
        payload = {
            "sub": self.email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }
        return jwt.encode(payload, current_app.config["SECRET_KEY"]).decode("UTF-8")


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
