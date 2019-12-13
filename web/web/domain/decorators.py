# web/domain/decorators.py
from functools import wraps

from flask import jsonify, request
from jwt import ExpiredSignatureError, InvalidTokenError
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from web.domain.helpers import get_authorization_from_request_headers
from web.domain.models.blacklisttokens import BlacklistToken
from web.domain.models.users import User, UserDoesNotExist

invalid_msg = {
    "message": "Invalid token. Registeration and / or authentication required",
    "authenticated": False,
}
expired_msg = {
    "message": "Expired token. Reauthentication required.",
    "authenticated": False,
}


def __check_if_token_is_blacklisted(token):
    try:
        if BlacklistToken.get_blacklistedtoken_by_token(token):
            raise ExpiredSignatureError
    except NoResultFound:
        pass


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = get_authorization_from_request_headers(request)

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            __check_if_token_is_blacklisted(token)
            data = User.decode_auth_token(token)
            user = User.get_user_by_email(email=data["sub"])
            return f(user, *args, **kwargs)
        except ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (InvalidTokenError, UserDoesNotExist):
            return jsonify(invalid_msg), 401

    return _verify


def request_schema(schema):
    def _verify_schema(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json = request.get_json()
            try:
                json_data = schema().load(json)
            except ValidationError:
                return jsonify({"status": "fail", "message": "Invalid json."}), 400
            return f(json_data, *args, **kwargs)

        return wrapper

    return _verify_schema
