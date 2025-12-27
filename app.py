from flask import Flask, render_template, url_for

users = [
    {"id": 1, "name": "Kostya", "vip": True, "active": True},
    {"id": 2, "name": "Anna", "vip": False, "active": False},
    {"id": 3, "name": "Sergey", "vip": True, "active": False},
]

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return render_template("index.html")


@app.route("/users")
def users_function() -> str:
    return render_template("users.html", users=users)


@app.route("/user/<int:id>")
def user_function(id: int) -> str:
    for user in users:
        if user["id"] == id:
            return render_template("user.html", user=user)
    return render_template("user.html",user="")
