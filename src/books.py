from flask import Blueprint, jsonify, request
from flasgger import swag_from

from src.models import Book
from src.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND


books_bp = Blueprint('books', __name__, url_prefix='/api')


@books_bp.get("/books/available")
@swag_from("./docs/books/available_books.yaml")
def available_books():


    books = Book.query.filter_by(is_available=True)

    if len(list(books)) < 1:
        
        return jsonify({
            "error": "no books are available"
        }),HTTP_404_NOT_FOUND

    books_object= list()

    for book in books:
        books_object.append({
            "id": book.id,
            "name": book.name,
            "author": book.author.first_name + " " + book.author.last_name,
            "category": book.category,
            "isbn": book.isbn
        })
    
    return jsonify(books_object), HTTP_200_OK
