from flask import Flask
from flask_restx import Api
from config import config
from app.extensions import db
from app.api.v1.users import api as users_api
from app.api.v1.amenities import api as amenities_api
from app.api.v1.places import api as places_api
from app.api.v1.reviews import api as reviews_api

def create_app(config_class=config['development']):
    app = Flask(__name__)

    # Database configuration
    USER = "hbnb_p3"
    PWD = "p3_pw"
    HOST = "localhost"
    DB = "hbnb_p3_db"

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

    return app