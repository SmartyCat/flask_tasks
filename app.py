from flask import Flask, render_template, request, redirect, session, g, url_for, flash
import sqlite3
from flask_login import LoginManager, current_user, login_required, login_user
from userlogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "users.db"
DEBUG = True
SECRET_KEY = "sfkvjkf789kmsfm1"

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)


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
    db = get_db()
    if request.method == "POST":
        username, password = request.form.get("username"), generate_password_hash(
            request.form.get("password")
        )
        if not username or not password:
            flash("You must fill all the fills", category="error")
        elif (
            db.cursor()
            .execute("SELECT * FROM users WHERE username = ?", (username,))
            .fetchone()
        ):
            flash("The user already exists", category="error")
        else:
            db.cursor().execute(
                "INSERT INTO users(username, password) VALUES(?, ?)",
                (username, password),
            )
            db.commit()
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
        print(user)
        if not user:
            flash("The user doesn't exist", category="error")
        elif not check_password_hash(user[2], request.form.get("password")):
            flash("Incorrect password", category="error")
        else:
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for("profile"))
    return render_template("login.html")


@login_manager.user_loader
def load_user(user_id: int) -> UserLogin:
    return UserLogin().fromDB(user_id, get_db())


@app.route("/profile")
@login_required
def profile() -> str:
    return render_template("profile.html", user=current_user.user[1])


@app.route("/logout")
def logout() -> None:
    session.clear()
    return redirect(url_for("login"))
