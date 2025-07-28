from flask import Blueprint, render_template

pages = Blueprint('pages', __name__)

@pages.route('/login.html')
def login_page():
    return render_template('login.html')
@pages.route('/')
@pages.route('/index.html')
def index_page():
    return render_template('index.html')
