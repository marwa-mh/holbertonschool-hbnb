import uuid
from datetime import datetime
from app.models.user import User
class Place:
    def __init__(self, title, description, price, latitude,
                 longitude, owner):
        if not all([title, price, latitude, longitude, owner]):
            raise ValueError("Required attribute not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
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

    #owner
    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise ValueError("Invalid object type passed in for owner!")
        self._owner = value

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