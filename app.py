from flask import render_template, request, g, flash, Flask, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "users.db"
DEBUG = True
SECRET_KEY = "sdfng1l"

app = Flask(__name__)
app.config.from_object(__name__)


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
    return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    db = get_db()
    if request.method == "POST":
        username, password, email = (
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
            request.form.get("email"),
        )
        if username and password and email:
            db.cursor().execute(
                "INSERT INTO users(username,password,email) VALUES(?, ?, ?)",
                (username, password, email),
            )
            flash("The user was added", category="success")
            db.commit()
            return redirect(url_for("users"))
        else:
            flash("Error", category="error")
    return render_template("register.html")


@app.route("/users")
def users() -> str:
    db = get_db()
    return render_template(
        "users.html", u=db.cursor().execute("SELECT * FROM users").fetchall()
    )
