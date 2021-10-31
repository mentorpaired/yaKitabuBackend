from datetime import datetime

from app import db 


class UserLogin(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200))
    google_external_id = db.Column(db.String(200), unique=True) 
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey("userprofile.id"), nullable=False)


class UserProfile(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    picture_url = db.Column(db.String(300))
    available_points = db.Column(db.Integer)
    used_points = db.Column(db.Integer)
    userlogin = db.relationship("UserLogin", backref="userprofile", lazy=True)
    book = db.relationship("Book", backref="userprofile", lazy=True)
    lend = db.relationship("Borrowed", backref="userprofile", lazy=True)
    borrowed = db.relationship("Borrowed", backref="userprofile", lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    isbn = db.Column(db.String(300))
    language = db.Column(db.String(300), nullable=False)
    year_of_publication = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(300), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("userprofile.id"), nullable=False)
    borrowed = db.Column(db.Integer, db.ForeignKey("userprofile.id"), nullable=False)
    book = db.relationship("Borrowed", backref="book", lazy=True)
    lend = db.relationship("Lend", backref="book")

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    book = db.relationship("Book", backref="author", lazy=True)
    borrowed = db.relationship("Borrowed", backref="author", lazy=False)


class Borrowed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrowed_date = db.Column(db.DateTime, default=datetime.now(), nullabe=False)
    deadline = db.Column(db.DateTime, default=datetime.now())
    returned_date = db.Column(db.DateTime, default=datetime.now())
    points_used = db.Column(db.Integer, default=0)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    lend_id = db.Column(db.Integer, db.Foreignkey("lend.id"), nullable=False)
    borrowed_id = db.Column(db.Integer, db.ForeignKey("userprofile.id"), nullable=False)


class Lend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.Foreignkey("book.id"), nullable=False)
    points = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    