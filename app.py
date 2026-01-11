from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "sdfvsfv"


@app.route("/", methods=["POST", "GET"])
def home() -> str:
    name = request.form.get("name")
    if request.method == "POST":
        if name:
            flash(f"Hello, {name}!", category="success")
        else:
            flash("Name is required",category="error")
    return render_template("home.html")
