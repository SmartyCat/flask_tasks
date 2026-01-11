from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "sdfjbkfghbdlf"


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    if "name_age" in session:
        return redirect(url_for("profile"))

    elif request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        session["name_age"] = (name, age)
        return redirect(url_for("profile", name=name, age=age))
    return render_template("home.html")


@app.route("/profile")
def profile() -> str:
    return render_template(
        "profile.html", name=session["name_age"][0], age=int(session["name_age"][1])
    )


@app.route("/clear")
def cleaar() -> str:
    session.clear()
    return redirect(url_for("home"))
