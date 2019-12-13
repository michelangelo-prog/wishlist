from flask import Blueprint, jsonify
from marshmallow import Schema, ValidationError, fields

from web.domain.decorators import request_schema, token_required
from web.domain.models.friendships import Friendship
from web.domain.models.users import User, UserDoesNotExist

friendship_blueprint = Blueprint("friendship", __name__)


class FriendshipRequestSchema(Schema):
    username = fields.Str(required=True)


@friendship_blueprint.route("/invitations", methods=["POST"])
@token_required
@request_schema(FriendshipRequestSchema)
def send_invitation(json_data, current_user):
    try:
        user = User.get_user_by_username(json_data["username"])
        Friendship.add_invitation(action_user=current_user, user=user)
        return jsonify({"status": "success"}), 201
    except (ValidationError, UserDoesNotExist) as e:
        return jsonify({"status": "fail", "message": str(e)}), 400
