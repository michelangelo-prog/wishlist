from flask import request
from flask_restful import Resource

from marshmallow import ValidationError

from web.domain.models.users import User, UserSchema
from web.domain import db


class UserAPI(Resource):
    def post(self):
        try:
            json = request.get_json()
            user_data = UserSchema().load(json)
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            return {"info": "User successfully created."}, 201
        except ValidationError as e:
            return 404
