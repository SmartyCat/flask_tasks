from flask import Blueprint, redirect, url_for, render_template, session
from main.forms import Form


main = Blueprint("main", __name__, template_folder="templates")


@main.route("/hello", methods=["GET", "POST"])
def hello() -> str:
    form = Form()
    if form.validate_on_submit():
        if not form.username.data:
            return redirect(url_for("main.hello"))
        else:
            session["username"] = form.username.data
            return redirect(url_for("main.result"))
    return render_template("hello.html", form=Form())


@main.route("/hello/result", methods=["GET", "POST"])
def result() -> str:
    return render_template("result.html", username=session.get("username"))
