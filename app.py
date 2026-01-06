from flask import Flask, render_template, flash, request


app = Flask(__name__)

app.config["SECRET_KEY"] = "dbdgb"


@app.route("/",methods=["GET","POST"])
def home() -> str:
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            flash (f"Hello, {name}!")
        else:
            flash ("Name is reqired!")
    return render_template("home.html")
