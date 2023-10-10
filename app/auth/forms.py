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
    confirmed_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(min=8, max=250),
            EqualTo("password"),
        ],
    )
    submit = SubmitField("Reset Password")
