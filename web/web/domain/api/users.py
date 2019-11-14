from flask import Blueprint, request, jsonify, current_app

from marshmallow import ValidationError

from web.domain import db
from web.domain.models.users import User

import jwt
from datetime import datetime, timedelta

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

    token = jwt.encode(
        {
            "sub": user.email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        current_app.config["SECRET_KEY"],
    )
    return jsonify({"token": token.decode("UTF-8")}), 201
