import uuid
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
class User:
    def __init__(self, first_name, last_name, email, is_admin):
        if not all([first_name, last_name, email]):
            raise ValueError("Required attribute not specified!")
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.reviews = []

    #-------------- Properties ------------
    #first_name
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if 0 < len(value.strip()) <= 50:
            self._first_name = value.strip()
        else:
            raise ValueError("Invalid first name length")
    
    #last_name
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if 0 < len(value.strip()) <= 50:
            self._last_name = value.strip()
        else:
            raise ValueError("Invalid last name length")
    
    #email
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not isinstance(value, str) or not EMAIL_REGEX.fullmatch(value):
            raise ValueError("Invalid email address")
        self._email = value
    
    #is_admin
    @property
    def is_admin(self):
        return self._is_admin()   
    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("The type must be boolean")
        self._is_admin = value

    # -- Methods --
    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
