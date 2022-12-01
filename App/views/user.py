from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for, flash
from flask_login import login_required
from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.get_json()
        author = authenticate(form["email"], form["password"])
        if author:
            loginuser(author,True)
            return render_template("index.html")
        else:
            flash("Invalid email or password.")
            return render_template("login.html")
    else:
        return render_template("login.html")

@user_views.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form = request.get_json()
        author = create_author(form["fname"], form["lname"], form["email"], form["password"])
        if not author:
            flash("Author already exists.")
            return render_template("signup.html")
        else:
            flash("Author account succesfully created.")
            return render_template("index.html")

@user_views.route("/logout",methods=["GET"])
@login_required
def logout():
    logoutuser()
    redirect("/login")

@user_views.route("/<id>/pubtree", methods=["GET"])
@login_required
def pubtree(id):
    root, authors, publications = author_publication_tree(id)
    return render_template("pubtree.html", root=root)


@user_views.route("/<id>",methods=["GET"])
@login_required
def author(id):
    author = get_author_by_id(id)
    return render_template("author_page.html",author = author)


@user_views.route("/addpublication", methods=["GET", "POST"])
@login_required
def add_publication():
    if request.method == "POST":
        data = request.get_json()
        return redirect((url_for(".add_authors")), data=data)
    else:
        fields = [  "Climate Change", "Cancer Research", "Music Therapy", "Ocean Acidification", 
                    "Urban Development", "Mental Health", "Sustainable Agriculture"]
        render_template("add_publication.html", fields=fields)


@user_views.route("/addauthors", methods=["GET", "POST"])
@login_required
def add_authors():
    if request.method == "POST":
        data = request.args.get("data", None)
        authors = []
        for fname, lname, email in zip( request.form.getlist("fname"),
                                        request.form.getlist("lname"),
                                        request.form.getlist("email")):
            author = {"first_name": fname, "last_name": lname, "email": email}
            authors.append(author)
        publication = create_publication(data["title"], data["field"], data["publication_date"], authors)
        return redirect(url_for(".author"), id=current_identity.id)
    else:
        return render_template("add_author.html")
