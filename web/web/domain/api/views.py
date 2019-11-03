from flask import Blueprint
from flask_restful import Api

from .resources.hello_world import HelloWorldEndpoint

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint)

api.add_resource(HelloWorldEndpoint, "/helloworld", endpoint="helloworld")
