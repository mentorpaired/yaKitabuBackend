import os
import json

from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flasgger import Swagger
import cloudinary

from src.models import db
from src.google import google_bp
from src.manage import create_tables
from src.config.swagger import  template,swagger_config

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
    
    
    issuer = os.environ.get('TOKEN_ISSUER')
    if issuer is None:
        raise Exception("TOKEN_ISSUER does not exist")
    

    client = os.environ.get('CLIENT_ID')
    if client is None:
        raise Exception("CLIENT_ID does not exist")
    
    
    cld_name = os.environ.get('CLD_CLOUD_NAME')
    cld_api_key = os.environ.get('CLD_CLOUDINARY_API_KEY')
    cld_secret = os.environ.get('CLD_CLOUDINARY_SECRET')
    
    # Check if any of the cloudinary envs are not set.
    if not (cld_name and cld_api_key and cld_secret):
         raise Exception("One or more Cloudinary credentials are missing")
     
    cloudinary.config(cloud_name = cld_name, api_key=cld_api_key, 
                      api_secret=cld_secret)
    
    
    if  not test_config:
        app.config.from_mapping(
            SECRET_KEY=secret_key,
            SQLALCHEMY_DATABASE_URI=db_url,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False,
            SWAGGER={
                'title': 'Yakitabu P2P Book Loan API',
                'uiversion':3
            },
        )
    else:
       app.config.from_mapping(test_config)
       
    # Initializations.
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)
    
    # swagger configuration
    Swagger(app=app, config=swagger_config,template=template)

    # Register blueprints.
    app.register_blueprint(google_bp)
    
    # Customs command to crate table.
    app.cli.add_command(create_tables)
    
    return app
