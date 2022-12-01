from flask_jwt import JWT
from App.models.author import Author

def authenticate(username, password):
    author = Author.query.filter_by(email=username).first()
    if author and author.check_password(password):
        return author
    return None

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return Author.query.get(payload['identity'])

def setup_jwt(app):
    return JWT(app, authenticate, identity)