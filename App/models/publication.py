from App.database import db
from flask_sqlalchemy import ForeignKey

class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(120), nullable=False, unique=True)
    field = db.Column("field", db.String(60), nullable=False)
    publication_date = db.Column("publication_date", db.DateTime, nullable=False)
    records = db.relationship("PublishingRecord", backref="publication", lazy=True, cascade="all, delete-orphan")

    def __init__(self ,title, fields, publication_date):
        self.title = title
        self.field = field
        self.publication_date = publication_date

    def getAuthors(self):
        authors = []
        for record in records:
            authors.append(record.author)
        return authors
    
    def toDict(self):
        return{
            "id": self.id,
            "title": self.title,
            "field": self.field,
            "publication_date": self.publication_date
        }

