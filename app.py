from flask import Flask, render_template, redirect, request, url_for, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "dfkdk"


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    if "person" in session:
        return redirect(url_for("profile"))
    elif request.method == "POST":

        name, age, sex, hobbie = (
            request.form.get("name"),
            int(request.form.get("age")),
            request.form.get("sex"),
            request.form.getlist("hobbie"),
        )
        if not name:
            flash("Name is required", category="error")
        elif age < 13:
            flash("You are too young", category="error")
        if name and age > 13 and sex and hobbie:
            session["person"] = (name, age, sex, hobbie)
            return redirect(url_for("profile"))
        else:
            flash("Please fill the form first", category="error")
    return render_template("home.html")


@app.route("/profile")
def profile() -> str:
    return render_template("profile.html")


@app.route("/logout")
def logout() -> str:
    session.clear()
    return redirect(url_for("home"))
