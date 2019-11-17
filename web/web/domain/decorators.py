# web/domain/decorators.py
from functools import wraps

from flask import request, jsonify

from web.domain.models.users import User

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
        auth_headers = request.headers.get("Authorization", "").split()

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = User.decode_auth_token(token)
            user = User.get_user_by_email(email=data["sub"])
            return f(user, *args, **kwargs)
        except ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (InvalidTokenError, Exception) as e:
            return jsonify(invalid_msg), 401

    return _verify
