from typing import Optional, List
from app import db
from app.models.models import Transcript
from app.services.video_service import VideoService


class TranscriptService:
    @staticmethod
    def create_transcript(
        video_id: int,
        content: str
    ) -> Transcript:
        """
        Create a new transcript
        
        Args:
            video_id: ID of the video this transcript belongs to
            content: The transcript content
            
        Returns:
            Transcript: The created transcript object
            
        Raises:
            ValueError: If required fields are empty or video doesn't exist
        """
        if not content or not content.strip():
            raise ValueError("Transcript content cannot be empty")
        
        if not VideoService.video_exists(video_id):
            raise ValueError(f"Video with ID {video_id} does not exist")
        
        transcript = Transcript(
            video_id=video_id,
            content=content.strip()
        )
        db.session.add(transcript)
        db.session.commit()
        return transcript

    @staticmethod
    def get_transcript_by_id(transcript_id: int) -> Optional[Transcript]:
        """
        Get a transcript by its ID
        
        Args:
            transcript_id: The ID of the transcript
            
        Returns:
            Transcript: The transcript object if found, None otherwise
        """
        return Transcript.query.get(transcript_id)

    @staticmethod
    def get_all_transcripts(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        video_id: Optional[int] = None
    ) -> List[Transcript]:
        """
        Get all transcripts with optional pagination and video filtering
        
        Args:
            limit: Maximum number of transcripts to return
            offset: Number of transcripts to skip
            video_id: Optional video ID to filter transcripts by video
            
        Returns:
            List[Transcript]: List of transcript objects
        """
        query = Transcript.query
        if video_id is not None:
            query = query.filter_by(video_id=video_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def delete_transcript(transcript_id: int) -> bool:
        """
        Delete a transcript by its ID
        
        Args:
            transcript_id: The ID of the transcript to delete
            
        Returns:
            bool: True if transcript was deleted, False if transcript not found
        """
        transcript = TranscriptService.get_transcript_by_id(transcript_id)
        if not transcript:
            return False
        
        db.session.delete(transcript)
        db.session.commit()
        return True

    @staticmethod
    def transcript_exists(transcript_id: int) -> bool:
        """
        Check if a transcript exists by ID
        
        Args:
            transcript_id: The ID of the transcript to check
            
        Returns:
            bool: True if transcript exists, False otherwise
        """
        return Transcript.query.filter_by(id=transcript_id).first() is not None

    @staticmethod
    def get_transcripts_by_video(video_id: int) -> List[Transcript]:
        """
        Get all transcripts for a specific video
        
        Args:
            video_id: The ID of the video
            
        Returns:
            List[Transcript]: List of transcript objects for the video
        """
        return Transcript.query.filter_by(video_id=video_id).all()
