from flask import Flask, render_template, redirect, request, url_for, flash, g
import sqlite3

DATABASE = "tasks.db"
DEBUG = True
SECRET_KEY = "dfvdb"

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db() -> sqlite3.Connection:
    return sqlite3.connect(app.config["DATABASE"])


def create_db() -> None:
    db = connect_db()
    with app.open_resource("tasks.sql", mode="r") as f:
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
    db = get_db()
    return render_template(
        "index.html", tasks=db.cursor().execute("SELECT * FROM tasks").fetchall()
    )


@app.route("/add", methods=["POST", "GET"])
def add() -> str:
    db = get_db()
    if request.method == "POST":
        title, article = request.form.get("title"), request.form.get("article")
        if title and article:
            flash("The new tasks was added", category="success")
            db.cursor().execute(
                "INSERT INTO tasks(title, article) VALUES(?, ?)", (title, article)
            )
            db.commit()
            return redirect(url_for("index"))
        else:
            flash("You must fill all the fills", category="error")
    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id: int) -> str:
    db = get_db()
    db.cursor().execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    if db.cursor().rowcount:
        flash("The article was success deleted", category="success")
    else:
        flash("The article doesn't exist", category="error")
    return redirect(url_for("index"))
