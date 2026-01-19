from flask import Flask, make_response, request, render_template, redirect, url_for

DEBUG = True
SECRET_KEY = "sdsfv"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    name = request.cookies.get("name")
    resp = make_response(
        render_template("index.html", name=name if name else "stranger")
    )
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            resp.set_cookie("name", name)
    return resp
