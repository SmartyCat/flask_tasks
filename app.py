from flask import Flask, render_template

users = [
    {"id": 1, "name": "Kostya", "vip": True, "active": True},
    {"id": 2, "name": "Anna", "vip": False, "active": False},
    {"id": 3, "name": "Sergey", "vip": True, "active": False},
    {"id": 4, "name": "Ivan", "vip": False, "active": True},
]


app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/users")
def users_func() -> str:
    return render_template("users.html", users=users)


@app.route("/users/active")
def users_active_func() -> str:
    return render_template(
        "users.html", users=[user for user in users if user["active"]]
    )


@app.route("/users/vip")
def users_vip_func() -> str:
    return render_template("users.html", users=[user for user in users if user["vip"]])
