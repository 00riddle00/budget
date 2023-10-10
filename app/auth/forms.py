from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)

from ..models import User


class LoginForm(FlaskForm):
    """User's login form."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=5, max=30),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=250)]
    )
    submit = SubmitField("Login")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError("Username does not exist.")


class RegisterForm(FlaskForm):
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
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=250),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Username already exists.")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email already exists.")


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Length(min=6, max=250), Email()],
    )
    submit = SubmitField("Reset Password")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with this email address. Please "
                "register first."
            )


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=8, max=250)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Reset Password")
