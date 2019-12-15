# web/domain/friendships.py
from marshmallow import ValidationError
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from web.domain import db
from web.domain.models.behaviors import IdMixin

STATUS = {1: "Pending", 2: "Accepted", 3: "Declined", 4: "Blocked"}


class Friendship(IdMixin, db.Model):
    __tablename__ = "friendships"

    user_one_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_two_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Integer, nullable=False)
    user_one = relationship("User", foreign_keys=[user_one_id])
    user_two = relationship("User", foreign_keys=[user_two_id])
    action_user = relationship("User", foreign_keys=[action_user_id])

    def __init__(self, **kwargs):
        kwargs["user_one"], kwargs["user_two"] = self.__set_up_users_order(
            kwargs["user_one"], kwargs["user_two"]
        )
        self.__check_if_invitation_already_exists(**kwargs)
        super().__init__(**kwargs)

    def __set_up_users_order(self, user_one, user_two):
        if user_one.id < user_two.id:
            return user_one, user_two
        else:
            return user_two, user_one

    def __check_if_invitation_already_exists(self, **kwargs):
        if self.query.filter_by(
            user_one=kwargs["user_one"],
            user_two=kwargs["user_two"],
            status=kwargs["status"],
        ).one_or_none():
            raise ValidationError("Already exists.")

    @classmethod
    def add_invitation(cls, action_user, user):
        obj = cls(
            user_one=action_user, user_two=user, status=1, action_user=action_user
        )
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def get_list_of_pending_users(cls, user):
        objs = cls.get_user_pending_friendships(user)
        return [
            obj.user_two if obj.user_one.username == user.username else obj.user_one
            for obj in objs
        ]

    @classmethod
    def get_user_pending_friendships(cls, user):
        return cls.query.filter(
            (cls.action_user != user)
            & ((cls.user_two == user) | (cls.user_one == user))
        ).all()
