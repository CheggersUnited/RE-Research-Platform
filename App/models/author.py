from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.node import Node

class Author(db.Model,UserMixin):
    __tablename__ = "author"
    id = db.Column("id", db.Integer, primary_key=True)
    first_name =  db.Column("first_name", db.String(60), nullable=False)
    last_name =  db.Column("last_name", db.String(60), nullable=False)
    email = db.Column("email", db.String(60), unique=True, nullable=False)
    password = db.Column("password", db.String(120), nullable=False)
    records = db.relationship("PublishingRecord", backref="author", lazy=True, cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)


    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def getPublications(self):
        publications = []
        for record in self.records:
            publications.append(self.record.publication)
        return publications

    # def getPublicationTree(self, authors, publications, queue):
    #     if self not in authors:
    #         authors.append(list(self))
    #     coauthors = []
    #     for publication in self.getPublications():
    #         if publication not in publications:
    #             publications.append(publication)
    #             coAuthors.extend(publication.getAuthors())
    #     publications.append("end")
    #     for author in coAuthors:
    #         if author not in authors:
    #             authors.append(author)
    #             queue.put(author)       #queue here is a python queue (queue.Queue)
    #     authors.append("end")
    #     if not queue.empty():
    #         authors, publications = queue.get().getPublicationTree(authors, publications, queue)
    #     return authors, publications

    def getPublicationTree(self, root, authors, publications, queue):
        if self not in authors:
            authors.append(self)
            root = Node(self, [])
        for publication in self.getPublications():
            if publication not in publications:
                publications.append(publication)
                root.children.append(Node(publication, []))
        for child in root.children:
            coAuthors = child.node.getAuthors()
            for author in coAuthors:
                if author not in authors:
                    authors.append(author)
                    child.node.children.append(author)
                    queue.put(Node(author, []))
        if not queue.empty():
            author = queue.get()
            root, authors, publications = author.node.getPublicationTree(author, authors, publications, queue)
        return root, authors, publications
        
    def toDict(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }