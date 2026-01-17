from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.services import UserService


def auth_required(f):
    """
    Decorator to require authentication for a route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            # Optionally verify user still exists
            user = UserService.get_user_by_id(current_user_id)
            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'User not found'
                }), 401
            
            # Attach user to request context for easy access
            request.current_user = user
            request.current_user_id = current_user_id
            
        except Exception as e:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or missing authentication token'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def setup_auth_middleware(blueprint, exempt_routes=None):
    """
    Setup authentication middleware for a blueprint
    
    Args:
        blueprint: The Flask blueprint to protect
        exempt_routes: List of route endpoints to exempt from authentication
                      Format: ['/login', '/logout', '/users'] (without /api prefix)
    """
    if exempt_routes is None:
        exempt_routes = ['/login', '/logout']
    
    @blueprint.before_request
    def require_auth():
        # Get the path (without /api prefix)
        path = request.path
        
        # Remove /api prefix if present
        if path.startswith('/api'):
            path = path[4:]  # Remove '/api'
        
        # Ensure path starts with /
        if not path.startswith('/'):
            path = '/' + path
        
        # Check if this route is exempt
        # Allow exact matches or if path starts with exempt route + / (for sub-routes)
        is_exempt = False
        for exempt_route in exempt_routes:
            if path == exempt_route:
                is_exempt = True
                break
            # Also allow POST to /users (registration) but not other methods
            if path == '/users' and request.method == 'POST':
                is_exempt = True
                break
        
        if is_exempt:
            return None  # Allow request to proceed without auth
        
        # For all other routes, require authentication
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            # Verify user still exists
            user = UserService.get_user_by_id(current_user_id)
            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'User not found'
                }), 401
            
            # Attach user to request context
            request.current_user = user
            request.current_user_id = current_user_id
            
        except Exception as e:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or missing authentication token. Please login first.'
            }), 401
        
        return None  # Allow request to proceed
