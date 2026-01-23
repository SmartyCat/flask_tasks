from flask import Flask, redirect, render_template, flash, request, session, url_for, g
import sqlite3
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from userlogin import UserLogin

DATABASE = "users.db"
DEBUG = True
SECRET_KEY = "sfkgm2;s;fv234"

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)


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
    if request.method == "POST":
        username, password = request.form.get("username"), generate_password_hash(
            request.form.get("password")
        )
        if not username or not password:
            flash("You didn't fill all the fills", category="error")
        elif (
            db.cursor()
            .execute("SELECT username FROM users WHERE username = ?", (username,))
            .fetchall()
        ):
            flash("The user exsists", category="error")
        else:
            db.cursor().execute(
                "INSERT INTO users(username,password) VALUES(?,?)", (username, password)
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
            .fetchall()
        )
        if user and check_password_hash(user[0][2], request.form.get("password")):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for("profile"))
        flash("Incorrect", category="error")
    return render_template("login.html")


@login_manager.user_loader
def load_user(user_id: int) -> tuple:
    db = get_db()
    return UserLogin().fromDB(user_id, db)


@app.route("/profile")
def profile() -> str:
    db = get_db()
    if session:
        return render_template(
            "profile.html",
            user=db.cursor().execute(
                "SELECT username FROM users WHERE id = ?", (session.get("_user_id"),)
            ).fetchone()[0],
        )
    return "Oops"


@app.route("/logout")
def logout() -> str:
    session.clear()
    return redirect(url_for("login"))
