from flask import Blueprint, render_template

pages = Blueprint('pages', __name__, template_folder='templates')

@pages.route('/login.html')
def login_page():
    return render_template('login.html')
@pages.route('/', strict_slashes=False)
@pages.route('/index.html')
def index_page():
    return render_template('index.html')
@pages.route('/place.html')
def place_page():
    return render_template('place.html')
@pages.route('/test')
def test():
    return "Blueprint is working!"
