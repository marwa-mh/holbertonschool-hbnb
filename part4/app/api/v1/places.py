from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade  # same object created in init file, not a class


api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    #'owner_id': fields.String(required=True, description='ID of the place owner'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# format the response
def format_place_response(place):
    """Helper function to format place response with embedded objects"""
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': float(place.price),
        'latitude': place.latitude,
        'longitude': place.longitude,
        'city': 'Melbourne',  # Pretend city
        'picture_url': 'static/images/place1.png',  # Placeholder image
        'amenities': [
            {
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities_r
        ] if place.amenities_r else [],
        'created_at': place.created_at.isoformat(),
        'updated_at': place.updated_at.isoformat()
    }

# /places
@api.route('/')
class PlaceList(Resource):
    # create a new place with post
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    @jwt_required()
    def post(self):
        """Create a new place"""
        place_data = api.payload
        current_user = get_jwt_identity()  # Get user info from token

        # Inject user ID into the data before passing to the facade
        place_data['owner_id'] = current_user['id']
        
        try:
            # Let facade handle all validation logic
            new_place = facade.create_place(place_data)
            return format_place_response(new_place), 201
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            if "not found" in str(e).lower():
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400

    # get all places with get
    @api.response(200, 'List of places retrieved successfully')
    @api.response(500, 'Internal server error')
    def get(self):
        """Retrieve all places"""
        try:
            places = facade.get_all_places()
            return [format_place_response(place) for place in places], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500

# specific place: /places/<place_id>
@api.route('/<place_id>')
class Place(Resource):
    # get request to retrieve that place info
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return format_place_response(place), 200

    # put request to update place info
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        current_user = get_jwt_identity()  # Get user info from token
        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
       
        try:
            # Let facade handle all validation and business logic
            updated_place = facade.update_place(place_id, place_data)
            return format_place_response(updated_place), 200
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            if "not found" in str(e).lower():
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400

# get reviews in a specific place
@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')

    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            # First check if the place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Get all reviews for this place
            reviews = facade.get_reviews_by_place(place_id)
            return [{'id': review.id,
                     'text':review.text,
                       'place_id': review.place_id,
                        'user_id': review.user_id,
                        'rating': review.rating,
                        'created_at': review.created_at.isoformat() if review.created_at else None,
                        'user_name': review.user_r.first_name + " " + review.user_r.last_name if review.user_r else None
                           } for review in reviews], 200
        except Exception as e:
            return {'error': str(e)}, 500

