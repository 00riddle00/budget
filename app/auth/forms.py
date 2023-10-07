from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from ..models import User


class RequestPasswordResetForm(FlaskForm):
    email = StringField("El. paštas", validators=[DataRequired(), Email()])
    submit = SubmitField("Gauti")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError(
                "Nėra paskyros, registruotos šiuo el. pašto adresu. Registruokitės."
            )


class PasswordResetForm(FlaskForm):
    slaptazodis = PasswordField("Slaptažodis", validators=[DataRequired()])
    patvirtintas_slaptazodis = PasswordField(
        "Pakartokite slaptažodį",
        validators=[DataRequired(), EqualTo("slaptazodis")],
    )
    submit = SubmitField("Atnaujinti Slaptažodį")
