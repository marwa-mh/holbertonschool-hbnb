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
from datetime import timedelta
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

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', prefix='/api/v1', doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_api, path='/users')
    api.add_namespace(amenities_api, path='/amenities')
    api.add_namespace(places_api, path='/places')
    api.add_namespace(reviews_api, path='/reviews')
    api.add_namespace(auth_api, path="/auth")
    api.add_namespace(protected_api, path="")
    bcrypt = Bcrypt()
    bcrypt.init_app(app)
    # Load JWT secret key from environment variables
    jwt_secret_key = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret_key:
        raise ValueError("No JWT_SECRET_KEY set for Flask application")
    app.config['JWT_SECRET_KEY'] = jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager()
    jwt.init_app(app)

    #for part 4
    app.register_blueprint(pages)
    
    # Enable CORS for all routes and origins
    CORS(app)
    return app