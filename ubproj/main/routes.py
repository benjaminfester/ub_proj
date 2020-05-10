from flask import render_template, request, Blueprint
from ubproj.models import Meal
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html', title='Home')

@main.route('/about')
def about_page():
    return render_template('about.html', title='About')

@main.route('/contact')
def contact_page():
    return render_template('contact.html', title='Contant')