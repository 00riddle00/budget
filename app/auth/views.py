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
from PIL import Image
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db
from ..main.forms import LoginForm, RegisterForm, UserUpdateForm
from ..main.views import load_user_picture
from ..models import User
from . import auth


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
