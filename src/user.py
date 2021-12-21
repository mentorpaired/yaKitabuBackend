from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_201_CREATED

import validators
import logging
import datetime
import  uuid

from os import access
from src.models import UserLogin, UserProfile, db
from src.google import get_user_info

user_bp = Blueprint("auth", __name__, url_prefix='/api')

@user_bp.post('/login/user/signup')
def signup():
    
    if 'first_name' not in request.json:
        return jsonify({'error': "'first_name' is not available in db"}), HTTP_400_BAD_REQUEST
    
    if 'last_name' not in request.json:
        return jsonify({'error': "'last_name' is not available in db"}), HTTP_400_BAD_REQUEST
    
    if 'email' not in request.json:
        return jsonify({'error': "'email' is not available in db"}), HTTP_400_BAD_REQUEST
    
    if 'password' not in request.json:
        return jsonify({'error': "'password' is not available in db"}), HTTP_400_BAD_REQUEST
    
    if 'picture_url' not in request.json:
        return jsonify({'error': "'picture_url' is not available in db"}), HTTP_400_BAD_REQUEST
    
    first_name=request.json['first_name']
    last_name=request.json['last_name']
    email=request.json['email']
    password=request.json['password']
    picture_url=request['picture_url']
    
    #check for length of password
    if len(password)<6:
        return jsonify({'error': 'Password is too short'}), HTTP_400_BAD_REQUEST
    
    #check for email validity
    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), HTTP_400_BAD_REQUEST
    
    #check if email exists in the models.py(db)
    if UserProfile.query.filter_by(email=email).first() is not None: 
        return jsonify({'error': 'Email is taken'}), HTTP_409_CONFLICT
    
    #check if first name exists in models.py(db)
    if UserProfile.query.filter_by(first_name=first_name).first() is not None: 
        return jsonify({'error': 'First name is taken'}), HTTP_409_CONFLICT
    
    #check if last name exists in models.py(db)
    if UserProfile.query.filter_by(last_name=last_name).first() is not None: 
        return jsonify({'error': 'Last name is taken'}), HTTP_409_CONFLICT
    
    #check if picture_url exists in models.py(db)
    if UserProfile.query.filter_by(picture_url=picture_url).first() is not None: 
        return jsonify({'error': 'Picture_url is taken'}), HTTP_409_CONFLICT
    
    password_hash= generate_password_hash(password)
    
    new_user = UserProfile(first_name=first_name, last_name=last_name, email=email, 
                password=password_hash, id=uuid.uuid4(), picture_url=picture_url)
    
    # user Login
    user_login = UserLogin(id=uuid.uuid4(), google_login=True, is_active=True,password_hash=password_hash,
        user_profile_id=new_user.id, last_login=datetime.now())

    db.session.add(new_user)
    db.session.add(user_login)
    db.session.commit()
    
    user_info = get_user_info(new_user.id)

    return jsonify(user_info), HTTP_201_CREATED
 