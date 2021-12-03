import os

from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from src.models import db
from src.google import google_bp
from src.home import home
from src.config.config import TestingConfig

load_dotenv()

def create_app(test_config=None):
    app: Flask = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False
        )
    else:
       app.config.from_mapping(test_config)

       
    # Initializations
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)

    # Register blueprints
    app.register_blueprint(google_bp)
    app.register_blueprint(home)
    return app
