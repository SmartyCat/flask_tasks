from flask import Flask

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return "Hello from Flask"


@app.route("/about")
def about() -> str:
    return "About page"


@app.route(f"/user/<username>")
def profile(username: str) -> str:
    return f"hello,{username}"


if __name__ == "main":
    app.run(debug=True)
