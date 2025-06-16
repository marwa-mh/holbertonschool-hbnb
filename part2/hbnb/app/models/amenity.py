import uuid
from datetime import datetime


class Amenity:
    def __init__(self, name):
        if name is None:
            raise ValueError("Required attribute not specified!")
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.places = []

    #-------------- Properties ------------
    #name
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if 0 < len(value.strip()):
            self._name = value.strip()
        else:
            raise ValueError("name is required")
        
    # -- Methods --
    def save(self):
        self.updated_at = datetime.now()
    
    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

