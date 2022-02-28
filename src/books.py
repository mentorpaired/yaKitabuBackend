from flask import Blueprint, jsonify, request
from flasgger import swag_from

from src.models import Book
from src.constants.http_status_codes import HTTP_200_OK


books_bp = Blueprint('books', __name__, url_prefix='/api')


@books_bp.get("/books/available")
@swag_from("./docs/books/available_books.yaml")
def available_books():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", None, type=int)
    books = Book.query.filter_by(is_available=True).paginate(page=page, per_page=per_page)

    books_object = []

    for book in books.items:
        books_object.append({
            "id": book.id,
            "name": book.name,
            "author": book.author.first_name + " " + book.author.last_name,
            "category": book.category,
            "isbn": book.isbn
        })

    meta = {
        "page": books.page,
        "pages": books.pages,
        "total_count": books.total,
        "prev_page": books.prev_num,
        "next_page": books.next_num,
        "has_next": books.has_next,
        "has_prev": books.has_prev
    }

    return jsonify({"data": books_object, "meta": meta}), HTTP_200_OK
