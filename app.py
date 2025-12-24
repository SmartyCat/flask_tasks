from flask import Flask, render_template

users = [
    {"id": 1, "name": "Kostya", "vip": True, "age": 30, "active": True},
    {"id": 2, "name": "Anna", "vip": False, "age": 16, "active": False},
    {"id": 3, "name": "Sergey", "vip": True, "age": 22, "active": False},
    {"id": 4, "name": "Ivan", "vip": False, "age": 19, "active": True},
]

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/users")
def users_function() -> str:
    for user in users:
        result = []
        if user["vip"]:
            result.append("VIP")
        if user["active"]:
            result.append("ACTIVE")
        if not user["active"]:
            result.append("INACTIVE")
        if user["age"] < 18:
            result.append("UNDERAGE")
        user["status"] = " ".join(result)
    return render_template("/users.html", users=users)
