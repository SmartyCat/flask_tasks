from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/")
def main() -> str:
    return "Hello from Flask"


@app.route("/about")
def about() -> str:
    return "About page"
