from App.models import Publication,PublishingRecord
from App.database import db
from . import author

def create_publication(title, field, publication_date, authors):
    new_publication = Publication(title, field, publication_date)
    db.session.add(new_publication)
    db.session.commit()
    for auth in authors:
        exists = author.get_author_by_name(auth.first_name,auth.last_name)
        if exists == None:
            new_author = author.create_default_author_account(auth.first_name, auth.last_name)
            new_record = PublishingRecord(new_author.id, new_publication.id)
            db.session.add(new_author)
        else:
            new_record = PublishingRecord(exists.id, new_publication.id)
        db.session.add(new_record)
    db.session.commit()
    return new_publication


def get_publication_by_title(title):
    return Publication.query.filter_by(title=title).first()

def get_publication(id):
    return Publication.query.get(id)

def get_all_publications():
    return Publication.query.all()

def get_publication_by_field(field):
    return Publication.query.filter_by(field=field).all()

#TO REMOVE
# def get_all_publications_json():
#     publications = Publication.query.all()
#     if not publications:
#         return []
#     publications = [publication.toJSON() for publication in publications]
#     return publications