from flask import Flask, render_template
from flask_orjson import OrjsonProvider

from example.extensions import db


def load_blueprints(flask_app):
    from example.rpc import rpc

    flask_app.register_blueprint(rpc)


def load_models(flask_app, flask_db):
    from example.models import clients

    flask_db.init_app(flask_app)

    with flask_app.app_context():
        flask_db.create_all()


def create_app():
    app = Flask(__name__, static_folder=None, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.secret_key = "secret"
    app.json = OrjsonProvider(app)

    load_models(app, db)
    load_blueprints(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
