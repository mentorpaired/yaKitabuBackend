import uuid
import random
from datetime import datetime, timedelta

from faker import Faker
from werkzeug.security import generate_password_hash

from src.models import Author, Book, Borrow, UserProfile, UserLogin


faker = Faker(['en_CA', 'en_AU', 'en_GB', 'de_DE', 'en_US'])
Faker.seed(25)

book_categories = ['adventure', 'humor', 'philosophy', 'science', 'drama', 'psychology', 'tech'
                   'religion', 'politics', 'action', 'travel', 'comedy', 'self-help']
languages = ['english', 'french', 'german']


def generate_seed_data():
    new_user = UserProfile(
        id=uuid.uuid4(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        picture_url=faker.url(),
    )
    user_login = UserLogin(
        id=uuid.uuid4(),
        google_login=True,
        is_active=True,
        password_hash=generate_password_hash('Password123$'),
        user_profile_id=new_user.id,
        last_login=datetime.now()
    )

    author = Author(
        id=uuid.uuid4(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        created_at=datetime.now()
    )
    book = Book(
        id=uuid.uuid4(),
        name=faker.sentence(nb_words=5),
        isbn=faker.isbn13(),
        year_of_publication=random.randint(1900, 2021),
        language=random.choice(languages),
        category=random.choice(book_categories),
        author_id=author.id,
        owner_id=new_user.id,
        created_at=datetime.now()
    )
    borrow = Borrow(
        id = uuid.uuid4(),
        borrowed_date=datetime.now(),
        deadline=datetime.now() + timedelta(days=5),
        points_used=random.choice([5,10,15,20,30]),
        book_id = book.id,
        borrower = new_user.id,
        created_at = datetime.now()        
    )
    book.is_available=False
    
    print(new_user)
    print(user_login)
    print(author)
    print(book)
    print('=======================')
    return new_user, user_login, author, book, borrow
