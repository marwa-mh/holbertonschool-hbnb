import uuid
from datetime import datetime
from app.models.user import User
from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship

# junction table for many-to-many relationship
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.String(1024), nullable=True)
    _price = db.Column('price', db.Numeric(10, 2), nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=True)
    _longitude = db.Column('longitude', db.Float, nullable=True)
    _owner_id = db.Column('owner_id', db.ForeignKey('users.id'), nullable=False)

    # Relationship with Amenity (many-to-many)
    amenities_r = db.relationship("Amenity", secondary="place_amenity", back_populates="places_r")

    # Relationship with Review (one-to-many)
    reviews_r = db.relationship("Review", back_populates="place_r", cascade="all, delete-orphan", lazy=True)

    # Relationship with User (many-to-one)
    user_r = db.relationship("User", back_populates="places_r")

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
        db.session.commit()

    def add_review(self, review):
        """Add a review to this place"""
        if review not in self.reviews_r:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if amenity not in self.amenities_r:
            self.amenities_r.append(amenity)