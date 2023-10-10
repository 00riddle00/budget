import os
import secrets
from datetime import datetime

from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from PIL import Image

from .. import db
from ..models import Expense, Income
from . import main
from .forms import ExpenseForm, IncomeForm, UserUpdateForm


def get_entries():
    userid = current_user.id
    # Query the database for the user's entries.
    income_data = Income.query.filter_by(user_id=userid).all()
    expense_data = Expense.query.filter_by(user_id=userid).all()
    income_total = sum([i.amount for i in income_data])
    expense_total = sum([i.amount for i in expense_data])
    balance = income_total - expense_total
    return income_data, expense_data, income_total, expense_total, balance


def load_user_picture():
    if current_user.is_authenticated:
        picture_url = url_for(
            "static", filename=f"pfp/{current_user.profile_picture}"
        )
    else:
        picture_url = url_for("static", filename="pfp/default.jpg")
    return picture_url


@main.route("/")
def index():
    picture_url = load_user_picture()
    return render_template("index.html", picture_url=picture_url)


@main.route("/profile", methods=["GET", "POST"])
@login_required
def user_update():
    form = UserUpdateForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_name = save_picture(form.profile_picture.data)
            current_user.profile_picture = picture_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for("main.user_update"))
    picture_url = load_user_picture()
    return render_template("profile.html", form=form, picture_url=picture_url)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/pfp", picture_fn
    )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@main.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    form_income = IncomeForm()
    form_expense = ExpenseForm()
    picture_url = load_user_picture()
    if request.method == "POST":
        if "form1_submit" in request.form and form_income.validate_on_submit():
            inc_amount = request.form["inc_amount"]
            inc_sender = request.form["inc_sender"]
            inc_description = request.form["inc_description"]
            userid = current_user.id
            inc_entry_date = datetime.strptime(
                str(datetime.now())[0:19], "%Y-%m-%d %H:%M:%S"
            )
            db.session.add(
                Income(
                    amount=inc_amount,
                    user_id=userid,
                    sender=inc_sender,
                    description=inc_description,
                    entry_date=inc_entry_date,
                )
            )
            db.session.commit()
        elif (
            "form2_submit" in request.form
            and form_expense.validate_on_submit()
        ):
            exp_payment_option = request.form["exp_payment_option"]
            exp_amount = request.form["exp_amount"]
            exp_description = request.form["exp_description"]
            userid = current_user.id
            exp_entry_date = datetime.strptime(
                str(datetime.now())[0:19], "%Y-%m-%d %H:%M:%S"
            )
            db.session.add(
                Expense(
                    amount=exp_amount,
                    user_id=userid,
                    payment_option=exp_payment_option,
                    description=exp_description,
                    entry_date=exp_entry_date,
                )
            )
            db.session.commit()
        (
            income_data,
            expense_data,
            income_total,
            expense_total,
            balance,
        ) = get_entries()
        return render_template(
            "budget.html",
            income_data=income_data,
            expense_data=expense_data,
            income_total=income_total,
            expense_total=expense_total,
            balance=balance,
            form1=form_income,
            form2=form_expense,
            picture_url=picture_url,
        )
    else:
        (
            income_data,
            expense_data,
            income_total,
            expense_total,
            balance,
        ) = get_entries()
        return render_template(
            "budget.html",
            income_data=income_data,
            expense_data=expense_data,
            income_total=income_total,
            expense_total=expense_total,
            balance=balance,
            form1=form_income,
            form2=form_expense,
            picture_url=picture_url,
        )


@main.route("/remove_entry/<table>/<entry_id:int>", methods=["GET", "POST"])
def remove_entry(table, entry_id):
    form_income = IncomeForm()
    form_expense = ExpenseForm()
    if table == "Income":
        income_entry = Income.query.get_or_404(entry_id)
        db.session.delete(income_entry)
        db.session.commit()
    elif table == "Expense":
        expense_entry = Expense.query.get_or_404(entry_id)
        db.session.delete(expense_entry)
        db.session.commit()
    (
        income_data,
        expense_data,
        income_total,
        expense_total,
        balance,
    ) = get_entries()
    return render_template(
        "budget.html",
        income_data=income_data,
        expense_data=expense_data,
        income_total=income_total,
        expense_total=expense_total,
        balance=balance,
        form1=form_income,
        form2=form_expense,
    )
