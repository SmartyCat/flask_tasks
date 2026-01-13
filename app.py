from flask import (
    Flask,
    url_for,
    redirect,
    request,
    render_template,
    flash,
    session,
    abort,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "dgkjnb"


@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        name, age = request.form.get("name"), int(request.form.get("age"))
        if not name:
            flash("You don't write your name", category="error")
        elif age < 16:
            flash("You are too young", category="error")
        else:
            if "user" in session:
                flash("Successful updating", category="success")
            else:
                flash("You are successful login", category="success")
            session["user"] = (name, age)
            return redirect(url_for("profile", name=session["user"][0]))
    return render_template("login.html")


@app.route("/profile/<name>")
def profile(name: str) -> str:
    if "user" not in session or session["user"][0] != name:
        abort(401)
    return render_template("profile.html")


@app.route("/logout")
def logout() -> str:
    session.clear()
    flash("Logged out successfully", category="success")
    return redirect(url_for("home"))


@app.errorhandler(404)
def base_error(error) -> str:
    return render_template("error.html")

