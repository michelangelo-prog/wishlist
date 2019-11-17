from flask import Blueprint, request, jsonify

from marshmallow import ValidationError

from web.domain import db
from web.domain.models.users import User
from web.domain.models.blacklisttokens import BlacklistToken


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["POST"])
def register():
    try:
        json = request.get_json()
        user = User(**json)
        db.session.add(user)
        db.session.commit()
        return jsonify({"info": "User successfully created."}), 201
    except ValidationError as exc:
        return jsonify(str(exc)), 400


@user_blueprint.route("/login", methods=["POST"])
def login():
    json = request.get_json()
    user = User.authenticate(**json)

    token = user.encode_auth_token()
    return jsonify({"token": token}), 201


logout_msg_success = {
    "message": "Successfully logged out.",
}

logout_msg_fail = {
    "message": "Invalid token. Registeration and / or authentication required",
}


@user_blueprint.route("/logout", methods=["POST"])
def logout():
    auth_headers = request.headers.get("Authorization", "").split()

    if len(auth_headers) != 2:
        return jsonify(logout_msg_fail), 401

    try:
        token = auth_headers[1]
        data = User.decode_auth_token(token)
        User.get_user_by_email(email=data["sub"])
        blacklisttoken = BlacklistToken(token=token)
        db.session.add(blacklisttoken)
        db.session.commit()
        return jsonify(logout_msg_success), 200
    except Exception as e:
        return jsonify(logout_msg_fail), 401
