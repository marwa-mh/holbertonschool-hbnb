import uuid
from datetime import datetime
from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    _name = db.Column('name', db.String(128), nullable=False)

    # Relationship with Place (many-to-many)
    places_r = relationship("Place", secondary="place_amenity", back_populates="amenities_r")


    def __init__(self, name):
        if not name or not name.strip():
            raise ValueError("Name is required")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name.strip()

    # -------------- Properties ------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value and len(value.strip()) > 0:
            self._name = value.strip()
        else:
            raise ValueError("Name is required")

    # -- Methods --
    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp