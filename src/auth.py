from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

import validators

from src.models import UserLogin

auth = Blueprint("auth", __name__, url_prefix="login/user/signup")

@auth.post('/signup')
def signup():
    username=request.json['first_name', 'last_name']
    email=request.json['email']
    password=request.json['password']
    
    #check for length of password
    if len(password)<6:
        return jsonify({'error': 'Password is too short'}), HTTP_400_BAD_REQUEST
    
    # if not username.isalnum() or " " in username:
    #     return jsonify({'error': 'Username should be alphanumeric, also no spaces'}), HTTP_400_BAD_REQUEST
    
    #check for length of username
    if len(username)<3:
        return jsonify({'error': 'Username is too short'}), HTTP_400_BAD_REQUEST
    
    #check for email validity
    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), HTTP_400_BAD_REQUEST
    
    #check if email exists in the models.py(db)
    if UserLogin.objects.filter_by(email=email).first() is not None: 
        return jsonify({'error': 'Email is taken'}), HTTP_409_CONFLICT
    
    #check if username exists in models.py(db)
    if UserLogin.objects.filter_by(username=username).first() is not None: 
        return jsonify({'error': 'Username is taken'}), HTTP_409_CONFLICT
    
    pwd_hash= generate_password_hash(password)
    
    UserLogin = UserLogin(username=username, password=pwd_hash, email=email)
    db.session.add(User)
    db.session.commit()
    
    return jsonify({
        'message': 'User Created',
        'User': {
            'username': first_name, last_name, email},
        'id': uuid,
        'available points': int
        'created_at': month, year
        'currently_reading'
                    })
    
    return "user created"

@auth.get("/me")
def me():
    return {"user": "me"}
 