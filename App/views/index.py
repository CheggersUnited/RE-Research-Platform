from flask import Blueprint, redirect, render_template, request, send_from_directory,url_for, flash
from flask_login import login_required
from App.controllers import get_publications_by_field, author_search, publication_search

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
@login_required
def index_page():
    field = request.args.get('field')
    search_type = request.args.get('search_type')
    search = request.args.get('search')

    search_results = []
    if search:
        if search_type == 'Publication':
            search_results = publication_search(search)
        else:
            search_results = author_search(search)
    
    if search_results == None:
        flash("No results obtained.")
        search_results = []
    elif search_results == 'Invalid':
        flash("Invalid Search")
        search_results = []
    
    if search_type == None:
        search_type = 'Author'
    
    publications = []
    if field:
        publications = get_publications_by_field(field)

    fields = [  "Climate Change", "Cancer Research", "Music Therapy", "Ocean Acidification", 
                "Urban Development", "Mental Health", "Sustainable Agriculture"]
    return render_template('index.html', fields=fields, publications=publications, search_type=search_type, search_results=search_results)