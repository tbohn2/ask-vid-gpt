from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
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
        if not username:
            return jsonify({
                'error': 'Validation error',
                'message': 'Username is required'
            }), 400
        
        # Check if username already exists
        if UserService.username_exists(username):
            return jsonify({
                'error': 'Conflict',
                'message': f'Username "{username}" already exists'
            }), 409
        
        user = UserService.create_user(username)
        
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

