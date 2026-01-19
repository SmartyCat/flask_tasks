from flask import Flask, make_response, request


DEBUG = True
SECRET_KEY = "sdfvfsv"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def index() -> str:
    visits = request.cookies.get("visits")
    if not visits:
        resp = make_response("Welcome! This your first visit.")
        resp.set_cookie("visits", "1")
    else:
        resp = make_response(f"You have visited this page {visits} times")
        visits = int(visits)
        visits += 1
        resp.set_cookie("visits", str(visits))
    return resp
