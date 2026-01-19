from flask import Flask, make_response


DEBUG = True
SECRET_KEY = "dfbdgfb"


app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def hello() -> str:
    resp = make_response("Hello, Flask!")
    resp._status_code = 200
    resp.headers["X-App-Name"] = "FlaskTraining"

    return resp
