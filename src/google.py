import logging
import json
import uuid
from datetime import datetime

from google.auth import jwt
from flask import Blueprint, jsonify, request

from src.constants.http_status_codes import HTTP_200_OK,HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from src.models import UserLogin, UserProfile, db, Borrow


google_bp = Blueprint('google', __name__, url_prefix='/api')


def decode_token(token_object):
    """
    Decodes a google token and returns a JSON object with the following details
    {
        "at_hash": "ekLIO2gVVwjiH02eiu88hQ",
        "aud": "170044535313-f02c8hd020ptha7n0t4fraouo2ap9bqq.apps.googleusercontent.com",
        "azp": "170044535313-f02c8hd020ptha7n0t4fraouo2ap9bqq.apps.googleusercontent.com",
        "email": "email@mail.com",
        "email_verified": true,
        "exp": 1636222353,
        "family_name": "Last_Name",
        "given_name": "First_Name",
        "iat": 1000000000,
        "iss": "accounts.google.com",
        "jti": "0019b0aaa2e355f8fa2b2ce8b3bbbbab7b63a5014",
        "locale": "en-GB",
        "name": "First_Name Name",
        "picture": "https://lh3.googleusercontent.com/a-/image_url..",
        "sub": "113501893650341726537"
    }
    """
    # https://google-auth.readthedocs.io/en/latest/reference/google.auth.jwt.html#google.auth.jwt.decode
    # Disabling verification because we don’t have the required certificates to do this verification in google at the moment.
    return jwt.decode(token_object, verify=False)
    

@google_bp.post('/login/google')
def login():
       
    if 'id_token' not in request.json:
        return jsonify({
            'error': "'id_token' is missing from request"
        }), HTTP_400_BAD_REQUEST

    token = request.json['id_token']
    
    google_response = decode_token(token)
    
    if google_response == HTTP_400_BAD_REQUEST:
        return jsonify({
            'error': "Invalid Token"
        }), HTTP_400_BAD_REQUEST


    email = google_response.get('email')
    first_name = google_response.get('given_name'),
    last_name = google_response.get('family_name')
    picture_url = google_response.get('picture')

    # Check if user already exists. If no, create their profile
    user_exists = UserProfile.query.filter_by(email=email).first()

    if user_exists:
        user_profile = UserProfile.query.filter_by(email=email).first()
        return jsonify(get_user_info(user_profile.id)), HTTP_200_OK

    # User doesn't exist yet, create user profile
    new_user = UserProfile(
        id=uuid.uuid4(),
        first_name=first_name,
        last_name=last_name,
        email=email,
        picture_url=picture_url
    )

    # user Login
    user_login = UserLogin(
        id=uuid.uuid4(),
        google_login=True,
        is_active=True,
        user_profile_id=new_user.id,
        last_login=datetime.now()
    )

    db.session.add(new_user)
    db.session.add(user_login)
    db.session.commit()

    user_profile = UserProfile.query.filter_by(id=new_user.id).first()
    if not user_profile:
        return jsonify({
            "error": "This user doesn't have a profile."
            }), HTTP_404_NOT_FOUND
    
    return jsonify(get_user_info(user_profile.id)), HTTP_200_OK


def get_user_info(uid):    
    """
    Returns a user's profile information using the user_id
    """
    user_profile = UserProfile.query.filter_by(id=uid).first()
    
    if not user_profile:
        return jsonify({
            "error": "This user doesn't have a profile."
            }), HTTP_404_NOT_FOUND
    
    user_info = {
        'id': user_profile.id,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'email': user_profile.email,
        'available_points': user_profile.available_points,
        'created_date': user_profile.created_at,
        'currently_reading': get_last_unreturned_book(user_profile.id)
    }
    return user_info


def get_last_unreturned_book(user_id):
    """
    Returns the last book a user borrowed.
    """
    last_borrowed = Borrow.query.filter_by(
        borrower=user_id,
        returned_date=None
    ).order_by(Borrow.created_at.desc()).first()

    # User has borrowed at least one book
    if last_borrowed:
        return {
            'title': last_borrowed.book.name,
            'author': last_borrowed.book.author.first_name + " " + last_borrowed.book.author.last_name
        }
    
    # User has not borrowed any book
    return {
        'title': '',
        'author': ''
    }
