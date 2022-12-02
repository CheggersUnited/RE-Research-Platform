from flask import Blueprint, redirect, render_template, request, send_from_directory,url_for
from flask_login import login_required
from App.controllers import get_publications_by_field

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET', 'POST'])
@login_required
def index_page():
    field = request.args.get('field')
    search_type = request.args.get('search_type')
    data = request.form
    if data:
        print(data['search'])
        

    if search_type == None:
        search_type = True
    
    publications = []
    if field:
        print(field)
        publications = get_publications_by_field(field)
        print(publications)
    fields = [  "Climate Change", "Cancer Research", "Music Therapy", "Ocean Acidification", 
                "Urban Development", "Mental Health", "Sustainable Agriculture"]
    return render_template('index.html', fields=fields, publications=publications, search_type=search_type)