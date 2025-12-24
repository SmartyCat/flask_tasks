from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("templates/index.html", title="Home", message="Hello from Flask")


if __name__ == "__main__":
    app.run(debug=True)
