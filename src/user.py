from flask import Blueprint, jsonify, request
from google.auth import jwt
from src.constants.http_status_codes import *
from src.models import UserLogin, UserProfile, db
import logging
import json
import uuid


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

        # # Currently setting username==email for google signups
        # email = google_response['email']

        # Check if user already exists. If no, create their profile
        user_exists = UserProfile.query.filter_by(email=email).first()
        if user_exists is None:
            uid = uuid.uuid4()

            new_user = UserProfile(
                id=uid,
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
                picture_url=image_url
            )
            #
            # user_login = UserLogin(
            #
            # )
            db.session.add(new_user)
            db.session.commit()

            return 'user_created'

    else:
        # TODO: Replace with Exception Message

        return jsonify({'error': "'id_token'  or 'image_url' is missing from request"}), HTTP_400_BAD_REQUEST

#
# Response: {
# 	first name: string
# 	Last name: string
# 	Id: string (this is the UUID that will be used as URL identifier)
# 	Available points: int
# 	Created date: month year
# 	Currently reading: {
# 		Title: string
# 		Author: string
# 		Category: string
# }
# }
