from flask import Blueprint, jsonify, request
from google.auth import jwt
from src.constants.http_status_codes import *
from src.models import UserLogin, UserProfile, db, Borrowing
import logging
import json
import uuid
from datetime import datetime

user = Blueprint('user', __name__, url_prefix='/api/v1/user')


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
    return jwt.decode(token_object, verify=False)


@user.post('/login/google')
def login():
    # Checks on request.
    if 'id_token' and 'image_url' in request.json:
        token = request.json['id_token']
        image_url = request.json['image_url']

        google_response = decode_token(token)

        email = google_response['email']
        first_name = google_response['given_name']
        last_name = google_response['family_name']
        picture_url = request.json['image_url']

        # Check if user already exists. If no, create their profile
        user_exists = UserProfile.query.filter_by(email=email).first()

        if user_exists is None:
            uid = uuid.uuid4()

            # User Profile
            new_user = UserProfile(
                id=uid,
                first_name=first_name,
                last_name=last_name,
                email=email,
                # Currently setting username==email for google signups
                username=email,
                picture_url=image_url
            )

            # user Login
            user_login = UserLogin(
                id=uuid.uuid4(),
                google_login=True,
                is_active=True,
                user_profile_id=new_user.id
            )
            db.session.add(new_user)
            db.session.add(user_login)
            db.session.commit()

            user_profile = UserProfile.query.filter_by(id=uid).first()
            last_borrowed = Borrowing.query.filter_by(borrower=uid).order_by(Borrowing.created_at.desc())

            return jsonify({
                'id': user_profile.id,
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'available_points': user_profile.available_points,
                'created_date': user_profile.created_at,
                'currently_reading': user_profile.book
                # TODO
                # 'currently_reading': jsonify({
                #     'title': last_borrowed.book.name,
                #     'author': last_borrowed.book.author.first_name + last_borrowed.book.author.last_name})
            }), HTTP_200_OK
        else:
            # Change filter criteria to email, since user already exists.
            user_profile = UserProfile.query.filter_by(email=email).first()
            # last_borrowed = Borrowing.query.filter_by(borrower=user_profile.id).order_by(Borrowing.created_at.desc(
            # )).\ first()
            last_borrowed = Borrowing.query.filter_by(borrower=user_profile.id).first()
            return jsonify({
                'id': user_profile.id,
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'available_points': user_profile.available_points,
                'created_date': user_profile.created_at,
                'currently_reading': user_profile.book,
                # TODO
                # 'currently_reading': jsonify({
                #     'title': last_borrowed.book.name,
                #     'author': last_borrowed.book.author.first_name + last_borrowed.book.author.last_name})
            }), HTTP_200_OK
    else:
        # TODO: Replace with Exception Message
        return jsonify({
            'error': "'id_token'  or 'image_url' is missing from request"
        }), HTTP_400_BAD_REQUEST
