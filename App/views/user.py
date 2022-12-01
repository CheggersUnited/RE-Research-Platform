from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for, flash, session
from flask_jwt import jwt_required, current_identity
from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        author = get_author_by_id(1)
        if author:
            return redirect(url_for("index_views.index_page"))
        else:
            flash("Invalid email or password.")
            return render_template("login.html")
    return render_template("login.html")

@user_views.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form = request.form
        author = create_author(form["fname"], form["lname"], form["email"], form["password"])
        if not author:
            flash("Author already exists.")
            return render_template("signup.html")
        flash("Author account succesfully created.")
        return redirect(url_for("index_views.index_page"))
    else: 
        return render_template("signup.html")

@user_views.route("/<id>/pubtree", methods=["GET"])
def pubtree(id):
    root, authors, publications = author_publication_tree(id)
    return render_template("pubtree.html", root=root)

@user_views.route("/author/<id>",methods=["GET"])
def author(id):
    author = get_author_by_id(id)
    publications = author.getPublications()
    return render_template("author_page.html", author = author, publications=publications) #Change to author template

@user_views.route("/profile", methods=["GET"])
def profile():
    return redirect(url_for(".author"), id=current_identity.id)

@user_views.route("/publication/<id>", methods=["GET"])
def publication(id):
    publication = get_publication(id)
    return render_template("publication_page.html", publication=publication)

@user_views.route("/addpublication", methods=["GET", "POST"])
def add_publication():
    if request.method == "POST":
        # data = request.get_data()
        # session["data"] = data
        print("testing 2 yes")
        return redirect(url_for(".add_publication"))
    else:
        fields = [  "Climate Change", "Cancer Research", "Music Therapy", "Ocean Acidification", 
                    "Urban Development", "Mental Health", "Sustainable Agriculture"]
        return render_template("add_publication.html", fields=fields)

@user_views.route("/addauthors", methods=["GET", "POST"])
def add_authors():
    if request.method == "POST":
        authors = []
        for fname, lname, email in zip( request.form.getlist("fname"),
                                        request.form.getlist("lname"),
                                        request.form.getlist("email")):
            author = {"first_name": fname, "last_name": lname, "email": email}
            authors.append(author)
        # data = session["data"]
        publication = create_publication(data["title"], data["field"], data["publication_date"], authors)
        return redirect(url_for(".author"), id=current_identity.id)
    else:
        
        print("testig")
        return render_template("add_author.html")
