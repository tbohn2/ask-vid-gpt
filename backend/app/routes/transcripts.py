from flask import jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from app.routes import api_bp
from app.services import TranscriptService


@api_bp.route('/transcripts', methods=['GET'])
@jwt_required()
def get_all_transcripts():
    """
    Get all transcripts with optional pagination and video filtering
    
    Query Parameters:
        limit (int, optional): Maximum number of transcripts to return
        offset (int, optional): Number of transcripts to skip
        video_id (int, optional): Filter transcripts by video ID
        
    Returns:
        JSON response with list of transcripts
    """
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        video_id = request.args.get('video_id', type=int)
        
        transcripts = TranscriptService.get_all_transcripts(
            limit=limit,
            offset=offset,
            video_id=video_id
        )
        
        transcripts_data = [{
            'id': transcript.id,
            'video_id': transcript.video_id,
            'content': transcript.content,
            'created_at': transcript.created_at.isoformat() if transcript.created_at else None
        } for transcript in transcripts]
        
        return jsonify({
            'transcripts': transcripts_data,
            'count': len(transcripts_data)
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve transcripts',
            'message': str(e)
        }), 500


@api_bp.route('/transcripts', methods=['POST'])
@jwt_required()
def create_transcript():
    """
    Create a new transcript
    
    Request Body (JSON):
        video_id (int, required): ID of the video this transcript belongs to
        content (str, required): The transcript content
        
    Returns:
        JSON response with created transcript data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be JSON'
            }), 400
        
        video_id = data.get('video_id')
        content = data.get('content')
        
        if not video_id:
            return jsonify({
                'error': 'Validation error',
                'message': 'Video ID is required'
            }), 400
        
        if not content:
            return jsonify({
                'error': 'Validation error',
                'message': 'Transcript content is required'
            }), 400
        
        transcript = TranscriptService.create_transcript(
            video_id=video_id,
            content=content
        )
        
        return jsonify({
            'id': transcript.id,
            'video_id': transcript.video_id,
            'content': transcript.content,
            'created_at': transcript.created_at.isoformat() if transcript.created_at else None,
            'message': 'Transcript created successfully'
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
            'error': 'Failed to create transcript',
            'message': str(e)
        }), 500


@api_bp.route('/transcripts/<int:transcript_id>', methods=['GET'])
@jwt_required()
def get_transcript(transcript_id):
    """
    Get a transcript by ID
    
    Path Parameters:
        transcript_id (int): The ID of the transcript
        
    Returns:
        JSON response with transcript data
    """
    try:
        transcript = TranscriptService.get_transcript_by_id(transcript_id)
        
        if not transcript:
            return jsonify({
                'error': 'Not found',
                'message': f'Transcript with ID {transcript_id} not found'
            }), 404
        
        return jsonify({
            'id': transcript.id,
            'video_id': transcript.video_id,
            'content': transcript.content,
            'created_at': transcript.created_at.isoformat() if transcript.created_at else None
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve transcript',
            'message': str(e)
        }), 500


@api_bp.route('/transcripts/<int:video_id>', methods=['GET'])
@jwt_required()
def get_transcripts_by_video(video_id):
    """
    Get all transcripts by video ID
    
    Path Parameters:
        video_id (int): The ID of the video
        
    Returns:
        JSON response with list of transcripts
    """
    try:
        transcripts = TranscriptService.get_transcripts_by_video(video_id)
        transcripts_data = [{
            'id': transcript.id,
            'video_id': transcript.video_id,
            'content': transcript.content,
            'created_at': transcript.created_at.isoformat() if transcript.created_at else None
        } for transcript in transcripts]
        return jsonify({
            'transcripts': transcripts_data,
            'count': len(transcripts_data)
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve transcripts',
            'message': str(e)
        }), 500


@api_bp.route('/transcripts/<int:transcript_id>', methods=['DELETE'])
@jwt_required()
def delete_transcript(transcript_id):
    """
    Delete a transcript by ID
    
    Path Parameters:
        transcript_id (int): The ID of the transcript to delete
        
    Returns:
        JSON response with deletion status
    """
    try:
        deleted = TranscriptService.delete_transcript(transcript_id)
        
        if not deleted:
            return jsonify({
                'error': 'Not found',
                'message': f'Transcript with ID {transcript_id} not found'
            }), 404
        
        return jsonify({
            'message': f'Transcript with ID {transcript_id} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete transcript',
            'message': str(e)
        }), 500
