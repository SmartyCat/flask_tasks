from flask import Flask

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return "Home page"


@app.route("/profile/<username>")
def profile(username: str) -> str:
    return f"Profile of {username}"


@app.route("/access/<int:age>")
def access(age: int) -> str:
    return "Access granted" if age >= 18 else "Access denied"


@app.route("/product/<name>/<int:price>")
def product(name: str, price: int) -> str:
    return f"Product {name} is {"expensive" if price > 1000 else "affordable"}"


if __name__ == "__main__":
    app.run(debug=True)
