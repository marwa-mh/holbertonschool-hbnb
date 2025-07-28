from flask import Flask
from flask_restx import Api
from config import config
from app.extensions import db
from app.api.v1.users import api as users_api
from app.api.v1.amenities import api as amenities_api
from app.api.v1.places import api as places_api
from app.api.v1.reviews import api as reviews_api
from app.api.v1.auth import api as auth_api
from app.api.v1.protected import api as protected_api
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.routes import pages
from flask_cors import CORS
load_dotenv()

def create_app(config_class=config['development']):
    #app = Flask(__name__)
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Database configuration
    USER = os.getenv("HBNB_MYSQL_USER")
    PWD = os.getenv("HBNB_MYSQL_PWD")
    HOST = os.getenv("HBNB_MYSQL_HOST")
    DB = os.getenv("HBNB_MYSQL_DB")

    # Configure SQLAlchemy to connect SQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    db.init_app(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_api, path='/api/v1/users')
    api.add_namespace(amenities_api, path='/api/v1/amenities')
    api.add_namespace(places_api, path='/api/v1/places')
    api.add_namespace(reviews_api, path='/api/v1/reviews')
    api.add_namespace(auth_api, path="/api/v1/auth")
    api.add_namespace(protected_api, path="/api/v1")
    bcrypt = Bcrypt()
    bcrypt.init_app(app)
    app.config['SECRET_KEY'] = 'c0535e4e95d52a0d4fc8f92ebd465d59b86c87d19f5d0e6c5f4ea8d8e2fcb61d'
    jwt = JWTManager()
    jwt.init_app(app)

    #for part 4
    app.register_blueprint(pages)
    # Enable CORS for all routes and origins
    CORS(app)
    return app