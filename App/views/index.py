from flask import Blueprint, redirect, render_template, request, send_from_directory,url_for
from flask_login import login_required

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    fields = [  "Climate Change", "Cancer Research", "Music Therapy", "Ocean Acidification", 
                "Urban Development", "Mental Health", "Sustainable Agriculture"]
    return render_template('index.html', fields=fields)