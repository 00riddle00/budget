"""Here reside database models, used by ORM."""

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class Income(db.Model):
    __tablename__ = "income"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    amount: Mapped[float] = mapped_column(Float)
    sender: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    entry_date: Mapped[str] = mapped_column(String)


class Expense(db.Model):
    __tablename__ = "expense"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    amount: Mapped[float] = mapped_column(Float)
    payment_option: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    entry_date: Mapped[str] = mapped_column(String)


class User(UserMixin, db.Model):
    """A user is the single most important component of our web app."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    profile_picture: Mapped[str] = mapped_column(
        String, nullable=False, default="default.jpg"
    )
    entries_income: Mapped["Income"] = relationship("Income")
    entries_expenses: Mapped["Expense"] = relationship("Expense")

    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
