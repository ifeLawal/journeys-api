from flask import Flask

from connecting import DATABASE
from journeys.api.utils import create_database


def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        from models import db

        url = create_database()  # noqa F841

        db.init_app(app)
        db.create_all()

        from journeys.api import api
        from journeys.api.routes import data

        app.register_blueprint(data)
        app.register_blueprint(api)

        return app
