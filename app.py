from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/result", methods=["POST"])
def result() -> str:
    return render_template(
        "result.html",
        name=request.form.get("name"),
        age=int(request.form.get("age")),
        sex=request.form.get("sex"),
    )
