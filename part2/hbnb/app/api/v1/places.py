from flask_restx import Namespace, Resource, fields
from app.services.facade import shared_facade as facade

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the place owner'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

# /places
@api.route('/')
class PlaceList(Resource):
    # create a new place with post
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Create a new place"""
        place_data = api.payload

        try:
            # Let facade handle all validation logic
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id,
                'amenities': [amenity.id for amenity in new_place.amenities] if new_place.amenities else [],
                'created_at': new_place.created_at.isoformat(),
                'updated_at': new_place.updated_at.isoformat()
            }, 201
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
            return [
                {
                    'id': place.id,
                    'title': place.title,
                    'description': place.description,
                    'price': place.price,
                    'latitude': place.latitude,
                    'longitude': place.longitude,
                    'owner_id': place.owner.id,
                    'amenities': [amenity.id for amenity in place.amenities] if place.amenities else []
                } for place in places
            ], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500

# specific place /places/<place_id>
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
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,
            'amenities': [amenity.id for amenity in place.amenities] if place.amenities else [],
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat()
        }, 200

    # put request to update place info
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        try:
            # Let facade handle all validation and business logic
            updated_place = facade.update_place(place_id, place_data)
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner.id,
                'amenities': [amenity.id for amenity in updated_place.amenities] if updated_place.amenities else [],
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }, 200
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            if "not found" in str(e).lower():
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400