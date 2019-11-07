# web/domain/users.py

from web.domain import db
from web.domain.models.behaviors import IdMixin, CreateAtMixin, UpdateAtMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(IdMixin, CreateAtMixin, UpdateAtMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get("email")
        password = kwargs.get("password")
        self.password = generate_password_hash(password, method="sha256")
