from datetime import datetime

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .. import db
from ..models import Expense, Income, User
from . import main
from .forms import ExpenseForm, IncomeForm, UserUpdateForm


@main.route("/")
def index():
    picture_url = User.get_picture_url(current_user)
    return render_template("index.html", picture_url=picture_url)


@main.route("/profile", methods=["GET", "POST"])
@login_required
def user_update():
    form = UserUpdateForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_name = current_user.upload_picture_and_get_url(
                form.profile_picture.data
            )
            current_user.profile_picture = picture_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for("main.user_update"))
    picture_url = User.get_picture_url(current_user)
    return render_template("profile.html", form=form, picture_url=picture_url)


@main.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    form_income = IncomeForm()
    form_expense = ExpenseForm()
    picture_url = User.get_picture_url(current_user)
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
        ) = current_user.get_entries()
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
        ) = current_user.get_entries()
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


@main.route("/remove_entry/<table>/<int:entry_id>", methods=["GET", "POST"])
@login_required
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
    ) = current_user.get_entries()
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
