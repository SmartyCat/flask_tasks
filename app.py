from flask import Flask, render_template, request, flash

app = Flask(__name__)
names = []
app.config["SECRET_KEY"] = "dfkbjndjgfo"


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    name = request.form.get("name")
    if name:
        names.append(name)
    if request.method == "POST":
        if name:
            flash("Success", category="success")
        else:
            flash("Error", category="error")
    return render_template("home.html", name=name)


@app.route("/profile")
def profile() -> str:
    return render_template("profile.html", name=names[-1])


@app.errorhandler(404)
def error(error) -> str:
    return render_template("error.html")
