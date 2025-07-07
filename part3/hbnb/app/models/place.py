import uuid
from datetime import datetime
from app.models.user import User
from app.extensions import db
from .base_model import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.String(1024), nullable=True)
    _price = db.Column('price', db.Numeric(10, 2), nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=True)
    _longitude = db.Column('longitude', db.Float, nullable=True)
    _owner_id = db.Column('owner_id', db.ForeignKey('users.id'), nullable=False)


    # Define relationship to User model later to get owner


    def __init__(self, title, description, price, latitude,
                 longitude, owner_id):
        if not all([title, price, latitude, longitude, owner_id]):
            raise ValueError("Required attribute not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    #-------------- Properties ------------
    #title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if 0 < len(value.strip()) <= 100:
            self._title = value.strip()
        else:
            raise ValueError("Title must be between 1 and 100 characters")

    #description
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        # Description can be empty/None (optional field)
        if value is None:
            self._description = ""
        else:
            self._description = value.strip() if hasattr(value, 'strip') else str(value)

    #price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not (isinstance(value, (int, float))) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)

    #latitude
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    #longitude
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    #owner_id
    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not value:
            raise ValueError("Owner ID is required")

        # Validate that the owner exists in the database
        if not User.query.get(value):
            raise ValueError(f"User with ID {value} does not exist")

        self._owner_id = value

    # -- Methods --
    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def add_review(self, review):
        """Add a review to this place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)