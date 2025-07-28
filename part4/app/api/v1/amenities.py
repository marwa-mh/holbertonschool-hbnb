from flask_restx import Namespace, Resource, fields
from app.services import facade  # same object created in init file, not a class
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# /amenities
@api.route('/')
class AmenityList(Resource):
    # create a new amenity with post
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        
        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        """Create a new amenity"""
        amenity_data = api.payload

        try:
            # Let facade handle all validation logic
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat()
            }, 201
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            return {'error': str(e)}, 400

    # get all amenities with get
    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(500, 'Internal server error')
    def get(self):
        """Retrieve all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [
                {
                    'id': amenity.id,
                    'name': amenity.name,
                    'created_at': amenity.created_at.isoformat(),
                    'updated_at': amenity.updated_at.isoformat()
                } for amenity in amenities
            ], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500

# specific amenity /amenities/<amenity_id>
@api.route('/<amenity_id>')
class Amenity(Resource):
    # get request to retrieve that amenity info
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }, 200

    # put request to update amenity info
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        
        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        """Update an amenity's information"""
        amenity_data = api.payload

        try:
            # Let facade handle all validation and business logic
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat(),
                'updated_at': updated_amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            if "not found" in str(e).lower():
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400