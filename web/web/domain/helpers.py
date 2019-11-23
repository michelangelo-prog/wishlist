# web/domain/helpers.py
from web.domain.models.users import User
from web.domain.models.blacklisttokens import BlacklistToken

from jwt import InvalidTokenError, ExpiredSignatureError

from sqlalchemy.orm.exc import NoResultFound


def check_if_token_valid(token):
    try:
        BlacklistToken.get_blacklistedtoken_by_token(token)
        return False
    except NoResultFound:
        data = User.decode_auth_token(token)
        User.get_user_by_email(email=data["sub"])
        return True
    except (ExpiredSignatureError, InvalidTokenError, NoResultFound):
        return False


def __check_if_token_is_blacklisted(token):
    try:
        if BlacklistToken.get_blacklistedtoken_by_token(token):
            raise ExpiredSignatureError
    except NoResultFound:
        pass


def get_authorization_from_request_headers(request):
    return request.headers.get("Authorization", "").split()
