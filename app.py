from flask import Flask, request, redirect, render_template, flash, session, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "gfbrgkj"


@app.route("/")
def home() -> str:
    if "person" in session:
        return redirect(url_for("dashboard"))
    return render_template("home.html")


@app.route("/form", methods=["GET", "POST"])
def form() -> str:
    if request.method == "POST":
        name, city = request.form.get("name"), request.form.get("city")
        if name and city and not session:
            session["person"] = (name, city)
            flash("Profile created", category="success")
            return redirect(url_for("dashboard"))
        elif name and city and session:
            session["person"] = (name, city)
            flash("Profile update", category="success")
            return redirect(url_for("dashboard"))
        else:
            flash("Fill all fields", category="error")
    return render_template("form.html")


@app.route("/dashboard")
def dashboard() -> str:
    if not session:
        flash("Access denied", category="error")
        return redirect(url_for("form"))
    return render_template("dashboard.html")


@app.route("/edit")
def edit() -> str:
    return redirect(url_for("form"))


@app.route("/logout")
def logout() -> str:
    session.clear()
    flash("Logged out", category="success")
    return redirect(url_for("home"))


@app.errorhandler(404)
def error(error) -> str:
    return render_template("error.html")
