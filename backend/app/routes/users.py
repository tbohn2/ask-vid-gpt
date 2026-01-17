from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app.routes import api_bp
from app.services import UserService


@api_bp.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users with optional pagination
    
    Query Parameters:
        limit (int, optional): Maximum number of users to return
        offset (int, optional): Number of users to skip
        
    Returns:
        JSON response with list of users
    """
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        
        users = UserService.get_all_users(limit=limit, offset=offset)
        
        users_data = [{
            'id': user.id,
            'username': user.username
        } for user in users]
        
        return jsonify({
            'users': users_data,
            'count': len(users_data)
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve users',
            'message': str(e)
        }), 500


@api_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    
    Request Body (JSON):
        username (str, required): Unique username for the user
        password (str, required): Password for the user (will be hashed)
        
    Returns:
        JSON response with created user data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be JSON'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username:
            return jsonify({
                'error': 'Validation error',
                'message': 'Username is required'
            }), 400
        
        if not password:
            return jsonify({
                'error': 'Validation error',
                'message': 'Password is required'
            }), 400
        
        # Check if username already exists
        if UserService.username_exists(username):
            return jsonify({
                'error': 'Conflict',
                'message': f'Username "{username}" already exists'
            }), 409
        
        user = UserService.create_user(username, password)
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'message': 'User created successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except IntegrityError:
        return jsonify({
            'error': 'Conflict',
            'message': f'Username "{data.get("username")}" already exists'
        }), 409
    except Exception as e:
        return jsonify({
            'error': 'Failed to create user',
            'message': str(e)
        }), 500


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID
    
    Path Parameters:
        user_id (int): The ID of the user to delete
        
    Returns:
        JSON response with deletion status
    """
    try:
        deleted = UserService.delete_user(user_id)
        
        if not deleted:
            return jsonify({
                'error': 'Not found',
                'message': f'User with ID {user_id} not found'
            }), 404
        
        return jsonify({
            'message': f'User with ID {user_id} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete user',
            'message': str(e)
        }), 500


@api_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user with username and password
    
    Request Body (JSON):
        username (str, required): Username of the user
        password (str, required): Password of the user
        
    Returns:
        JSON response with user data if authentication succeeds
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be JSON'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username:
            return jsonify({
                'error': 'Validation error',
                'message': 'Username is required'
            }), 400
        
        if not password:
            return jsonify({
                'error': 'Validation error',
                'message': 'Password is required'
            }), 400
        
        user = UserService.login(username, password)
        
        if not user:
            return jsonify({
                'error': 'Authentication failed',
                'message': 'Invalid username or password'
            }), 401
        
        # Create JWT access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'access_token': access_token,
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to authenticate',
            'message': str(e)
        }), 500


@api_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout a user (revoke their token)
    
    Headers:
        Authorization: Bearer <access_token>
        
    Returns:
        JSON response with logout status
    """
    try:
        # Get the JWT token
        jti = get_jwt()['jti']
        
        # In a production app, you might want to add the token to a blacklist
        # For now, we'll just return success (client should discard the token)
        
        return jsonify({
            'message': 'Logout successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to logout',
            'message': str(e)
        }), 500
