from app.services.repositories.user_repo import UserRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models import User, Place, Amenity, Review
from sqlalchemy.exc import IntegrityError

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    ### for /users
    def create_user(self, user_data):
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required")

        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

        # Extract password and remove it from user_data
        password = user_data.pop('password', None)
        if not password:
            raise ValueError("Password is required")

        # Create new user instance
        user = User(**user_data, password=password)

        try:
            self.user_repo.add(user)
        except IntegrityError:
            from app.extensions import db
            db.session.rollback()
            raise ValueError("Email already registered")

        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

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

        user.update(user_data)  # Use update() in User model
        return user

    ### for /amenities
    def create_amenity(self, amenity_data):

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
        return amenity

    ### for /places
    def create_place(self, place_data):
        """Create a new place with owner and amenities"""
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        # Handle amenities if provided
        amenities = [self.get_amenity(aid) for aid in place_data.get('amenities', [])]
        if None in amenities:
            raise ValueError("One or more amenities not found")

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=owner.id
        )

        place.amenities = amenities

        # Add place to repository
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        # Get the existing place
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # Handle owner_id update if provided
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")

        # Handle amenities update if provided
        if 'amenities' in place_data:
            amenities = [self.get_amenity(aid) for aid in place_data['amenities']]
            if None in amenities:
                raise ValueError("One or more amenities not found")
            # Replace the entire amenities ID list with objects to match Place Model
            place.amenities_r = amenities
            # Remove amenities key from update data
            del place_data['amenities']

        # Update other place attributes using the model's update method
        place.update(place_data)
        return place

    ### for reviews
    def create_review(self, review_data):

        # Validate user_id
        existing_user = self.user_repo.get(review_data.get('user_id'))
        if not existing_user:
            raise ValueError("user not exist!")

        # Validate place_id
        existing_place = self.place_repo.get(review_data.get('place_id'))
        if not existing_place:
            raise ValueError("place not exist!")

        # Prevent owner from reviewing their own place
        if existing_place.owner_id == existing_user.id:
            raise ValueError("Owners cannot review their own places")

         # Create new user instance
        review = Review(**review_data)

        # Add user to repository
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews_r  # based on the relationship

    def update_review(self, review_id, review_data):

        review = self.review_repo.get(review_id)

        if not review:
            raise ValueError("Review not found")

        if review.place_id != review_data['place_id'] or review.user_id != review_data['user_id']:
            raise ValueError("You are not allowed to change the review")

        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
