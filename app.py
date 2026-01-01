from flask import Flask, render_template

users = [
    {"id": 1, "name": "Kostya", "vip": True, "active": True},
    {"id": 2, "name": "Anna", "vip": False, "active": False},
    {"id": 3, "name": "Sergey", "vip": True, "active": False},
]

articles = [
    {"id": 1, "title": "Flask Basics", "user_id": 1, "published": True},
    {"id": 2, "title": "Jinja Tips", "user_id": 1, "published": True},
    {"id": 3, "title": "Draft Article", "user_id": 2, "published": False},
]

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/users")
def users_func() -> str:
    return render_template("users.html", users=users)


@app.route("/articles")
def articles_func() -> str:
    return render_template("articles.html", articles=articles)


@app.route("/user/<int:id>")
def user_func(id: int) -> str:
    result = [
        article["title"]
        for article in articles
        if id == article["user_id"] and article["published"]
    ]
    for user in users:
        if user["id"] == id:
            return render_template(
                "user.html", user=user, article=result if result else None
            )


@app.route("/article/<int:id>")
def art_func(id: int) -> str:
    for ar in articles:
        if ar["id"] == id:
            return render_template(
                "art.html",
                ar=ar,
                author=[user["name"] for user in users if ar["user_id"] == user["id"]][
                    0
                ],
            )
