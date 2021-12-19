import os
import json

from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from src.models import db
from src.google import google_bp
from src.manage import create_tables
from src.auth import auth

load_dotenv()

def get_db_url():
    # Heroku hack
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:       
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://',1)
    return db_url
    

def create_app(test_config=None):
    app: Flask = Flask(__name__, instance_relative_config=True)
    
    secret_key = os.environ.get('SECRET_KEY')
    
    if secret_key is None:
        raise Exception("SECRET_KEY does not exist")
    
    db_url = get_db_url()
    
    if db_url is None:
        raise Exception("DATABASE_URL does not exist")
    
    if  not test_config:
        app.config.from_mapping(
            SECRET_KEY=secret_key,
            SQLALCHEMY_DATABASE_URI=db_url,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False
        )
    else:
       app.config.from_mapping(test_config)
       
    # Initializations.
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)

    # Register blueprints.
    app.register_blueprint(google_bp)
    
    # Customs command to create table.
    app.cli.add_command(create_tables)
    
    app.signup
    return app
