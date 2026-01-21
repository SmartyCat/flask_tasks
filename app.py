from flask import Flask, render_template, request, session, url_for, redirect, flash


DEBUG = True
SECRET_KEY = "dfvnl12zsdfv"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def index() -> str:
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        username, role = request.form.get("username"), request.form.get("role")
        session["username"] = username
        session["role"] = role
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
        role=session.get("role"),
    )


@app.route("/action")
def action() -> str:
    if "username" not in session:
        return redirect(url_for("login"))
    session["actions"] += 1
    flash("Action counted")
    return redirect(url_for("dashboard"))


@app.route("/admin")
def admin() -> str:
    if "username" in session and session.get("role") == "admin":
        return "Hello, admin"
    flash("Access denied", category="error")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout() -> str:
    if session:
        session.clear()
        return redirect(url_for("login"))
