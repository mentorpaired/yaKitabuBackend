import click
from tqdm import tqdm
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
    """Generate seed data in staging and local database for testing purposes
       number = 1 will generate 2 User profiles (1 borrower and 1 lender), 
       2 books (the first book is borrowed, while second book will be available for loan)) and 1 
    Args:
        number (int):   number of seed data to generate. 
                        number=1 will generate 2 
                        
    """
    print("Generating seed data for testing purposes")
    for _ in tqdm(range(number)):
        objects = generate_seed_data()
        for item in objects:
            db.session.add(item)
            print(f"Generating: {item}")
            print("==================")
    db.session.commit()
    print(f"Succesfully generated {number*2}:User Profiles, {number*2}:Books, {number*2}:Authors and {number}:book(s) borrowed")
