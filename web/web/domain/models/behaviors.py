import datetime

from web.domain import db


class CreateAtMixin(db.Model):

    __abstract__ = True

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


class UpdateAtMixin(db.Model):

    __abstract__ = True

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )


class IdMixin(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
