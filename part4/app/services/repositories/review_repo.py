from app.persistence.repository import SQLAlchemyRepository
from app.models import Review

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_by_user_and_place(self, user_id, place_id):
        """Find a review by a specific user for a specific place."""
        return self.model.query.filter_by(user_id=user_id, place_id=place_id).first()