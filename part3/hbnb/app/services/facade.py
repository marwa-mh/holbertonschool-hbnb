from app.persistence.repository import SQLAlchemyRepository
from app.models import User, Place, Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository()
        self.place_repo = SQLAlchemyRepository()
        self.review_repo = SQLAlchemyRepository()
        self.amenity_repo = SQLAlchemyRepository()

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


    ### for /places
    def create_place(self, place_data):
        """Create a new place with owner and amenities"""
        # Get the owner first to validate it exists
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")

        # transform owner_id to owner to mactch with Place Model
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        # Handle amenities if provided
        amenity_objects = []
        amenity_ids = place_data.get('amenities', [])

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            amenity_objects.append(amenity)

        # Create new place instance with owner object
        place_data_with_owner = {
            'title': place_data.get('title'),
            'description': place_data.get('description'),
            'price': place_data.get('price'),
            'latitude': place_data.get('latitude'),
            'longitude': place_data.get('longitude'),
            'owner': owner  # Pass the User object, not the ID
        }

        # unpacks dictionaries into keyword arguments
        place = Place(**place_data_with_owner)

        # Add amenities to the place
        for amenity in amenity_objects:
            place.add_amenity(amenity)

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

        # Handle owner update if provided
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            # Update the owner object, not just the ID
            place_data['owner'] = owner
            # Remove owner_id since the model uses 'owner' attribute
            del place_data['owner_id']

        # Handle amenities update if provided
        if 'amenities' in place_data:
            amenity_objects = []
            amenity_ids = place_data['amenities']

            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
                amenity_objects.append(amenity)

            # Replace the entire amenities ID list with objects to match Place Model
            place.amenities = amenity_objects
            # Remove amenities from update data since we transformed to amenity_objects above
            del place_data['amenities']

        # Update other place attributes using the model's update method
        place.update(place_data)

        # Update the place in repository
        self.place_repo.update(place_id, place_data)

        return place


    ### for reviews
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        from app.models.review import Review

        # Validate user_id
        existing_user = self.user_repo.get(review_data.get('user_id'))
        if not existing_user:
            raise ValueError("user not exist!")
        # Validate place_id
        existing_place = self.place_repo.get(review_data.get('place_id'))
        if not existing_place:
            raise ValueError("place not exist!")

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
        reviews = self.review_repo.get_all_by_attribute("place_id", place_id)
        print(f"DEBUG: Found {len(reviews)} reviews for place {place_id}")
        return reviews

    def update_review(self, review_id, review_data):

        review = self.review_repo.get(review_id)

        if review.place_id != review_data['place_id']:
            raise ValueError("You are not allowed to change the review")
        if review.user_id != review_data['user_id']:
            raise ValueError("You are not allowed to change the review")

        # Update the review in repository
        self.review_repo.update(review_id, review_data)

        return review

    def delete_review(self, review_id):
        if not review_id:
            raise ValueError("Review id is required")
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
        else:
            raise ValueError("Review not found")
