from flask import Flask, redirect, url_for
from main.routes import main

app = Flask(__name__)

app.register_blueprint(main, url_prefix="/")


@app.route("/")
def index() -> str:
    return redirect(url_for("main.hello"))
