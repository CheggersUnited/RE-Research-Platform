from App.models import Publication,PublishingRecord
from App.database import db
from . import author

def create_publication(title, field, publication_date, authors):
    pub = Publication.query.filter_by(title=title).first()
    if pub:
        return None

    new_publication = Publication(title, field, publication_date)
    db.session.add(new_publication)
    db.session.commit()
    return add_authors_to_publication(new_publication, authors)

def add_authors_to_publication(publication, authors):
    for auth in authors:
        exists = author.get_author_by_name(auth["first_name"],auth["last_name"])
        if exists == None:
            new_author = author.create_default_author_account(auth["first_name"],auth["last_name"], auth["email"])
            new_record = PublishingRecord(new_author.id, publication.id)
        else:
            new_record = PublishingRecord(exists.id, publication.id)
    db.session.add(new_record)
    db.session.commit()
    return publication

def get_publication_by_title(title):
    return Publication.query.filter_by(title=title).first()

def get_publication(id):
    return Publication.query.get(id)

def get_all_publications():
    return Publication.query.all()

def get_publication_by_field(field):
    return Publication.query.filter_by(field=field).all
