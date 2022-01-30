import uuid
import os
import logging
from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from src.models import Author, Book,  db
from src.google import get_user_info
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

book_bp = Blueprint('book', __name__, url_prefix='/api')


@book_bp.post('/books')
@swag_from('./docs/book/create.yml')
def create_book():
    file = request.files['image']
    
    # Author    
    author_first_name = request.form['author_first_name']
    author_last_name = request.form['author_last_name']
    
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
            'error': "book title is required"
        }), HTTP_400_BAD_REQUEST
        
    if not owner_id:
        return jsonify({
            'error': "book owner is required"
        }), HTTP_400_BAD_REQUEST
        
    if not year_of_publication:
        return jsonify({
            'error': "year of publication is required"
        }), HTTP_400_BAD_REQUEST
        
    if not (author_first_name and author_last_name):
        return jsonify({
            'error': "author's first and last name is required"
        }), HTTP_400_BAD_REQUEST
        
    # Upload image to cloudinary server
    cloudinary_response = upload(file, folder="yakitabu-books")
    
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
        url = cloudinary_response['secure_url'], # from cloudinary response after successful upload
        cld_asset_id=cloudinary_response['asset_id'],
        cld_public_id=cloudinary_response['public_id'],
        is_available=True,
        created_at=datetime.now(),
        borrowed=False # Not borrowed on creation
        )
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    
    return cloudinary_response

    return {"message":"book created"}, HTTP_201_CREATED
