import json
from unittest import TestCase, mock

from dotenv import load_dotenv
from flask import jsonify

from src import create_app
from src.user import validate_password_complexity
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST


class TestSignUp(TestCase):
    
    @mock.patch("src.user.signup", return_value=201 )
    def test_user_signup(self,signup):
        """
        Test case covering User signup
        """
        
        dummy_user = {
            "first_name": "Johannes",
            "last_name": "Döe",
            "email": "jd@email.com",
            "password": "J$12(H.A5h)2Doe!"
        }
        
        flask_app = create_app()
        
        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/login/user/signup',
                                        data=json.dumps(dummy_user), 
                                        content_type='application/json')
            response.status_code = signup()
            self.assertEqual(response.status_code, HTTP_201_CREATED)
            
            
    @mock.patch("src.user.login", return_value=200 )
    def test_user_login(self,login):
        """
        Test case covering User_login
        """

        test_user = {
            "email": "jd@email.com",
            "password": "J$12(H.A5h)2Doe!"
        }
        
        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/login/user',
                                        data=json.dumps(test_user), 
                                        content_type='application/json')
            response.status_code = login()
            self.assertEqual(response.status_code, HTTP_200_OK)
            
            
    def test_valid_password(self):
        """
        Test for testing valid password.
        """
        
        valid_password = "P@33word@12s#cret3"
        self.assertEqual(True, validate_password_complexity(valid_password))
        
        
    def test_invalid_password(self):
        """
        Test covering invalid password.
        """
        
        invalid_password = "password"
        self.assertEqual(False, validate_password_complexity(invalid_password))
        
        
    def test_invalid_password(self):
        """
        Additional test for testing invalid password.
        """
        
        invalid_password = "Password"
        self.assertEqual(False, validate_password_complexity(invalid_password))
        
    def test_invalid_password(self):
        """
        Additional test for testing invalid password.
        """
        
        invalid_password = "Password1"
        self.assertEqual(False, validate_password_complexity(invalid_password))

