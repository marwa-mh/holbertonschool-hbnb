import uuid
from datetime import datetime
from app.models.place import Place

class Amenity:
    def __init__(self, name, place):
        if name is None or place is None:
            raise ValueError("Required attribute not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.place = place

    #-------------- Properties ------------
    #name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(value.strip()) > 0:
            self._name = value.strip()
        else:
            raise ValueError("name is required")

    #place
    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise ValueError("Invalid object type passed in for place!")
        self._place = value
    # -- Methods --
    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

