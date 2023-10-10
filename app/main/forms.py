from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    PasswordField,
    RadioField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    Length,
    ValidationError,
)

from ..models import User


def validate_amount(_form, amount):
    if not amount.data.isdigit():
        raise ValidationError("Amount must be a number.")
    if float(amount.data) <= 0:
        raise ValidationError("Amount must be greater than 0.")


def validate_username_if_not_exists(_form, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError("Username already exists.")


def validate_username_if_exists(_form, username):
    user = User.query.filter_by(username=username.data).first()
    if not user:
        raise ValidationError("Username does not exist.")


def validate_email(_form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError("Email already exists.")


def validate_username_if_not_exists_update(_form, username):
    if current_user.username == username.data:
        return
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError("Username already exists.")


def validate_email_update(_form, email):
    if current_user.email == email.data:
        return
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError("Email already exists.")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=5, max=30),
            validate_username_if_not_exists,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(min=6, max=250),
            Email(message="Invalid email."),
            validate_email,
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            EqualTo("confirm_password", message="Passwords don't match."),
            Length(min=8, max=250),
        ],
    )
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=5, max=30),
            validate_username_if_exists,
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=250)]
    )
    submit = SubmitField("Login")


class UserUpdateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=5, max=30),
            validate_username_if_not_exists_update,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(min=6, max=250),
            Email(message="Invalid email."),
            validate_email_update,
        ],
    )
    profile_picture = FileField(
        "Profile Picture",
        validators=[FileAllowed(["jpg", "png"]), Length(min=5, max=250)],
    )
    submit = SubmitField("Update")


class IncomeForm(FlaskForm):
    inc_amount = StringField(
        "Amount", validators=[DataRequired(), validate_amount]
    )
    inc_sender = StringField(
        "Sender", validators=[DataRequired(), Length(max=120)]
    )
    inc_description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=500)]
    )
    inc_submit = SubmitField("Submit", name="form1_submit")


class ExpenseForm(FlaskForm):
    exp_payment_option = RadioField(
        "Payment Option",
        choices=[("Cash", "Cash"), ("Card", "Card"), ("Transfer", "Transfer")],
        validators=[DataRequired(), Length(max=60)],
    )
    exp_amount = StringField(
        "Amount", validators=[DataRequired(), validate_amount]
    )
    exp_description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=500)]
    )
    exp_submit = SubmitField("Submit", name="form2_submit")
