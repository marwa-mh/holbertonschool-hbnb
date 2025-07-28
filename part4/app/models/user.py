import uuid
from datetime import datetime
import re
from app.extensions import db, bcrypt
from .base_model import BaseModel
from sqlalchemy.orm import relationship


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class User(BaseModel):
    __tablename__ = 'users'

    # specify explicit column names to avoid underscore prefixes
    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), unique=True, nullable=False)
    _password= db.Column('password', db.String(128), nullable=False)
    _is_admin = db.Column('is_admin',db.Boolean, default=False)

    # Relationship with Review (one-to-many):
    reviews_r = relationship("Review", back_populates="user_r", cascade="all, delete-orphan", lazy=True)

    # Relationship with Place (one-to-many):
    places_r = relationship("Place", back_populates="user_r", cascade="all, delete-orphan", lazy=True)


    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()  # Let BaseModel handle id and timestamps

        if not all([first_name, last_name, email]):
            raise ValueError("Required attribute not specified!")

        # self.id = str(uuid.uuid4())
        # self.created_at = datetime.now()
        # self.updated_at = datetime.now() >> handled by BaseModel
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin

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
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("The type must be boolean")
        self._is_admin = value

    #password
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if 0 < len(value.strip()) <= 128:
            self._password = value.strip()
        else:
            raise ValueError("Invalid password length")
    # -- Utinity Methods --
    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        print("Password hashed")

    def verify_password(self, password):
        """Verify the hashed password."""
        print('self.password='+self.password +', password='+password)
        return bcrypt.check_password_hash(self.password, password)

    # --Business Logic methods--
    def save(self):
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
        db.session.commit()
