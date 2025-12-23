from flask import Flask

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return "Welcome to the app"


@app.route("/hello/<username>")
def hello(username: str) -> str:
    return f"Hello, {username}"


@app.route("/age/<int:age>")
def age(age: int) -> str:
    return "Access granted" if age >= 18 else "Access denied"


@app.route("/product/<name>/<int:price>")
def product(name: str, price: int) -> str:
    if price < 20:
        return f"Product {name} is cheap"
    elif price > 100:
        return f"Product {name} is expensive"
    else:
        return f"Product {name} is affortable"


@app.route("/user/<username>/<int:posts>")
def user(username: str, posts: int) -> str:
    return f"{username is {'active' if posts >= 5 else 'inactive'}}"


if __name__ == "__main__":
    app.run(debug=True)
