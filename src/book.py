import uuid
import os
import logging
from datetime import datetime

from flask import Blueprint, jsonify, request
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from src.models import Author, Book,  db
from src.google import get_user_info
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

book_bp = Blueprint('book', __name__, url_prefix='/api')


@book_bp.post('/books')
def create_book():
    file = request.files['image']
    if not file:
        return jsonify({
            'error': "book image missing"
        }), HTTP_400_BAD_REQUEST


    # Author
    book_author = request.form['author'].split(' ')
    author_first_name = book_author[0]
    author_last_name = ' '.join(book_author[1:])

    # Book
    title = request.form['title']
    isbn = request.form['isbn']
    language = request.form['language']
    year_of_publication = request.form['year_of_publication']
    category = request.form['category']
    owner_id = request.form['owner_id']
    
    if not title:
        return jsonify({
            'error': "book's title missing"
        }), HTTP_400_BAD_REQUEST

    if not language:
        return jsonify({
            'error': "book's language missing"
        }), HTTP_400_BAD_REQUEST
        
    if not owner_id:
        return jsonify({
            'error': "book's owner missing"
        }), HTTP_400_BAD_REQUEST
    
    if not year_of_publication:
        return jsonify({
            'error': "book's year of publication missing"
        }), HTTP_400_BAD_REQUEST
    
    if not (author_first_name and author_last_name):
        return jsonify({
            'error': "author's name missing"
        }), HTTP_400_BAD_REQUEST
        

    # Upload image to cloudinary server
    cloudinary_response = upload(file, folder="bookie-books")
    
    if not cloudinary_response:
        return jsonify({
            'error': "error uploading image"
        }), HTTP_400_BAD_REQUEST

    author = Author(
        id=uuid.uuid4(),
        first_name=author_first_name,
        last_name=author_last_name)

    book = Book(
        id=uuid.uuid4(),
        name=title,
        isbn=isbn,
        language=language,
        year_of_publication=year_of_publication,
        category=category,
        author_id=author.id,
        owner_id=uuid.UUID(owner_id),
        url = cloudinary_response['url'], # from cloudinary response after successful upload
        is_available=True,
        created_at=datetime.now(),
        borrowed=False # Not borrowed on creation
        )
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    
    return {"message":"book created"}, HTTP_201_CREATED
