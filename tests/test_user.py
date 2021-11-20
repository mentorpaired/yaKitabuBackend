import os
import json
from src import app, create_app
from unittest import TestCase
from src.user import decode_token, login, get_user_info, get_last_unreturned_book
from src.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST


import unittest

class TestUser(TestCase):
    
    def setUp(self):
        pass
    
    def test_token_decode(self):
        """
        Test for decoding token and extracting user information.
        """

        token = {
            'id_token': "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI3YzcyNjE5ZDA5MzVhMjkwYzQxYzNmMDEwMTY3MTM4Njg1ZjdlNTMiLCJ0eXAiOiJKV1" \
                   "QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTcwMDQ0NTM1MzEzLWYwMmM4aGQwMjBwdGhhN24wdDRmc" \
                   "mFvdW8yYXA5YnFxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTcwMDQ0NTM1MzEzLWYwMmM4aGQwMjBwdGh" \
                   "hN24wdDRmcmFvdW8yYXA5YnFxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAzOTE3NDEzMTM4OTI4NDc1M" \
                   "TMyIiwiZW1haWwiOiJ5YWtpdGFidS5pb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6InVtU01" \
                   "zeV9EQ3lVRXJyTFZCQ3VmbmciLCJuYW1lIjoiWWFraXRhYnUgUHJvamVjdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nb" \
                   "GV1c2VyY29udGVudC5jb20vYS9BQVRYQUp6bjdWNWZYaGZuYXpvVjYyNWVDY25pR21yYXpuNEd5dVhqQW5lUz1zOTYtYyIsImd" \
                   "pdmVuX25hbWUiOiJZYWtpdGFidSIsImZhbWlseV9uYW1lIjoiUHJvamVjdCIsImxvY2FsZSI6ImVuLUdCIiwiaWF0IjoxNjM3M" \
                   "DE5MDIyLCJleHAiOjE2MzcwMjI2MjIsImp0aSI6ImNkNzAyYzgxOGEwNDFhOTJkNWFlNzU1ZmM4OWFkMjhjZDFkOTU1NGMifQ.U" \
                   "jGqawnbzRHTtoNDLneEwbHXw954NOiyS3GSXIo1j-lfUYmGtFMkXLTpMuEFHX6xRX-U7x0stxQ_riz4U28v2ThmHLFbOdaPsWAi" \
                   "sf2kUGznT3jhW7YvbQht8uSy9HSVKHZkVsozmryVFUocheSMBAwbjjJh0zE8QJv9DOTTKHzGbQcnQXmPP2BJs3Z1xlXMxXbXLWb" \
                   "T6-rGDMBtQUenD0GmVeY8cnPgEo12BAajenljtSW8ec7EdDRW44gNLR5ba2huBld7609oUdo4nLm_oIXGyVHuCzlv1OBJyyT5EO" \
                   "yU98jiHF3e7AyTSMtCD5s7WvbTvKy8So4PGeZxnRmKjA"
                   }
        decoded_token = decode_token(token['id_token'])

        self.assertEqual(decoded_token['email'], 'yakitabu.io@gmail.com')
        self.assertEqual(decoded_token['given_name'], 'Yakitabu')
        self.assertEqual(decoded_token['family_name'], 'Project')

    def test_valid_login(self):
        """
        Test case covering Valid Login
        """
        token = {
            'id_token': "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI3YzcyNjE5ZDA5MzVhMjkwYzQxYzNmMDEwMTY3MTM4Njg1ZjdlNTMiLCJ0eXAiOiJKV1" \
                   "QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTcwMDQ0NTM1MzEzLWYwMmM4aGQwMjBwdGhhN24wdDRmc" \
                   "mFvdW8yYXA5YnFxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTcwMDQ0NTM1MzEzLWYwMmM4aGQwMjBwdGh" \
                   "hN24wdDRmcmFvdW8yYXA5YnFxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAzOTE3NDEzMTM4OTI4NDc1M" \
                   "TMyIiwiZW1haWwiOiJ5YWtpdGFidS5pb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6InVtU01" \
                   "zeV9EQ3lVRXJyTFZCQ3VmbmciLCJuYW1lIjoiWWFraXRhYnUgUHJvamVjdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nb" \
                   "GV1c2VyY29udGVudC5jb20vYS9BQVRYQUp6bjdWNWZYaGZuYXpvVjYyNWVDY25pR21yYXpuNEd5dVhqQW5lUz1zOTYtYyIsImd" \
                   "pdmVuX25hbWUiOiJZYWtpdGFidSIsImZhbWlseV9uYW1lIjoiUHJvamVjdCIsImxvY2FsZSI6ImVuLUdCIiwiaWF0IjoxNjM3M" \
                   "DE5MDIyLCJleHAiOjE2MzcwMjI2MjIsImp0aSI6ImNkNzAyYzgxOGEwNDFhOTJkNWFlNzU1ZmM4OWFkMjhjZDFkOTU1NGMifQ.U" \
                   "jGqawnbzRHTtoNDLneEwbHXw954NOiyS3GSXIo1j-lfUYmGtFMkXLTpMuEFHX6xRX-U7x0stxQ_riz4U28v2ThmHLFbOdaPsWAi" \
                   "sf2kUGznT3jhW7YvbQht8uSy9HSVKHZkVsozmryVFUocheSMBAwbjjJh0zE8QJv9DOTTKHzGbQcnQXmPP2BJs3Z1xlXMxXbXLWb" \
                   "T6-rGDMBtQUenD0GmVeY8cnPgEo12BAajenljtSW8ec7EdDRW44gNLR5ba2huBld7609oUdo4nLm_oIXGyVHuCzlv1OBJyyT5EO" \
                   "yU98jiHF3e7AyTSMtCD5s7WvbTvKy8So4PGeZxnRmKjA"
                   }
        flask_app = create_app()
        

        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/v1/user/login/google',
                                        data=json.dumps(token),
                                        content_type='application/json',
                                        )
            assert response.status_code == HTTP_200_OK
            

    def test_invalid_login(self):
        """
        Test case covering Bad Request
        """
        token = {'id_token': "5om3InvalidTokeN"}
        flask_app = create_app()
        

        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/v1/user/login/google',
                                        data=json.dumps(token),
                                        content_type='application/json',
                                        )
            assert response.status_code == HTTP_400_BAD_REQUEST
       
    def test_login_get(self):
        """
        Test case covering unsupported METHOD: POST
        """

        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.get('http://localhost:5000/api/v1/user/login/google')

            assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
            
            
    def test_login_put(self):
        """
        Test case covering unsupported METHOD: PUT
        """

        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.get('http://localhost:5000/api/v1/user/login/google')

            assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


if __name__ == '__main__':
    unittest.main()
