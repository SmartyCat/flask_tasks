from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html", username="Kostya", is_auth=False)


if __name__ == "__main__":
    app.run(debug=True)
