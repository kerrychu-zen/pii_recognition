from flask import Flask, render_template

app = Flask(__name__)


@app.route("/sidebar")
def index():
    return render_template("start.html")
