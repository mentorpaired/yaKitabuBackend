import re
import uuid
from datetime import datetime

import validators
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended.utils import get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

from src.google import get_user_info
from src.models import UserLogin, UserProfile, db
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLIT



user_bp = Blueprint('user', __name__, url_prefix='/api')


@user_bp.post('/login/user/signup')
@swag_from('./docs/signup/user.yml')
def signup():
    """Endpoint for user signup

    Returns:
        json: user's information
    """
    
    if 'first_name' not in request.json:
        return jsonify({
            'error': "first_name is missing from request"
        }), HTTP_400_BAD_REQUEST
        
    if 'last_name' not in request.json:
        return jsonify({
            'error': "last_name is missing from request"
        }), HTTP_400_BAD_REQUEST
    
    if 'email' not in request.json:
        return jsonify({
            'error': "email is missing from request"
        }), HTTP_400_BAD_REQUEST
    
    if 'password' not in request.json:
        return jsonify({
            'error': "password is missing from request"
        }), HTTP_400_BAD_REQUEST
        
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    
    if not validators.email(email):
        return jsonify({
            'error': "email is invalid"
        }), HTTP_400_BAD_REQUEST
        
    if not validate_password_complexity(password):
        return jsonify({
            'error': "password should be at least 8 characters long and it contain minimum one lower case, one uppercase and one special character"
        }), HTTP_400_BAD_REQUEST
        
    # Check if email is taken    
    if UserProfile.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error': "account with this email already exists"
        }), HTTP_409_CONFLIT
        
    password_hash = generate_password_hash(password)
    
    new_user = UserProfile(
        id=uuid.uuid4(),
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    # user Login
    user_login = UserLogin(
        id=uuid.uuid4(),
        google_login=True,
        is_active=True,
        password_hash=password_hash,
        user_profile_id=new_user.id,
        last_login=datetime.now()
    )

    db.session.add(new_user)
    db.session.add(user_login)
    db.session.commit()
    
    # TODO: Create access and refresh tokens.
    
    user_info = get_user_info(new_user.id)
    
    return jsonify(user_info), HTTP_201_CREATED



@user_bp.post('/login/user')
@swag_from('./docs/login/user.yml')
def login():
    """Login endpoint

    Returns:
        json: user's information
    """
    
    if 'email' not in request.json:
        return jsonify({
            'error': "email cannot be blank"
        }), HTTP_400_BAD_REQUEST
        
    if 'password' not in request.json:
        return jsonify({
            'error': "password is missing"
        }), HTTP_400_BAD_REQUEST
    
    email = request.json['email']
    password = request.json['password']
    
    if not validators.email(email):
        return jsonify({
            'error': "email is invalid"
        }), HTTP_400_BAD_REQUEST

    # check if user exists
    usr = UserProfile.query.filter_by(email=email).first()
    if not usr:
        return jsonify({
            'error': "user is invalid"
        }), HTTP_401_UNAUTHORIZED
    
    user_login = UserLogin.query.filter_by(user_profile_id=usr.id).first()
    
    
    # Check if password is correct
    is_valid_pass = check_password_hash(
        pwhash=user_login.password_hash,
        password=password)
    if is_valid_pass:
        
        # TODO: Create access and refresh tokens.
        
        user_info =  get_user_info(usr.id)
        
        # updates last login
        user_login.last_login = datetime.now()   
        user_login.google_login =  False
        db.session.commit()
        
        return jsonify(user_info), HTTP_200_OK
    
    return jsonify({'error':'incorrect password'}), HTTP_401_UNAUTHORIZED


def validate_password_complexity(password):
    """Checks password complexity
    
    Passwords:
        Should have at least one number.
        Should have at least one uppercase and one lowercase character.
        Should have at least one special symbol.
        Should be at least 8 characters long.
        
    Args:
        password (string): [description]

    Returns:
        boolean: true if the conditions are met, false otherwise.
    """
    pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&.,()]{8,}$")
    return re.search(pattern, password)
