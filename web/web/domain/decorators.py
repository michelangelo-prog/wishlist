# web/domain/decorators.py
from functools import wraps

from flask import request, jsonify

from sqlalchemy.orm.exc import NoResultFound

from web.domain.models.users import User
from web.domain.helpers import (
    get_authorization_from_request_headers,
    __check_if_token_is_blacklisted,
)

from jwt import ExpiredSignatureError, InvalidTokenError


invalid_msg = {
    "message": "Invalid token. Registeration and / or authentication required",
    "authenticated": False,
}
expired_msg = {
    "message": "Expired token. Reauthentication required.",
    "authenticated": False,
}


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
        except (InvalidTokenError, NoResultFound) as e:
            return jsonify(invalid_msg), 401

    return _verify
