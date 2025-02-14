from flask_login import login_user, logout_user,LoginManager
from App.models.author import Author
from flask import redirect,render_template,url_for

login_manager = LoginManager()

@login_manager.user_loader
def load_user(author_id):
    return Author.query.get(author_id)

@login_manager.unauthorized_handler
def no_authorization():
    return redirect("/login")

def authenticate(username, password):
    author = Author.query.filter_by(email=username).first()
    if author and author.check_password(password):
        return author
    return None

def loginuser(author, remember):
    return login_user(author, remember=remember)

def logoutuser():
    logout_user()

# Payload is a dictionary which is passed to the function by Flask JWT
# def identity(payload):
#     return Author.query.get(payload['identity'])

# def setup_jwt(app):
#     return JWT(app, authenticate, identity)