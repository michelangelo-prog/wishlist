from flask import Blueprint, request, jsonify

from marshmallow import ValidationError

from web.domain import db
from web.domain.models.users import User

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
