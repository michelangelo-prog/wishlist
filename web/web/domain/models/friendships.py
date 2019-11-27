# web/domain/friendships.py
# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.utils.types.choice import ChoiceType
#
# from web.domain import db
# from web.domain.models.behaviors import IdMixin
#
#
# class Friendship(IdMixin, db.Model):
#     STATUS = [
#         (1, "Pending"),
#         (2, "Accepted"),
#         (3, "Declined"),
#         (4, "Blocked"),
#     ]
#
#     __tablename__ = "friendships"
#
#     user_one_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     user_two_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     action_user = Column(Integer, ForeignKey("users.id"), nullable=False)
#     status = Column(ChoiceType(STATUS, impl=Integer()), nullable=False)
#     user_one = relationship("User", foreign_keys=[user_one_id])
#     user_two = relationship("User", foreign_keys=[user_two_id])
#     action_user = relationship("User", foreign_keys=[action_user])
