import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.amenity import Amenity
from app.models.place import Place
from app.models.user import User

def test_amenity_creation():
    owner = User(first_name="John", last_name="Doe", email="john@example.com")
    place = Place(
        title="Cozy Apartment",
        description="Nice and clean",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    amenity = Amenity(name="Wi-Fi", place=place)

    assert amenity.name == "Wi-Fi"
    assert amenity.place == place
    print("Amenity creation test passed!")

test_amenity_creation()
