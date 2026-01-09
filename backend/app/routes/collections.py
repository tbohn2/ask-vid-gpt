from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from app.routes import api_bp
from app.services import CollectionService


@api_bp.route('/collections', methods=['GET'])
def get_all_collections():
    """
    Get all collections with optional pagination and user filtering
    
    Query Parameters:
        limit (int, optional): Maximum number of collections to return
        offset (int, optional): Number of collections to skip
        user_id (int, optional): Filter collections by user ID
        
    Returns:
        JSON response with list of collections
    """
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        user_id = request.args.get('user_id', type=int)
        
        collections = CollectionService.get_all_collections(
            limit=limit,
            offset=offset,
            user_id=user_id
        )
        
        collections_data = [{
            'id': collection.id,
            'name': collection.name,
            'description': collection.description,
            'user_id': collection.user_id,
            'created_at': collection.created_at.isoformat() if collection.created_at else None
        } for collection in collections]
        
        return jsonify({
            'collections': collections_data,
            'count': len(collections_data)
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve collections',
            'message': str(e)
        }), 500


@api_bp.route('/collections', methods=['POST'])
def create_collection():
    """
    Create a new collection
    
    Request Body (JSON):
        name (str, required): Name of the collection
        user_id (int, required): ID of the user who owns the collection
        description (str, optional): Description of the collection
        
    Returns:
        JSON response with created collection data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be JSON'
            }), 400
        
        name = data.get('name')
        user_id = data.get('user_id')
        description = data.get('description')
        
        if not name:
            return jsonify({
                'error': 'Validation error',
                'message': 'Collection name is required'
            }), 400
        
        if not user_id:
            return jsonify({
                'error': 'Validation error',
                'message': 'User ID is required'
            }), 400
        
        collection = CollectionService.create_collection(
            name=name,
            user_id=user_id,
            description=description
        )
        
        return jsonify({
            'id': collection.id,
            'name': collection.name,
            'description': collection.description,
            'user_id': collection.user_id,
            'created_at': collection.created_at.isoformat() if collection.created_at else None,
            'message': 'Collection created successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except IntegrityError as e:
        return jsonify({
            'error': 'Database error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Failed to create collection',
            'message': str(e)
        }), 500


@api_bp.route('/collections/<int:collection_id>', methods=['GET'])
def get_collection(collection_id):
    """
    Get a collection by ID
    
    Path Parameters:
        collection_id (int): The ID of the collection
        
    Returns:
        JSON response with collection data
    """
    try:
        collection = CollectionService.get_collection_by_id(collection_id)
        
        if not collection:
            return jsonify({
                'error': 'Not found',
                'message': f'Collection with ID {collection_id} not found'
            }), 404
        
        return jsonify({
            'id': collection.id,
            'name': collection.name,
            'description': collection.description,
            'user_id': collection.user_id,
            'created_at': collection.created_at.isoformat() if collection.created_at else None
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve collection',
            'message': str(e)
        }), 500


@api_bp.route('/collections/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    """
    Delete a collection by ID
    
    Path Parameters:
        collection_id (int): The ID of the collection to delete
        
    Returns:
        JSON response with deletion status
    """
    try:
        deleted = CollectionService.delete_collection(collection_id)
        
        if not deleted:
            return jsonify({
                'error': 'Not found',
                'message': f'Collection with ID {collection_id} not found'
            }), 404
        
        return jsonify({
            'message': f'Collection with ID {collection_id} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete collection',
            'message': str(e)
        }), 500

