from flask_restx import Namespace, Resource, fields
from app.services import facade  # same object created in init file, not a class
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(required=False, default=False, description='Admin status'),
    'places': fields.List(fields.String, required=False, description='List of user places'),
    'password': fields.String(required=True, description='Password of the user')
})

# /users
@api.route('/')
class UserList(Resource):
    # create a new user with post
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    # @jwt_required()
    def post(self):
        # current_user = get_jwt_identity()

        # If 'is_admin' is part of the identity payload

        # if not current_user.get('is_admin'):
        #    return {'error': 'Admin privileges required'}, 403
        # """Register a new user"""
        user_data = api.payload
        # print(user_data)
        try:
            # Let facade handle all validation logic
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name}, 201
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            return {'error': str(e)}, 400

    # get all users with get
    @api.response(200, 'List of users retrieved successfully')
    @api.response(500, 'Internal server error')
    def get(self):
        """ Retrieve all users"""
        try:
            users = facade.get_all_users()
            return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500

# specific user /users/<user_id>
@api.route('/<user_id>')
class User(Resource):
    # get request to retrieve that user info
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    # put request to update user info
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update a user's information"""
        current_user = get_jwt_identity()  # Get user info from token
        # Only allow non-admins to update their own profile
        if not current_user.get('is_admin') and user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        is_admin = current_user.get('is_admin', False)

        try:
            # Let facade handle all validation and business logic
            updated_user = facade.update_user(user_id, user_data, is_admin)
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            if "not found" in str(e).lower():
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400

    @api.response(204, 'User deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user (admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            facade.delete_user(user_id)
            return '', 204
        except ValueError as e:
            return {'error': str(e)}, 404
