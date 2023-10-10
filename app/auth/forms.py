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


class RequestPasswordResetForm(FlaskForm):
    email = StringField(
        "El. paštas",
        validators=[DataRequired(), Length(min=6, max=250), Email()],
    )

    submit = SubmitField("Gauti")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError(
                "Nėra paskyros, registruotos šiuo el. pašto adresu. Registruokitės."
            )


class PasswordResetForm(FlaskForm):
    slaptazodis = PasswordField(
        "Slaptažodis", validators=[DataRequired(), Length(min=8, max=250)]
    )
    patvirtintas_slaptazodis = PasswordField(
        "Pakartokite slaptažodį",
        validators=[
            DataRequired(),
            Length(min=8, max=250),
            EqualTo("slaptazodis"),
        ],
    )
    submit = SubmitField("Atnaujinti Slaptažodį")
