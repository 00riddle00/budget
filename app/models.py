"""Here reside database models, used by ORM."""
import os
import secrets
from datetime import datetime

from flask import current_app, url_for
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from PIL import Image
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db, login_manager


class Income(db.Model):
    __tablename__ = "income"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    sender: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(512))
    entry_date: Mapped[str] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )


class Expense(db.Model):
    __tablename__ = "expense"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_option: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(512))
    entry_date: Mapped[str] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )


class User(UserMixin, db.Model):
    """A user is the single most important component of our web app."""

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    email: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False
    )
    profile_picture: Mapped[str] = mapped_column(
        String(256), nullable=False, default="default.jpg"
    )
    income_entries: Mapped["Income"] = relationship("Income")
    expenses_entries: Mapped["Expense"] = relationship("Expense")

    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def get_picture_url(self):
        user_picture = "default.jpg"
        if self.is_authenticated:
            user_picture = self.profile_picture
        return url_for(
            "static", filename=f"img/user_profile_pictures/{user_picture}"
        )

    @staticmethod
    def upload_picture_and_get_url(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(
            current_app.root_path,
            "static/img/user_profile_pictures",
            picture_fn,
        )
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        return picture_fn

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except Exception:
            return None
        return User.query.get(data["id"])


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
