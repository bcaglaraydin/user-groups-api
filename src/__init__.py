from flask import Flask
import os
from src.users import user
from src.groups import group
from src.database import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False)

    else:
        app.config.from_mapping(test_config)
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()
    app.register_blueprint(user)
    app.register_blueprint(group)
    return app
