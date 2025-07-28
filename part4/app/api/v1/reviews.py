from flask_restx import Namespace, Resource, fields
from app.services import facade  # same object created in init file, not a class
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    #'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()  # Get user info from token
        # Inject user ID into the data before passing to the facade
        review_data['user_id'] = current_user['id']
        try:
            # Let facade handle all validation logic
            review = facade.create_review(review_data)
            return {'id': review.id, 'place_id': review.place_id, 'user_id': review.user_id, 'text': review.text, 'rating': review.rating, 'created_at':review.created_at.isoformat(), 'updated_at':review.updated_at.isoformat()}, 201
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return [{'id': review.id,'text': review.text, 'place_id': review.place_id, 'user_id': review.user_id, 'rating': review.rating} for review in reviews], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    # get review with ID
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id,'text':review.text,'place_id': review.place_id, 'user_id': review.user_id, 'rating': review.rating}, 200

    # update a review with ID
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        current_user = get_jwt_identity()  # Get user info from token
        review = facade.get_review(review_id)
        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            # Let facade handle all validation and business logic
            updated_review = facade.update_review(review_id, review_data)
            return {'id': updated_review.id,'place_id': updated_review.place_id, 'user_id': updated_review.user_id, 'rating': updated_review.rating, 'text': updated_review.text, 'created_at': updated_review.created_at.isoformat(), 'updated_at': updated_review.updated_at.isoformat()}, 200
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            if "not found" in str(e).lower():
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400

    # delete a review
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()  # Get user info from token
        review = facade.get_review(review_id)
        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        try:
            facade.delete_review(review_id)
            return ("Review deleted successfully")
        except Exception as e:
            return {'error': str(e)}, 404
