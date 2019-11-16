from flask import Blueprint, jsonify

helloworld_blueprint = Blueprint("helloworld", __name__)


@helloworld_blueprint.route("/helloworld", methods=["GET"])
def helloworld():
    return jsonify({"message": "Hello World!"}), 200
