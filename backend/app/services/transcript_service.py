from typing import Optional, List
from app import db
from app.models.models import Transcript
from app.services.video_service import VideoService

# Chunk size by total transcript length (chars): ~5min, ~10min, ~20min, 1hr+
_CHUNK_SIZE_BY_LENGTH = [
    (4000, 2000),
    (8000, 4000),
    (15000, 8000),
]
_DEFAULT_CHUNK_SIZE = 8000


def _chunk_size_for_length(length: int) -> int:
    """Return suggested chunk size in chars based on total transcript length."""
    for max_len, chunk_size in _CHUNK_SIZE_BY_LENGTH:
        if length <= max_len:
            return chunk_size
    return _DEFAULT_CHUNK_SIZE


def _split_into_chunks(content: str, chunk_size: int) -> List[str]:
    """Split content into chunks, breaking at word boundaries when possible."""
    content = content.strip()
    if not content:
        return []
    chunks = []
    start = 0
    while start < len(content):
        end = min(start + chunk_size, len(content))
        if end < len(content):
            # Try to break at last space in this range
            last_space = content.rfind(" ", start, end + 1)
            if last_space > start:
                end = last_space + 1
        chunks.append(content[start:end].strip())
        start = end
    return [c for c in chunks if c]


class TranscriptService:
    @staticmethod
    def create_transcript(
        video_id: int,
        content: str
    ) -> List[Transcript]:
        """
        Create transcript chunks for a video from full transcript content.
        Chunk size is chosen by total length (e.g. 2k for short, 8k for long).
        Replaces any existing transcript chunks for this video.

        Args:
            video_id: ID of the video this transcript belongs to
            content: Full transcript content

        Returns:
            List[Transcript]: Created transcript chunks, ordered by chunk_index

        Raises:
            ValueError: If content is empty or video doesn't exist
        """
        if not content or not content.strip():
            raise ValueError("Transcript content cannot be empty")

        if not VideoService.video_exists(video_id):
            raise ValueError(f"Video with ID {video_id} does not exist")

        text = content.strip()
        size = _chunk_size_for_length(len(text))
        chunk_texts = _split_into_chunks(text, size)

        # Replace existing transcripts for this video
        Transcript.query.filter_by(video_id=video_id).delete()

        transcripts = []
        for i, chunk_content in enumerate(chunk_texts):
            t = Transcript(
                video_id=video_id,
                content=chunk_content,
                chunk_index=i,
            )
            db.session.add(t)
            transcripts.append(t)
        db.session.commit()
        return transcripts

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
            query = query.filter_by(video_id=video_id).order_by(Transcript.chunk_index)
        else:
            query = query.order_by(Transcript.video_id, Transcript.chunk_index)
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
        Get all transcript chunks for a specific video, ordered by chunk_index.

        Args:
            video_id: The ID of the video

        Returns:
            List[Transcript]: List of transcript chunks for the video
        """
        return (
            Transcript.query.filter_by(video_id=video_id)
            .order_by(Transcript.chunk_index)
            .all()
        )
