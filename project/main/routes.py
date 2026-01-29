from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/hello")
def hello() -> str:
    return "Hello form blueprint"
