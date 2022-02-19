import io
import json
from unittest import TestCase, mock

from src import create_app
from src.book import create_book
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST

class TestBook(TestCase):
    
    
    def test_successful_book_create(self):
        """
        Test Successful book creation.
        """
        with open('resources/yakitabu-image.png', 'rb') as img:
            image = io.BytesIO(img.read())
            
        test_data = {
            'image':(image,'yakitabu-logo.png'),
            'title': 'How not to learn German',
            'author_first_name': 'Tim',
            'isbn':'12-3434-J1002',
            'author_last_name': 'Lahaye',
            'language':'EN',
            'year_of_publication': 2002,
            'category': 'Motivational',
            'owner_id':'5c8d1765-4c9a-4641-841d-be8f9207f144'
        }
        flask_app = create_app()
        
        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/books',
                                        content_type='multipart/form-data',
                                        data=test_data
                                        )
            self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_unsuccessful_book_create_when_title_missing(self):
            """
            Test Unsuccessful book save due to book title missing.
            """
            with open('resources/yakitabu-image.png', 'rb') as img:
                image = io.BytesIO(img.read())
                
            test_data = {
                'image':(image,'yakitabu-logo.png'),
                'isbn':'12-3434-J1002',
                'author_first_name': 'Tim',
                'author_last_name': 'Lahaye',
                'language':'EN',
                'year_of_publication': 2002,
                'category': 'Motivational',
                'owner_id':'5c8d1765-4c9a-4641-841d-be8f9207f144'
            }
            flask_app = create_app()
            
            with flask_app.test_client() as test_client:
                response = test_client.post('http://localhost:5000/api/books',
                                            content_type='multipart/form-data',
                                            data=test_data
                                            )
                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
    
    
    def test_unsuccessful_book_create_when_isbn_missing(self):
        """
        Test Unsuccessful book save due to ISBN missing.
        """
        with open('resources/yakitabu-image.png', 'rb') as img:
            image = io.BytesIO(img.read())
            
        test_data = {
            'image':(image,'yakitabu-logo.png'),
            'title': 'How not to learn German',
            'author_first_name': 'Tim',
            'author_last_name': 'Lahaye',
            'language':'EN',
            'year_of_publication': 2002,
            'category': 'Motivational',
            'owner_id':'5c8d1765-4c9a-4641-841d-be8f9207f144'
        }
        flask_app = create_app()
        
        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/books',
                                        content_type='multipart/form-data',
                                        data=test_data
                                        )
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
            

    def test_unsuccessful_book_create_when_author_first_name_missing(self):
        """
        Test Unsuccessful book save due to author's first name missing.
        """
        with open('resources/yakitabu-image.png', 'rb') as img:
            image = io.BytesIO(img.read())
            
        test_data = {
            'image':(image,'yakitabu-logo.png'),
            'title': 'How not to learn German',
            'isbn':'12-3434-J1002',
            'author_last_name': 'Lahaye',
            'language':'EN',
            'year_of_publication': 2002,
            'category': 'Motivational',
            'owner_id':'5c8d1765-4c9a-4641-841d-be8f9207f144'
        }
        flask_app = create_app()
        
        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/books',
                                        content_type='multipart/form-data',
                                        data=test_data
                                        )
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
            
    def test_unsuccessful_book_create_when_owner_id_missing(self):
        """
        Test Unsuccessful book save due to Owner's ID missing.
        """
        with open('resources/yakitabu-image.png', 'rb') as img:
            image = io.BytesIO(img.read())
            
        test_data = {
            'image':(image,'yakitabu-logo.png'),
            'title': 'How not to learn German',
            'isbn':'12-3434-J1002',
            'author_first_name': 'Tim',
            'author_last_name': 'Lahaye',
            'language':'EN',
            'year_of_publication': 2002,
            'category': 'Motivational'
        }
        flask_app = create_app()
        
        with flask_app.test_client() as test_client:
            response = test_client.post('http://localhost:5000/api/books',
                                        content_type='multipart/form-data',
                                        data=test_data
                                        )
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
