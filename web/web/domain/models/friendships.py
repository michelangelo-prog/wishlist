# web/domain/friendships.py
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

    @classmethod
    def add_invitation(cls, action_user, user):
        user_one, user_two = cls.__get_users_in_order(action_user, user)
        obj = cls(
            user_one=user_one, user_two=user_two, status=1, action_user=action_user
        )
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def __get_users_in_order(cls, user_one, user_two):
        if user_one.id < user_two.id:
            return user_one, user_two
        else:
            return user_two, user_one
