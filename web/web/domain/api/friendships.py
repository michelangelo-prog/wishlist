from flask import Blueprint, abort, jsonify
from marshmallow import Schema, ValidationError, fields

from web.domain.decorators import request_schema, token_required
from web.domain.models.friendships import Friendship, FriendshipDoesNotExist
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
    except (ValidationError, UserDoesNotExist):
        abort(400)


@friendship_blueprint.route("/invitations", methods=["GET"])
@token_required
def list_invitations_from_users(current_user):
    users = Friendship.get_list_of_pending_users(current_user)
    return jsonify({"results": [{"username": user.username} for user in users]}), 200


@friendship_blueprint.route("/invitations", methods=["PUT"])
@token_required
@request_schema(FriendshipRequestSchema)
def accept_invitation_from_user(json_data, current_user):
    try:
        user = User.get_user_by_username(json_data["username"])
        Friendship.accept_invitation(action_user=current_user, user=user)
        return {}, 204
    except (UserDoesNotExist, FriendshipDoesNotExist):
        abort(400)


@friendship_blueprint.route("/invitations", methods=["DELETE"])
@token_required
@request_schema(FriendshipRequestSchema)
def decline_invitation_from_user(json_data, current_user):
    try:
        user = User.get_user_by_username(json_data["username"])
        Friendship.decline_invitation(action_user=current_user, user=user)
        return {}, 204
    except (UserDoesNotExist, FriendshipDoesNotExist):
        abort(400)


@friendship_blueprint.route("/invitations/sent", methods=["GET"])
@token_required
def get_all_users_who_got_invitation(current_user):
    users = Friendship.get_list_of_users_who_got_invitation(current_user)
    return (jsonify({"results": [{"username": user.username} for user in users]}), 200)


@friendship_blueprint.route("/all", methods=["GET"])
@token_required
def get_all_friends(current_user):
    user_friends = Friendship.get_list_of_user_friends(current_user)
    return (
        jsonify({"results": [{"username": user.username} for user in user_friends]}),
        200,
    )


@friendship_blueprint.route("/delete", methods=["DELETE"])
@token_required
@request_schema(FriendshipRequestSchema)
def delete_friend(json_data, current_user):
    try:
        user = User.get_user_by_username(json_data["username"])
        Friendship.delete_friend(action_user=current_user, user=user)
        return {}, 204
    except (UserDoesNotExist, FriendshipDoesNotExist):
        abort(400)
