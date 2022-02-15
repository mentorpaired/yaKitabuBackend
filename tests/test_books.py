import os
from unittest import TestCase, mock

from src import create_app
from src.books import available_books
from src.constants.http_status_codes import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED


class TestBooks(TestCase):
    @mock.patch("src.books.available_books", return_value=200)
    def test_valid_available_books(self, available_books):
        """
        Test case covering valid available books
        """
        flask_app = create_app()

        with flask_app.test_client() as test_client:

            response = test_client.get(
                "http://localhost:5000/api/books/available"
            )
            self.assertEqual(response.status_code, HTTP_200_OK)

    def test_when_no_books_are_available(self):
        """
        Test case covering when no books are available books
        """
        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.get(
                "http://localhost:5000/api/books/available"
            )        
            self.assertEqual(response.status_code, HTTP_200_OK)

    def test_available_books_post(self):
        """
        Test case covering unsupported METHOD: POST
        """

        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.post(
                "http://localhost:5000/api/books/available"
            )

            self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_available_books_put(self):
        """
        Test case covering unsupported METHOD: PUT
        """

        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.put(
                "http://localhost:5000/api/books/available"
            )

            self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_available_books_delete(self):
        """
        Test case covering unsupported METHOD: DELETE
        """

        flask_app = create_app()

        with flask_app.test_client() as test_client:
            response = test_client.delete(
                "http://localhost:5000/api/books/available"
            )

            self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
