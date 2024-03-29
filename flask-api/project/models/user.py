from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from datetime import datetime
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import db


@dataclass
class User(db.Model, SerializerMixin, UserMixin):
    __tablename__="users"
    serialize_only=("user_id", "username", "password_hash", "email", "created_at", "updated_at", "is_admin")

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    _password: Mapped[str] = mapped_column("password", nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_admin: Mapped[bool] = mapped_column(default=False)

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)


# @db.event.listens_for(User, 'before_insert')
# @db.event.listens_for(User, 'before_update')
# def hash_password(mapper, connection, target):
#     if target._password is not None:
#         target._password = generate_password_hash(target._password)
#         print("hash_password", target._password)
