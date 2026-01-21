from flask import Flask, render_template, request, session, url_for, redirect, flash

SECRET_KEY = "sdvjdfvl12w4d0sfvd34"
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def index() -> str:
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login() -> str:
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Error", category="error")
        else:
            session["username"] = username
            return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/profile")
def profile() -> str:
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("profile.html", username=session["username"])


@app.route("/logout")
def logout() -> str:
    session.clear()
    return redirect(url_for("login"))
