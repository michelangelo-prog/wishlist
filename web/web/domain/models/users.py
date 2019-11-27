# web/domain/users.py

from flask import current_app

from sqlalchemy.orm import validates

from web.domain import db
from web.domain.models.behaviors import IdMixin, CreateAtMixin, UpdateAtMixin

from werkzeug.security import generate_password_hash, check_password_hash

from marshmallow import Schema, fields, ValidationError

import jwt
from datetime import datetime, timedelta


class User(IdMixin, CreateAtMixin, UpdateAtMixin, db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        user_data = UserSchema().load(kwargs)
        super().__init__(**user_data)

    @validates("username")
    def validate_username(self, key, value):
        if not key or not value:
            raise ValidationError(
                {"status": "fail", "message": "Username not provided."}
            )
        if User.user_with_username_exists(value):
            raise ValidationError(
                {"status": "fail", "message": "User with given username exists."}
            )
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not key or not value:
            raise ValidationError({"status": "fail", "message": "Email not provided."})
        if User.user_with_email_exists(value):
            raise ValidationError(
                {"status": "fail", "message": "User with given username exists."}
            )
        return value

    @validates("password")
    def validate_password(self, key, value):
        if not key or not value:
            raise ValidationError(
                {"status": "fail", "message": "Password not provided."}
            )
        return generate_password_hash(value, method="sha256")

    def to_dict(self):
        return dict(id=self.id, email=self.email)

    @classmethod
    def user_with_username_exists(cls, username):
        return cls.query.filter_by(username=username).first() is not None

    @classmethod
    def user_with_email_exists(cls, email):
        return cls.query.filter_by(email=email).first() is not None

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
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
