from flask import Flask, render_template, redirect, g, request, url_for
import sqlite3

DATABASE = "test.db"
DEBUG = True
SECRET_KEY = "sfvsf"

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db() -> sqlite3.Connection:
    return sqlite3.connect(app.config["DATABASE"])


def create_db() -> None:
    db = connect_db()
    with app.open_resource("test.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db() -> sqlite3.Connection:
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error) -> None:
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/")
def index() -> str:
    db = get_db()
    return render_template(
        "index.html", users=db.cursor().execute("SELECT * FROM users").fetchall()
    )


@app.route("/add", methods=["GET", "POST"])
def add() -> str:
    db = get_db()
    if request.method == "POST":
        name, age = request.form.get("name"), request.form.get("age")
        db.cursor().execute("INSERT INTO users(name, age) VALUES(?, ?)", (name, age))
        db.commit()
        db.close()
        return redirect(url_for("index"))
    return render_template("add.html")
