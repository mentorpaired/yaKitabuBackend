from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


db = SQLAlchemy()

class UserLogin(db.Model):
    __tablename__ = 'user_login'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    password_hash = db.Column(db.String(200))
    google_login = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    user_profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user_profile.id"))
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    picture_url = db.Column(db.String(300))
    available_points = db.Column(db.Integer)
    used_points = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Relationships
    user_login = db.relationship("UserLogin", backref="user_profile")
    borrowed = db.relationship("Borrow", backref="user_profile")
    book = db.relationship("Book", backref="user_profile", lazy=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f'User Profile ({self.id})'


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    isbn = db.Column(db.String(20))
    language = db.Column(db.String(30), nullable=False)
    year_of_publication = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(300), nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey("author.id"))
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user_profile.id"), nullable=False)
    borrowed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    is_available = db.Column(db.Boolean, default=True)
    loan_points = db.Column(db.Integer)

    book = db.relationship("Borrow", backref="book", lazy=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Borrow(db.Model):
    __tablename__ = 'borrow'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    borrowed_date = db.Column(db.DateTime, default=datetime.now())
    deadline = db.Column(db.DateTime, nullable=False)
    returned_date = db.Column(db.DateTime)
    points_used = db.Column(db.Integer)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey("book.id"), nullable=False)
    borrower = db.Column(UUID(as_uuid=True), db.ForeignKey("user_profile.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    book = db.relationship("Book", backref="author", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
