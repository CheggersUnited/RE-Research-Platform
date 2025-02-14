from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for, flash
from flask_login import login_required, current_user
from App.controllers import *
import ast

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        author = authenticate(form["email"], form["password"])
        if author:
            loginuser(author,True)
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
        loginuser(author, True)
        return redirect(url_for("index_views.index_page"))
    else: 
        return render_template("signup.html")

@user_views.route("/logout",methods=["GET"])
@login_required
def logout():
    logoutuser()
    return redirect("/login")

@user_views.route("/<id>/pubtree", methods=["GET"])
@login_required
def pubtree(id):
    root, authors, publications = author_publication_tree(id)
    return render_template("pubtree.html", root=root)

@user_views.route("/author/<id>",methods=["GET"])
@login_required
def author(id):
    author = get_author_by_id(id)
    authorized = False
    if author.id == current_user.id:
        authorized = True
    publications = author.getPublications()
    return render_template("author_page.html", author=author, publications=publications, authorized=authorized) 

@user_views.route("/publication/<id>",methods=["GET"])
@login_required
def publication(id):
    publication = get_publication(id)
    authors = publication.getAuthors()
    authorized = False
    for author in authors:
        if author.id == current_user.id:
            authorized = True
    return render_template("publication_page.html", authors=authors, publication=publication, authorized=authorized)

@user_views.route("/profile", methods=["GET"])
@login_required
def profile():
    return redirect(url_for(".author", id=current_user.id))

@user_views.route("/addpublication", methods=["GET", "POST"])
@login_required
def add_publication():
    if request.method == "POST":
        data = request.form
        publication = create_publication(data["title"], data["field"], data["publication_date"])
        if not publication:
            publication = get_publication_by_title(data["title"])
            if publication in current_user.getPublications():
                flash("Publication already added.")
            else:
                if not publication.getAuthors():
                    publication = add_authors_to_publication(publication.id, [{"first_name":current_user.first_name, "last_name":current_user.last_name, "email":current_user.email}])
                    flash("Publication Added.")
                else:
                    flash("Publication exists. Must request author permission to add.")
            return redirect("/profile")
        return redirect(url_for(".add_authors", id=publication.id))
    else:
        fields = [  "Climate Change", "Cancer Research", "Music Therapy", "Ocean Acidification", 
                    "Urban Development", "Mental Health", "Sustainable Agriculture"]
        return render_template("add_publication.html", fields=fields)

@user_views.route("/<id>/addauthors", methods=["GET", "POST"])
@login_required
def add_authors(id):
    if request.method == "POST":
        authors = []
        pub_authors = get_publication(id).getAuthors()
        for fname, lname, email in zip( request.form.getlist("fname"),
                                        request.form.getlist("lname"),
                                        request.form.getlist("email")):
            author = {"first_name": fname, "last_name": lname, "email": email}
            if(len(author["first_name"]) != 0 and len(author["last_name"])  !=0 and len(author["email"])!=0):
                authors.append(author)
        current_auth = current_user._get_current_object()
        author = { 
                    "first_name": current_auth.first_name, 
                    "last_name": current_auth.last_name,
                    "email":current_auth.email
                }
        authors.append(author)
        publication = add_authors_to_publication(id, authors)
        return redirect("/publication/{}".format(publication.id))
    else:
        return render_template("add_author.html", id=id)

@user_views.route("/authors", methods=["GET"])
@login_required
def all_authors():
    items = get_all_authors()
    heading = 'Authors'
    list_type = 'Author'
    return render_template("list.html", items=items, heading=heading, list_type=list_type)

@user_views.route("/publications", methods=["GET"])
@login_required
def all_publications():
    items = get_all_publications()
    heading = 'Publications'
    list_type = 'Publication'
    return render_template("list.html", items=items, heading=heading, list_type=list_type)