import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate, db
from App.main import create_app
# from App.controllers import ( create_user, get_all_users_json, get_all_users )
from App.controllers import ( create_author, delete_author, get_all_authors_json, get_all_authors, get_author_by_name ) #getauthor removed for now
# from App.controllers import ( get_all_items_json )
from App.controllers import ( create_publication )#, get_all_publications_json

from datetime import date

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')


@app.cli.command("drop")
def drop():
    db.drop_all()
    print("database destroyed")

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("author", help="Run Author tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AuthorUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("publication", help="Run Publication tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "PublicationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)





# authors
author_cli = AppGroup('author', help='author object commands') 

@author_cli.command("list")
def list_authors():
    authors = get_all_authors_json()
    print(authors)

@author_cli.command("create", help="Creates an author")
@click.argument("first_name", default="bob")
@click.argument("last_name", default="burger")
@click.argument("email", default="bob@mail.com")
@click.argument("password", default="bobpass")
def create_author_command(first_name, last_name, email, password):
    author = create_author(first_name, last_name, email, password)
    print(author.first_name+" created!")

@author_cli.command("delete", help="Deletes an author")
@click.argument("id")
def delete_author_command(id):
    delete_author(id)
    print("Author deleted")

@author_cli.command("list", help="Lists all authors")
def list_authors_command():
    authors = get_all_authors_json()
    print(authors)

app.cli.add_command(author_cli)






# publications
publication_cli = AppGroup('pub', help='pub object commands') 

@publication_cli.command("create", help="Creates a publication")
@click.option("--author_ids", "-a", multiple=True)
@click.option("--coauthor_ids", "-ca", multiple=True)
@click.argument("title", default="Computer Science 1st Edition")
def create_publication_command(title, author_ids, coauthor_ids):
    authors = [get_author(id) for id in author_ids]
    coauthors = [get_author(id) for id in coauthor_ids]
    # a = get_author(author_ids)
    create_publication(title, authors, coauthors)
    print(f'{title} created!')

@publication_cli.command("list")
def list_publications():
    publications = get_all_publications_json()
    print(publications)

@publication_cli.command("create_names")
@click.option("--author_names", "-A", multiple=True)
@click.option("--coauthor_names", "-CA", multiple=True)
@click.argument("title", default="Computer Science 1st Edition")
def create_publication_command(title, author_names, coauthor_names):
    authors = sum ( [get_author_by_name(name) for name in author_names], [] )
    print(authors)
    coauthors = sum ( [get_author_by_name(name) for name in coauthor_names], [] )
    print(coauthors)
    # a = get_author(author_ids)
    create_publication(title, authors, coauthors)
    print(f'{title} created!')


app.cli.add_command(publication_cli)
