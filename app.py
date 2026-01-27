from flask import Flask, render_template, g, redirect, url_for, flash
import sqlite3
from loginform import RegisterForm, LoginForm
from userlogin import UserLogin
from flask_login import (
    login_user,
    logout_user,
    current_user,
    LoginManager,
    login_required,
)
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "users.db"
DEBUG = True
SECRET_KEY = "fgjbfog12sdf"

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "You need autho"
login_manager.login_message_category = "error"


def connect_db() -> sqlite3.Connection:
    return sqlite3.connect(app.config["DATABASE"])


def create_db() -> None:
    db = connect_db()
    with app.open_resource("users.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db() -> sqlite3.Connection:
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error: Exception | None) -> None:
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/")
def index() -> str:
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    db = get_db().cursor()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.check_password.data:
            flash("Incorrect password", category="error")
        elif db.execute(
            "SELECT * FROM users WHERE username = ?", (form.username.data,)
        ).fetchone():
            flash("The user already exists", category="error")
        else:
            db.execute(
                "INSERT INTO users(username, password) VALUES(?, ?)",
                (form.username.data, generate_password_hash(form.password.data)),
            )
            get_db().commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    db = get_db().cursor()
    form = LoginForm()
    if form.validate_on_submit():
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (form.username.data,)
        ).fetchone()
        if not user:
            flash("The user doesn't exist", category="error")
        elif not check_password_hash(user[2], form.password.data):
            flash("Incorrect password", category="error")
        else:
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for("profile"))
    return render_template("login.html", form=form)


@login_manager.user_loader
def load_user(user_id: int) -> UserLogin:
    return UserLogin().fromDB(user_id, get_db())


@app.route("/profile")
@login_required
def profile() -> str:
    return render_template("profile.html", user=current_user.username)


@app.route("/logout")
def logout() -> str:
    logout_user()
    return redirect(url_for("login"))
