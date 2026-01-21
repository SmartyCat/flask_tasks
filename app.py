from flask import Flask, render_template, redirect, session, url_for, request

SECRET_KEY = "sdkvj12e23sld"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    if "count" not in session:
        session["count"] = 0
    if request.method == "POST":
        session["count"] += 1
        return redirect(url_for("index"))
    return render_template("index.html", count=session["count"])
