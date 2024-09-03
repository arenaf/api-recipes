"""
File responsible for performing different operations with the user: creation, change of password,
login and logout, as well as verifying whether the user is currently logged in.
"""

from functools import wraps
from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from recipe_contents import db, login_manager
from recipe_contents.forms import RegisterUserForm, LoginForm, ChangePasswordForm
from recipe_contents.models import User

user_blueprint = Blueprint("user", __name__, template_folder="../templates")


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


# -------- New user registration --------
@user_blueprint.route('/new-user', methods=["GET", "POST"])
def register_new_user():
    if current_user.is_authenticated:
        return redirect(url_for("recipes.home"))
    form = RegisterUserForm()
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if not form.validate():
            flash("Invalid email.")
            return redirect(url_for("user.register_new_user"))
        if user != None:
            flash("This email already exists! Log in!")
            return redirect(url_for("user.login"))
        if request.form["password"] == request.form["check_password"]:
            final_pass = generate_password_hash(password=request.form["password"], method="pbkdf2:sha256",
                                                salt_length=8)
            new_user = User(
                name=request.form["name"],
                password=final_pass,
                email=request.form["email"]
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("recipes.home"))
        else:
            flash("Passwords do not match.")
    return render_template("register_user.html", form=form, current_user=current_user)


@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('recipes.home'))


@user_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("recipes.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form["email"]).first()
        if user == None:
            flash("There is no user registered with that email!")
            return redirect(url_for("user.login"))
        if check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("recipes.home"))
        else:
            flash("Incorrect password. Please try again.")
            return redirect(url_for("user.login"))
    return render_template("login.html", form=form, current_user=current_user)


# --------- Change Password --------
@user_blueprint.route('/change-password', methods=["GET", "POST"])
def change_password():
    if current_user.is_authenticated:
        return redirect(url_for("recipes.home"))
    form = ChangePasswordForm()
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if not form.validate():
            flash("Invalid email.")
            return redirect(url_for("user.change_password"))
        if user == None:
            flash("There is no user registered with that email!")
        if user != None:
            if request.form["password"] == request.form["check_password"]:
                final_pass = generate_password_hash(password=request.form["password"], method="pbkdf2:sha256",
                                                    salt_length=8)
                user.password = final_pass
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for("recipes.home"))
            else:
                flash("Passwords do not match.")
    return render_template("change_password.html", form=form, current_user=current_user)


# -------- Decorator Function --------
# Check that the user is logged in.
def user_logged(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Only logged in users have access to the site.")
            return redirect(url_for("user.login"))
        return function(*args, **kwargs)

    return decorated_function
