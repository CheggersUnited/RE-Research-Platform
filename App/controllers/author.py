from App.models import Author
from App.database import db
from sqlalchemy.exc import IntegrityError
from queue import Queue

def create_author(first_name, last_name, email, password):
    new_author = Author(first_name=first_name, last_name=last_name, email=email, password=password)
    try:
        db.session.add(new_author)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return new_author

def get_all_authors():
    return Author.query.all()

def get_all_authors_json():
    authors = Author.query.all()
    if not Author:
        return []
    authors = [author.toDict() for author in authors]
    return authors

def get_author_by_name(first_name,last_name):
    print(first_name,last_name)
    authors = Author.query.filter_by(first_name=first_name)
    author = authors.filter_by(last_name = last_name).first()
    if not author:                              
        return None
    return author
    
def create_default_author_account(first_name, last_name, email):
    password = first_name + "pass"
    new_author = create_author(first_name, last_name, email, password)
    return new_author == None

def get_author_by_id(id):
    author = Author.query.filter_by(id=id).first()
    return author

def create_new_author_account():
    pass

def author_publication_tree(id):
    author = get_author_by_id(id)
    authors = []
    publications = []
    queue = Queue()
    return author.getPublicationTree(root, authors, publications, queue)

def delete_author(id):
    author = get_author_by_id(id)
    db.session.delete(author)
    db.session.commit()
    return True