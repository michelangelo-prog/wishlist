from flask import Blueprint, jsonify, request
from marshmallow import Schema, ValidationError, fields, validates_schema

from web.domain import db
from web.domain.decorators import request_schema, token_required
from web.domain.helpers import get_authorization_from_request_headers
from web.domain.models.blacklisttokens import BlacklistToken
from web.domain.models.users import User

user_blueprint = Blueprint("user", __name__)

register_msg_success = {"message": "User successfully created."}

login_msg_fail = {"message": "Invalid user data."}

logout_msg_success = {"message": "Successfully logged out."}

logout_msg_fail = {
    "message": "Invalid token. Registeration and / or authentication required"
}


class UserLoginRequestSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(required=True)

    @validates_schema
    def validate_username_and_email(self, data, **kwargs):
        if data.get("username") and data.get("email"):
            raise ValidationError("Email and Username provided.")
        elif not data.get("username") and not data.get("email"):
            raise ValidationError("Email or username not provided.")


@user_blueprint.route("/register", methods=["POST"])
def register():
    try:
        json = request.get_json()
        user = User(**json)
        db.session.add(user)
        db.session.commit()
        return jsonify(register_msg_success), 201
    except ValidationError as exc:
        return jsonify({"message": str(exc)}), 400


@user_blueprint.route("/login", methods=["POST"])
@request_schema(UserLoginRequestSchema)
def login(json_data):
    try:
        user = User.authenticate(**json_data)

        token = user.encode_auth_token().decode("UTF-8")
        return jsonify({"token": token}), 201
    except Exception:
        return jsonify(login_msg_fail), 401


@user_blueprint.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    token = get_authorization_from_request_headers(request)[1]
    blacklisttoken = BlacklistToken(token=token)
    db.session.add(blacklisttoken)
    db.session.commit()
    return jsonify(logout_msg_success), 200
