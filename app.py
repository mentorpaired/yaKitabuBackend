import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

a = app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return "<p> Hello World.! </p>"
    