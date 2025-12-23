from flask import Flask

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return "Hello from Flask"


@app.route("/about")
def about() -> str:
    return "About page"


@app.route("/user/<name>/<int:age>")
def user(name: str, age: int) -> str:
    return f"User {name}, age {age}"


if __name__ == "__main__":
    app.run(debug=True)
