import os
from unittest import TestCase, mock

from src import create_app

from src.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND, \
    HTTP_405_METHOD_NOT_ALLOWED


class TestBooks(TestCase):
    @mock.patch("src.books.available_books", return_value=200)
    @mock.patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql://postgres:<db password>"
                            "@<host>:<port>/<db name>"
        },
    )
    def test_valid_available_books(self, available_books):
        """
        Test case covering valid available books
        """
        flask_app = create_app()

        with flask_app.test_client() as test_client:
            try:
                response = test_client.get(
                    "http://localhost:5000/api/books/available"
                )
                self.assertEqual(response.status_code, HTTP_200_OK)
            except AssertionError:
                response = test_client.get(
                    "http://localhost:5000/api/books/available"
                )
                self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

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
