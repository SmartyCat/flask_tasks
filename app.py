from flask import Flask, render_template, redirect, url_for, g, flash
import sqlite3
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_required,
    login_user,
)
from userlogin import UserLogin
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "users.db"
DEBUG = True
SECRET_KEY = "dfgbndgkob13dvblfv"


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
    with app.open_resource("users.sql", mode="r") as file:
        db.cursor().executescript(file.read())
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
    db = get_db()
    form = RegisterForm()
    if form.validate_on_submit():
        if (
            db.cursor()
            .execute("SELECT * FROM users WHERE username = ?", (form.username.data,))
            .fetchone()
        ):
            flash("The user already exists", category="error")
        else:
            db.cursor().execute(
                "INSERT INTO users(username, password) VALUES(?, ?)",
                (form.username.data, generate_password_hash(form.password.data)),
            )
            flash("The user was added", category="success")
            db.commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    db = get_db()
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    if form.validate_on_submit():
        user = (
            db.cursor()
            .execute("SELECT * FROM users WHERE username = ?", (form.username.data,))
            .fetchone()
        )
        if not user:
            flash("The user doesn't exist", category="error")
        else:
            userlogin = UserLogin().create(user)
            login_user(userlogin, remember=form.username.data)
            flash("Yeahh", category="success")
            return redirect(url_for("profile"))
    return render_template("login.html", form=form)


@login_manager.user_loader
def load_user(user_id: int) -> UserLogin:
    return UserLogin().fromDB(user_id, get_db())


@app.route("/profile")
def profile() -> str:
    return render_template("profile.html", username=current_user.username)


@app.route("/logout")
def logout() -> str:
    logout_user()
    return redirect(url_for("login"))
