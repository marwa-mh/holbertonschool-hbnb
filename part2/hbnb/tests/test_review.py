import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.review import Review
from app.models.place import Place
from app.models.user import User

def test_review_creation():
    owner = User(first_name="John", last_name="Doe", email="john@example.com")
    place = Place(
        title="Cozy Apartment",
        description="Nice and clean",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    """ self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id"""
    review = Review(text="Good appartemt",rating=4, user_id=owner.id, place_id=place.id)

    assert review.text == "Good appartemt"
    assert review.place_id == place.id
    assert review.user_id==owner.id
    assert review.rating == 4
    print("Review creation test passed!")

def test_delete_review():
    # Setup
   

    owner = User("Alice", "Smith", "alice@example.com")
    place = Place(
        title="Beach House",
        description="By the sea",
        price=200,
        latitude=36.7783,
        longitude=-119.4179,
        owner=owner
    )

   

test_delete_review()
test_review_creation()
