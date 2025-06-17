from app.persistence.repository import InMemoryRepository
from app.models import User, Place, Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    ### for /users
    def create_user(self, user_data):
        # Validate email uniqueness
        existing_user = self.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValueError("Email already registered")

        # Create new user instance
        user = User(**user_data)

        # Add user to repository
        self.user_repo.add(user)

        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        # Get the existing user
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        # Check if email is being updated and if it's already taken by another user
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        # Update user attributes
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        # Update the user in repository
        self.user_repo.update(user_id, user_data)

        return user

    ### for /amenities
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        from app.models.amenity import Amenity

        # Create new amenity instance (only needs name)
        amenity = Amenity(name=amenity_data.get('name'))

        # Add amenity to repository
        self.amenity_repo.add(amenity)

        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        # Get the existing amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        # Update amenity attributes using the model's update method
        amenity.update(amenity_data)

        # Update the amenity in repository
        self.amenity_repo.update(amenity_id, amenity_data)

        return amenity


    ### for /places -> handle later
    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        place: Place = self.place_repo.get(place_id)
        if place:
            place.reviews = self.review_repo.get_by_attribute('place_id', place_id)