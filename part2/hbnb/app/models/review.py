import uuid
from datetime import datetime
from app.models.user import User
from app.models.place import Place
class Review:
    def __init__(self, text, rating,place_id, user_id):
        if not all([text, rating,place_id, user_id]):
            raise ValueError("Required attribute not specified!")
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        

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
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        if not value:
            raise ValueError("user_id is required")
        
        self._user_id = value
    
    #place
    @property
    def place_id(self):
        return self._place_id
    
    @place_id.setter
    def place_id(self, value):
        if not value:
            raise ValueError("place_id is required")
        
        self._place_id = value
    
    # -- Methods --
    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
