from flask import jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from app.routes import api_bp
from app.services import VideoService


@api_bp.route('/videos', methods=['GET'])
@jwt_required()
def get_all_videos():
    """
    Get all videos with optional pagination and collection filtering
    
    Query Parameters:
        limit (int, optional): Maximum number of videos to return
        offset (int, optional): Number of videos to skip
        collection_id (int, optional): Filter videos by collection ID
        
    Returns:
        JSON response with list of videos
    """
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        collection_id = request.args.get('collection_id', type=int)
        
        videos = VideoService.get_all_videos(
            limit=limit,
            offset=offset,
            collection_id=collection_id
        )
        
        videos_data = [{
            'id': video.id,
            'youtube_id': video.youtube_id,
            'title': video.title,
            'description': video.description,
            'collection_id': video.collection_id,
            'created_at': video.created_at.isoformat() if video.created_at else None
        } for video in videos]
        
        return jsonify({
            'videos': videos_data,
            'count': len(videos_data)
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve videos',
            'message': str(e)
        }), 500


@api_bp.route('/videos', methods=['POST'])
@jwt_required()
def create_video():
    """
    Create a new video
    
    Request Body (JSON):
        youtube_id (str, required): Unique YouTube ID for the video
        title (str, required): Title of the video
        collection_id (int, required): ID of the collection this video belongs to
        description (str, optional): Description of the video
        
    Returns:
        JSON response with created video data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be JSON'
            }), 400
        
        youtube_id = data.get('youtube_id')
        title = data.get('title')
        collection_id = data.get('collection_id')
        description = data.get('description')
        
        if not youtube_id:
            return jsonify({
                'error': 'Validation error',
                'message': 'YouTube ID is required'
            }), 400
        
        if not title:
            return jsonify({
                'error': 'Validation error',
                'message': 'Video title is required'
            }), 400
        
        if not collection_id:
            return jsonify({
                'error': 'Validation error',
                'message': 'Collection ID is required'
            }), 400
        
        video = VideoService.create_video(
            youtube_id=youtube_id,
            title=title,
            collection_id=collection_id,
            description=description
        )
        
        return jsonify({
            'id': video.id,
            'youtube_id': video.youtube_id,
            'title': video.title,
            'description': video.description,
            'collection_id': video.collection_id,
            'created_at': video.created_at.isoformat() if video.created_at else None,
            'message': 'Video created successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except IntegrityError as e:
        return jsonify({
            'error': 'Database error',
            'message': 'A video with this YouTube ID already exists'
        }), 409
    except Exception as e:
        return jsonify({
            'error': 'Failed to create video',
            'message': str(e)
        }), 500


@api_bp.route('/videos/<int:video_id>', methods=['GET'])
@jwt_required()
def get_video(video_id):
    """
    Get a video by ID
    
    Path Parameters:
        video_id (int): The ID of the video
        
    Returns:
        JSON response with video data
    """
    try:
        video = VideoService.get_video_by_id(video_id)
        
        if not video:
            return jsonify({
                'error': 'Not found',
                'message': f'Video with ID {video_id} not found'
            }), 404
        
        return jsonify({
            'id': video.id,
            'youtube_id': video.youtube_id,
            'title': video.title,
            'description': video.description,
            'collection_id': video.collection_id,
            'created_at': video.created_at.isoformat() if video.created_at else None
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve video',
            'message': str(e)
        }), 500


@api_bp.route('/videos/<int:video_id>', methods=['PUT'])
@jwt_required()
def update_video(video_id):
    """
    Update a video by ID
    
    Path Parameters:
        video_id (int): The ID of the video to update
        
    Request Body (JSON):
        title (str, optional): New title for the video
        description (str, optional): New description for the video
        collection_id (int, optional): New collection ID for the video
        
    Returns:
        JSON response with updated video data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be JSON'
            }), 400
        
        title = data.get('title')
        description = data.get('description')
        collection_id = data.get('collection_id')
        
        video = VideoService.update_video(
            video_id=video_id,
            title=title,
            description=description,
            collection_id=collection_id
        )
        
        if not video:
            return jsonify({
                'error': 'Not found',
                'message': f'Video with ID {video_id} not found'
            }), 404
        
        return jsonify({
            'id': video.id,
            'youtube_id': video.youtube_id,
            'title': video.title,
            'description': video.description,
            'collection_id': video.collection_id,
            'created_at': video.created_at.isoformat() if video.created_at else None,
            'message': 'Video updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Failed to update video',
            'message': str(e)
        }), 500


@api_bp.route('/videos/<int:video_id>', methods=['DELETE'])
@jwt_required()
def delete_video(video_id):
    """
    Delete a video by ID
    
    Path Parameters:
        video_id (int): The ID of the video to delete
        
    Returns:
        JSON response with deletion status
    """
    try:
        deleted = VideoService.delete_video(video_id)
        
        if not deleted:
            return jsonify({
                'error': 'Not found',
                'message': f'Video with ID {video_id} not found'
            }), 404
        
        return jsonify({
            'message': f'Video with ID {video_id} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete video',
            'message': str(e)
        }), 500
