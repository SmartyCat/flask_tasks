from flask import Flask, render_template

users = [
    {"name": "Kostya", "vip": True, "age": 30, "active": True},
    {"name": "Anna", "vip": False, "age": 16, "active": False},
    {"name": "Sergey", "vip": True, "age": 22, "active": False},
]

products = [
    {"name": "Hammer", "category": "tools", "price": 44, "in_stock": True},
    {"name": "Tomato", "category": "food", "price": 22, "in_stock": False},
    {"name": "Vacuum", "category": "electronics", "price": 5, "in_stock": True},
]

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return render_template("index.html")


@app.route("/users")
def users_function() -> str:
    return render_template("users.html", users=users)


@app.route("/products")
def products_function() -> str:
    return render_template("products.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)
