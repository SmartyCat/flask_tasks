from flask import Flask, render_template

app = Flask(__name__)


users = [
    {"name": "Kostya", "vip": True},
    {"name": "Anna", "vip": False},
    {"name": "Sergey", "vip": True},
]


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/users")
def users_func() -> str:
    return render_template("users.html", users=users)
