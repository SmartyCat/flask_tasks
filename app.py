from flask import Flask, make_response, request

DEBUG = True
SECRET_KEY = "sdfvdf"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def index() -> str:
    username = request.form.get("username")
    if username:
        result = "Hello, {username}"
    else:
        result = "Hello, stranger"
    resp = make_response(result)
    resp.set_cookie("username", "Alex")

    return resp

