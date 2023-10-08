import os
import secrets

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from PIL import Image
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, mail
from ..main.forms import LoginForm, RegisterForm, UserUpdateForm
from ..main.views import load_user_picture
from ..models import User
from . import auth
from .forms import PasswordResetForm, RequestPasswordResetForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Takes the data from the form.
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Checks if the user exists.
        user = User.query.filter_by(username=username).first()

        # If the user doesn't exist or the password is incorrect, redirects to the login page.
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))

        # Logs in the user.
        login_user(user)

        return redirect(url_for("main.index"))

    else:
        picture_url = load_user_picture()
        return render_template(
            "login.html", form=form, picture_url=picture_url
        )


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    # Takes the data from the form.
    if form.validate_on_submit():
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Creates a new user
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method="scrypt"),
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(username=username).first()
            login_user(user)
        except Exception as e:
            db.session.rollback()  # Rollback changes if there's an error
            flash(f"An error occurred while registering: {e}")
            return redirect(url_for("auth.signup"))

        return redirect(url_for("main.budget"))
    else:
        picture_url = load_user_picture()
        return render_template(
            "signup.html", form=form, picture_url=picture_url
        )


@auth.route("/logout")
def logout():
    logout_user()
    picture_url = load_user_picture()
    return render_template("index.html", picture_url=picture_url)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Slaptažodžio atnaujinimo užklausa",
        sender="ptua6.real4dmin@gmail.com",
        recipients=[user.email],
    )
    msg.body = (
        f"Norėdami atnaujinti slaptažodį, paspauskite nuorodą: "
        f"{url_for('auth.reset_token', token=token, _external=True)} "
        f"Jei jūs nedarėte šios užklausos, nieko nedarykite ir "
        f"slaptažodis nebus pakeistas."
    )
    mail.send(msg)


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RequestPasswordResetForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash(
                "Jums išsiųstas el. laiškas su slaptažodžio atnaujinimo instrukcijomis.",
                "info",
            )
            return redirect(url_for("auth.login"))
    except Exception as e:
        flash(f"An error occurred while registering: {e}")
        return redirect(url_for("auth.reset_request"))
    return render_template(
        "reset_request.html", title="Reset Password", form=form
    )


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Užklausa netinkama arba pasibaigusio galiojimo", "warning")
        return redirect(url_for("reset_request"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.slaptazodis.data, method="scrypt"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Tavo slaptažodis buvo atnaujintas! Gali prisijungti", "success")
        return redirect(url_for("auth.login"))
    return render_template(
        "reset_token.html", title="Reset Password", form=form
    )


@auth.route("/profile", methods=["GET", "POST"])
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
        return redirect(url_for("auth.user_update"))
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
