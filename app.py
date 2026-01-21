from flask import Flask, session, render_template, redirect, request, flash, url_for


SECRET_KEY = "SJFVHFDIU8234SDVK23"
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def index() -> str:
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("error", category="error")
        else:
            session["username"] = username
            session["actions"] = 0
            return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/dashboard")
def dashboard() -> str:
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        actions=session.get("actions"),
    )


@app.route("/action")
def action() -> str:
    if "username" not in session:
        return redirect(url_for("login"))
    session["actions"] += 1
    flash("Action counted", category="success")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout() -> str:
    if "username" not in session:
        return redirect(url_for("login"))
    session.clear()
    flash("Logged out", category="success")
    return redirect(url_for("login"))
