from flask import Blueprint
from flask_restful import Api

from web.domain.api.resources.user import UserAPI

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint)


api.add_resource(UserAPI, "/users/register", endpoint="helloworld")
