import click
from flask.cli import with_appcontext

from src import db
from src.bootstrap.seeder import generate_seed_data


# Custom commands to manage migrations.
# https://flask.palletsprojects.com/en/2.0.x/cli/#custom-commands
@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()


# This enables the generation of seed data into the local and staging db.
# To generate seed, user needs to run `flask generate_data [number]` in the terminal
# `number` represents the number of seed data to generate.
@click.command(name='generate_data')
@click.argument("number", required=True, type=int)
@with_appcontext
def generate_data(number):    
    for _ in range(int(number)):
        new_user, user_login, author, book, borrow, = generate_seed_data()
        db.session.add(author)
        db.session.add(new_user)
        db.session.add(user_login)
        db.session.add(book)
        db.session.add(borrow)
    db.session.commit()
