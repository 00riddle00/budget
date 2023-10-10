from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import RadioField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from ..models import User


class UserUpdateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=5, max=30),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(min=6, max=250),
            Email(message="Invalid email."),
        ],
    )
    profile_picture = FileField(
        "Profile Picture",
        validators=[FileAllowed(["jpg", "png"]), Length(min=5, max=250)],
    )
    submit = SubmitField("Update")

    def validate_username(self, field):
        if current_user.username == field.data:
            return
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Username already exists.")

    def validate_email_update(self, field):
        if current_user.email == field.data:
            return
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email already exists.")


class IncomeForm(FlaskForm):
    inc_amount = StringField("Amount", validators=[DataRequired()])
    inc_sender = StringField(
        "Sender", validators=[DataRequired(), Length(max=120)]
    )
    inc_description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=500)]
    )
    inc_submit = SubmitField("Submit", name="form1_submit")

    def validate_inc_amount(self, field):
        if not field.data.isdigit():
            raise ValidationError("Amount must be a number.")
        if float(field.data) <= 0:
            raise ValidationError("Amount must be greater than 0.")


class ExpenseForm(FlaskForm):
    exp_payment_option = RadioField(
        "Payment Option",
        choices=[("Cash", "Cash"), ("Card", "Card"), ("Transfer", "Transfer")],
        validators=[DataRequired(), Length(max=60)],
    )
    exp_amount = StringField("Amount", validators=[DataRequired()])
    exp_description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=500)]
    )
    exp_submit = SubmitField("Submit", name="form2_submit")

    def validate_exp_amount(self, field):
        if not field.data.isdigit():
            raise ValidationError("Amount must be a number.")
        if float(field.data) <= 0:
            raise ValidationError("Amount must be greater than 0.")
