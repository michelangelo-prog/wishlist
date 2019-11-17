from flask import Blueprint, jsonify

from web.domain.decorators import token_required

helloworld_blueprint = Blueprint("helloworld", __name__)


@helloworld_blueprint.route("/helloworld", methods=["GET"])
@token_required
def helloworld(current_user):
    return jsonify({"message": "Hello World!"}), 200
