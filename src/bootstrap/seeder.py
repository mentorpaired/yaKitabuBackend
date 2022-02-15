import uuid
import random
from datetime import datetime, timedelta

from faker import Faker
from werkzeug.security import generate_password_hash

from src.models import Author, Book, Borrow, UserProfile, UserLogin


faker = Faker(['en_CA', 'en_AU', 'en_GB', 'de_DE', 'en_US'])

book_categories = ['adventure', 'humor', 'philosophy', 'science', 'drama', 'psychology', 'tech'
                   'religion', 'politics', 'action', 'travel', 'comedy', 'self-help']
languages = ['english', 'french', 'german']


def generate_seed_data():
    # A User whose book was borrowed
    user_lender = UserProfile(
        id=uuid.uuid4(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        picture_url=faker.url(),
    )

    # A User who borrowed the book.
    user_borrower = UserProfile(
        id=uuid.uuid4(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        picture_url=faker.url(),
    )
    
    user_lender_login = UserLogin(
        id=uuid.uuid4(),
        google_login=False,
        is_active=True,
        password_hash=generate_password_hash('Password123$'),
        user_profile_id=user_lender.id,
        last_login=datetime.now()
    )
    
    user_borrower_login = UserLogin(
        id=uuid.uuid4(),
        google_login=False,
        is_active=True,
        password_hash=generate_password_hash('Password123$'),
        user_profile_id=user_borrower.id,
        last_login=datetime.now()
    )

    author_book_a = Author(
        id=uuid.uuid4(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        created_at=datetime.now()
    )
    author_book_b = Author(
        id=uuid.uuid4(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        created_at=datetime.now()
    )
    
    lenders_book = Book(
        id=uuid.uuid4(),
        name=faker.sentence(nb_words=5),
        isbn=faker.isbn13(),
        year_of_publication=random.randint(1900, 2021),
        language=random.choice(languages),
        category=random.choice(book_categories),
        author_id=author_book_a.id,
        owner_id=user_lender.id,
        is_available=False,
        created_at=datetime.now()
    )
    
    # This book will be available for borrowing.
    avail_book = Book(
        id=uuid.uuid4(),
        name=faker.sentence(nb_words=5),
        isbn=faker.isbn13(),
        year_of_publication=random.randint(1900, 2021),
        language=random.choice(languages),
        category=random.choice(book_categories),
        author_id=author_book_b.id,
        owner_id=user_borrower.id,
        is_available=True,
        created_at=datetime.now()
    )
    
    borrow = Borrow(
        id=uuid.uuid4(),
        borrowed_date=datetime.now(),
        deadline=datetime.now() + timedelta(days=5),
        points_used=random.choice([5, 10, 15, 20, 30]),
        book_id=lenders_book.id,
        borrower=user_borrower.id,
        created_at=datetime.now()
    )
    
    return (user_lender, user_borrower, user_lender_login, user_borrower_login,
            author_book_a, author_book_b, lenders_book,avail_book, borrow)
