from flask import Flask, render_template, g
import sqlite3


DATABASE = "test.db"
SECRET_KEY = "sfdf"
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    return conn


def create_db() -> None:
    db = connect_db()
    with app.open_resource("test.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db() -> None:
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()


@app.teardown_appcontext
def close_db(error) -> None:
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/")
def index() -> str:
    db = connect_db()
    return render_template("index.html", users=db.cursor().fetchall())
