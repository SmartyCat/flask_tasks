from flask import Flask, render_template, url_for


app = Flask(__name__)


users = [
    {"id": 1, "name": "Kostya", "vip": True, "active": True},
    {"id": 2, "name": "Anna", "vip": False, "active": False},
    {"id": 3, "name": "Sergey", "vip": True, "active": False},
    {"id": 4, "name": "Ivan", "vip": False, "active": True},
]

posts = [
    {
        "id": 1,
        "title": "Flask basics",
        "user_id": 1,
        "published": True,
    },
    {
        "id": 2,
        "title": "Jinja templates",
        "user_id": 1,
        "published": True,
    },
    {
        "id": 3,
        "title": "Draft post",
        "user_id": 2,
        "published": False,
    },
    {
        "id": 4,
        "title": "Advanced Flask",
        "user_id": 3,
        "published": True,
    },
    {
        "id": 5,
        "title": "Hidden thoughts",
        "user_id": 3,
        "published": False,
    },
]


@app.route("/")
def main() -> str:
    return render_template("index.html")


@app.route("/users")
def users_function() -> str:
    return render_template("users.html", users=users)


@app.route("/user/<int:id>")
def user_function(id: int) -> str:
    result = [post["title"] for post in posts if id == post["user_id"]]
    for user in users:
        if id == user["id"]:
            return render_template("user.html", id=id, user=user, posts=result)


@app.route("/posts")
def posts_function() -> str:
    return render_template("posts.html", posts=posts)


@app.route("/post/<int:id>")
def post_function(id: int) -> str:
    for post in posts:
        if id == post["id"]:
            return render_template("post.html", post=post, users=users)
