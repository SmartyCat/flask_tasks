from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/hello", methods=["POST"])
def hello() -> str:
    return render_template("hello.html", name=request.form["name"])
