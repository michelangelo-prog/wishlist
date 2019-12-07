# web/domain/helpers.py
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm.exc import NoResultFound

from web.domain.models.blacklisttokens import BlacklistToken
from web.domain.models.users import User


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


def get_authorization_from_request_headers(request):
    return request.headers.get("Authorization", "").split()
