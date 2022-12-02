from App.models import Author, PublishingRecord
from App.database import db
from sqlalchemy.exc import IntegrityError
from queue import Queue
from . import publication

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
    authors = Author.query.filter_by(first_name=first_name)
    author = authors.filter_by(last_name = last_name).first()
    if not author:                              
        return None
    return author
    
def create_default_author_account(first_name, last_name, email):
    password = first_name + "pass"
    return create_author(first_name, last_name, email, password)

def get_author_by_id(id):
    author = Author.query.filter_by(id=id).first()
    return author

def add_publication_to_author(id, title, field, publication_date):
    author = get_author_by_id(id)
    publication = publication.create_publication(title, field, publication_date)
    new_record = PublishingRecord(author.id, publication.id)
    db.session.add(new_record)
    db.session.commit()
    return author, publication

def author_publication_tree(id):
    author = get_author_by_id(id)
    authors = []
    publications = []
    queue = Queue()
    root = None
    return author.getPublicationTree(root, authors, publications, queue)

def delete_author(id):
    author = get_author_by_id(id)
    db.session.delete(author)
    db.session.commit()
    return True