from flask import Blueprint, jsonify, request

from web.domain.decorators import token_required
from web.domain.models.friendships import Friendship
from web.domain.models.users import User

friendship_blueprint = Blueprint("friendship", __name__)


def get_username_from_request_json(request):
    return request.get_json().pop("username", None)


@friendship_blueprint.route("/invitations", methods=["POST"])
@token_required
def send_invitation(current_user):
    username = get_username_from_request_json(request)
    user = User.get_user_by_username(username)
    Friendship.add_invitation(action_user=current_user, user=user)
    return jsonify({"status": "success"}), 201
