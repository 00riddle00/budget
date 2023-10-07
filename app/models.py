from . import db
from flask_login import UserMixin
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import login_manager


@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))


# class Entry(db.Model):
# 	type = db.Column(db.String(64), index=True) Bool as an option

class Income(db.Model):
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
	amount: Mapped[float] = mapped_column(Float)
	sender: Mapped[str] = mapped_column(String)
	description: Mapped[str] = mapped_column(String)
	entry_date: Mapped[str] = mapped_column(String)


class Expenses(db.Model):
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
	amount: Mapped[float] = mapped_column(Float)
	payment_option: Mapped[str] = mapped_column(String)
	description: Mapped[str] = mapped_column(String)
	entry_date: Mapped[str] = mapped_column(String)


class User(UserMixin, db.Model):
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	profile_picture: Mapped[str] = mapped_column(String, nullable=False, default='default.jpg')
	entries_income: Mapped["Income"] = relationship("Income")
	entries_expenses: Mapped["Expenses"] = relationship("Expenses")

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
