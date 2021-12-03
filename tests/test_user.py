import json
import logging
from unittest import TestCase, mock

from dotenv import load_dotenv
from flask import jsonify

from src import create_app
from src.google import decode_token, login
from src.constants.http_status_codes import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST


class TestUser(TestCase):

    @mock.patch("src.google.decode_token", return_value={
        'given_name': 'Yakitabu',
        'family_name': 'Project'
                
    })
    def test_token_decode(self, decode_token):
        """
        Test for decoding token and extracting user information.
        """

        decoded_token = decode_token("<Dummy_Token>")

        self.assertEqual(decoded_token['given_name'], 'Yakitabu')
        self.assertEqual(decoded_token['family_name'], 'Project')

    
    @mock.patch("src.google.login", return_value=200 )
    def test_valid_login(self,login):
        """
        Test case covering valid login
        """
    
        flask_app = create_app()
        
        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/login/google',
                                        data=json.dumps({'id':'sometoken'}),
                                        content_type='application/json',
                                        )
            response.status_code = login()
            self.assertEqual(response.status_code, HTTP_200_OK)


    def test_invalid_login(self):
        """
        Test case covering Bad Request
        """
        token = {'id_token': "5om3hcvjhkct.cyfkukbhckyjsjdjsdsdsdtfghjkghv.vjkfyjujhjctrzrerrezxeszZwerzbxd.InvalidTokeN"}
        flask_app = create_app()
        
       
        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/login/google',
                                        data=json.dumps(token),
                                        content_type='application/json',
                                        )
            self.assertRaises(ValueError, decode_token, token)
       
       
    def test_login_get(self):
        """
        Test case covering unsupported METHOD: POST
        """

        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.get('http://localhost:5000/api/login/google')

            self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
            
            
    def test_login_put(self):
        """
        Test case covering unsupported METHOD: PUT
        """

        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.get('http://localhost:5000/api/login/google')

            self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
