from datetime import datetime

from app import db 


class UserLogin(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Integer, unique=True)
    google_external_id = db.Column(db.String, unique=True) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class UserProfile(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    picture_url = db.Column(db.String(300))
    available_points = db.Column(db.Integer)
    used_points = db.Column(db.Integer)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    isbn = db.Column(db.String(300))
    language = db.Column(db.String(300))
    author = db.relationship("Author", backref="book", lazy=True)
    year_of_publication = db.Column(db.Integer)
    category = db.Column(db.String(300), nullable=False)
    owner = db.relationship("UserProfile", backref="book", lazy=True)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))


class Borrowed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lender = db.relationship("Userprofile", backref="borrowed", lazy=True)
    borrower = db.relationship("Userprofile", backref="borrowed", lazy=True)
    borrowed_date = db.Column(db.DateTime, default=datetime.now())
    deadline = db.Column(db.DateTime)
    returned_date = db.Column(db.DateTime)
    points_used = db.Column(db.Integer, default=0)


class Lend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.relationship("Book", backref="lend")
    points = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, defualt=True)
