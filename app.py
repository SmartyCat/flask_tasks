from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/profile")
def profile() -> str:
    return render_template("profile.html")


@app.route("/summary", methods=["POST"])
def summary() -> str:
    return render_template(
        "summary.html",
        age=int(request.form.get("age")),
        name=request.form.get("name"),
        city=request.form.get("city"),
    )


@app.route("/about")
def about() -> str:
    return render_template("about.html")
