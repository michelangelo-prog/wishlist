# web/domain/users.py
from datetime import datetime, timedelta

import jwt
from flask import current_app
from marshmallow import Schema, ValidationError, fields
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import validates
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from web.domain import db
from web.domain.models.behaviors import CreateAtMixin, IdMixin, UpdateAtMixin

TOKEN_ALGORITHM = "HS256"


class UserDoesNotExist(Exception):
    """Raise when user does not exist."""

    pass


class User(IdMixin, CreateAtMixin, UpdateAtMixin, db.Model):
    __tablename__ = "users"

    username = Column(String(120), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        user_data = UserSchema().load(kwargs)
        super().__init__(**user_data)

    @validates("username")
    def validate_username(self, key, value):
        if not key or not value:
            raise ValidationError("Username not provided.")
        if User.user_with_username_exists(value):
            raise ValidationError("User with given username exists.")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not key or not value:
            raise ValidationError("Email not provided.")
        if User.user_with_email_exists(value):
            raise ValidationError("User with given email exists.")
        return value

    @validates("password")
    def validate_password(self, key, value):
        if not key or not value:
            raise ValidationError("Password not provided.")
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
        username = kwargs.get("username")
        email = kwargs.get("email")
        password = kwargs.get("password")

        if username and password:
            user = cls.get_user_by_username(username)
        elif email and password:
            user = cls.get_user_by_email(email)
        else:
            return None

        if not user or not check_password_hash(user.password, password):
            return None

        return user

    @classmethod
    def get_user_by_email(cls, email):
        try:
            return cls.query.filter_by(email=email).one()
        except NoResultFound:
            raise UserDoesNotExist("User does not exist.")

    @classmethod
    def get_user_by_username(cls, username):
        try:
            return cls.query.filter_by(username=username).one()
        except NoResultFound:
            raise UserDoesNotExist("User does not exist.")

    @classmethod
    def decode_auth_token(cls, token):
        return jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=TOKEN_ALGORITHM
        )

    def encode_auth_token(self):
        payload = {
            "sub": self.email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }
        return jwt.encode(
            payload, current_app.config["SECRET_KEY"], algorithm=TOKEN_ALGORITHM
        )


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
