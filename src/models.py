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
    email_id = db.Column(UUID, db.ForeignKey("user_profile.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    picture_url = db.Column(db.String(300))
    available_points = db.Column(db.Integer)
    used_points = db.Column(db.Integer)
    borrowed = db.relationship("Borrowed", backref="user_profile", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Relationships
    userlogin = db.relationship("UserLogin", backref="user_profile", lazy=True)
    book = db.relationship("Book", backref="user_profile", lazy=True)
    lend = db.relationship("Borrowed", backref="user_profile", lazy=True)

    def __repr__(self):
        return f'User Profile ({self.id})'


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    isbn = db.Column(db.String(20))
    language = db.Column(db.String(30), nullable=False)
    year_of_publication = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(300), nullable=False)
    author_id = db.Column(UUID, db.ForeignKey("author.id"), nullable=False)
    owner_id = db.Column(UUID, db.ForeignKey("user_profile.id"), nullable=False)
    borrowed = db.Column(UUID, db.ForeignKey("user_profile.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    is_available = db.Column(db.Boolean, default=True)
    loan_points = db.Column(db.Integer, default=10)

    book = db.relationship("Borrowing", backref="book", lazy=True)
    lend = db.relationship("Lend", backref="book")


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    book = db.relationship("Book", backref="author", lazy=True)
    borrowed = db.relationship("Borrowed", backref="author", lazy=False)


class Borrowing(db.Model):
    __tablename__ = 'borrowing'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    borrowed_date = db.Column(db.DateTime, default=datetime.now())
    deadline = db.Column(db.DateTime, default=datetime.now())
    returned_date = db.Column(db.DateTime, default=datetime.now())
    points_used = db.Column(db.Integer, default=0)
    # lend_id = db.Column(UUID, db.Foreignkey("lending.id"), nullable=False)
    book_id = db.Column(UUID, db.ForeignKey("book.id"), nullable=False)
    borrowed_id = db.Column(UUID, db.ForeignKey("user_profile.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
