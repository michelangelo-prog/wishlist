from flask import request
from flask_restful import Resource

from marshmallow import ValidationError

from web.domain.models.users import User
from web.domain import db


class UserAPI(Resource):
    def post(self):
        try:
            json = request.get_json()
            user = User(**json)
            db.session.add(user)
            db.session.commit()
            return {"info": "User successfully created."}, 201
        except ValidationError as e:
            return 404
