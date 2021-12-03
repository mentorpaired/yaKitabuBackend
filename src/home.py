
from google.auth import jwt
from flask import Blueprint, jsonify, request

home = Blueprint('home', __name__, url_prefix='/')

# Route for heroku testing
@home.get('hi')
def hello():
    return jsonify({'hello':'world'})
