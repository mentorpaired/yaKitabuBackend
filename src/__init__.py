import os
from flask import Flask
from src.models import db
from src.user import user


def create_app(test_config=None):
    app: Flask = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    # Initializations
    db.app = app
    db.init_app(app)

    # Register blueprints

    app.register_blueprint(user)
    return app
