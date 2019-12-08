from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from web.domain import db
from web.domain.decorators import token_required
from web.domain.helpers import get_authorization_from_request_headers
from web.domain.models.blacklisttokens import BlacklistToken
from web.domain.models.users import User

user_blueprint = Blueprint("user", __name__)

register_msg_success = {"status": "fail", "message": "User successfully created."}

login_msg_fail = {"status": "fail", "message": "Invalid user data."}

logout_msg_success = {"status": "success", "message": "Successfully logged out."}

logout_msg_fail = {
    "status": "fail",
    "message": "Invalid token. Registeration and / or authentication required",
}


@user_blueprint.route("/register", methods=["POST"])
def register():
    try:
        json = request.get_json()
        user = User(**json)
        db.session.add(user)
        db.session.commit()
        return jsonify(register_msg_success), 201
    except ValidationError as exc:
        return jsonify(str(exc)), 400


@user_blueprint.route("/login", methods=["POST"])
def login():
    try:
        json = request.get_json()
        user = User.authenticate(**json)

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
