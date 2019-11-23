from web.domain import db
from web.domain.models.behaviors import IdMixin

import datetime


class BlacklistToken(IdMixin, db.Model):
    __tablename__ = "blacklist_tokens"

    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now
    )

    @classmethod
    def get_blacklistedtoken_by_token(cls, token):
        return cls.query.filter_by(token=token).one()

    def __repr__(self):
        return f"<token: {self.token}>"
