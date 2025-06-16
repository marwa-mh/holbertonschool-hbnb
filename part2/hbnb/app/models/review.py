import uuid
from datetime import datetime
from app.models.user import User
from app.models.place import Place
class Review:
    def __init__(self, text, rating,place, user):
        if not all([text, rating,place, user]):
            raise ValueError("Required attribute not specified!")
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place
        

    #-------------- Properties ------------
    #text
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        if 0 < len(value.strip()):
            self._text = value.strip()
        else:
            raise ValueError("text is required")
    
    #rating
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not( 1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5 and integer number")
        self._rating = int(value)
    
    
    #user
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise ValueError("Invalid object type passed in for user!")
        self._user = value
    
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
