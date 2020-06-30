from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route("/sidebar")
    def sidebar():
        return render_template("start.html")

    return app
