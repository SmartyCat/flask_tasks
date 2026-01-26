from flask import Flask, render_template, request, g, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from userlogin import UserLogin

DATABASE = "users.db"
DEBUG = True
SECRET_KEY = "sfjvhdfll;134sfv"

app = Flask(__name__)
app.config.from_object(__name__)


login_manger = LoginManager(app)
login_manger.login_view = "login"
login_manger.login_message = "You need to enter in the system"
login_manger.login_message_category = "error"


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
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username, password, check_password = (
            request.form.get("username"),
            request.form.get("password"),
            request.form.get("check"),
        )
        if not username or not password or not check_password:
            flash("You must fill all the fills", category="error")
        elif (
            db.cursor()
            .execute("SELECT * FROM users WHERE username = ?", (username,))
            .fetchone()
        ):
            flash("The user already exists", category="error")
        elif password != check_password:
            flash("The passwords don't match", category="error")
        else:
            db.cursor().execute(
                "INSERT INTO users(username,password) VALUES(?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            flash("Success", category="success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    db = get_db()
    if request.method == "POST":
        user = (
            db.cursor()
            .execute(
                "SELECT * FROM users WHERE username = ?",
                (request.form.get("username"),),
            )
            .fetchone()
        )
        if not user:
            flash("The user doesn't exist", category="error")
        elif not check_password_hash(user[2], request.form.get("password")):
            flash("Incorrect password", category="error")
        else:
            user_login = UserLogin().create(user)
            rm = True if request.form.get("remember") else False
            login_user(user_login, remember=rm)
            flash("Success", category="success")
            return redirect(url_for("profile"))
    return render_template("login.html")


@login_manger.user_loader
def load_user(user_id: int) -> UserLogin:
    return UserLogin().fromDB(user_id, get_db())


@app.route("/profile")
@login_required
def profile() -> str:
    return render_template("profile.html", user=current_user.user)


@app.route("/logout")
def logout() -> str:
    logout_user()
    return redirect(url_for("login"))
