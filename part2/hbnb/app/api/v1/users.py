from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# /users
@api.route('/')
class UserList(Resource):
    # create a new user with post
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

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
    def put(self, user_id):
        """Update a user's information"""
        user_data = api.payload

        try:
            # Let facade handle all validation and business logic
            updated_user = facade.update_user(user_id, user_data)
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
        except ValueError as e:
            # Catch validation errors from facade and return appropriate HTTP response
            if "not found" in str(e).lower():
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400