from typing import Optional, List
from app import db
from app.models.models import Video
from app.services.collection_service import CollectionService


class VideoService:
    @staticmethod
    def create_video(
        youtube_id: str,
        title: str,
        collection_id: int,
        description: Optional[str] = None
    ) -> Video:
        """
        Create a new video
        
        Args:
            youtube_id: Unique YouTube ID for the video
            title: Title of the video
            collection_id: ID of the collection this video belongs to
            description: Optional description of the video
            
        Returns:
            Video: The created video object
            
        Raises:
            ValueError: If required fields are empty or collection doesn't exist
        """
        if not youtube_id or not youtube_id.strip():
            raise ValueError("YouTube ID cannot be empty")
        
        if not title or not title.strip():
            raise ValueError("Video title cannot be empty")
        
        if not CollectionService.collection_exists(collection_id):
            raise ValueError(f"Collection with ID {collection_id} does not exist")
        
        video = Video(
            youtube_id=youtube_id.strip(),
            title=title.strip(),
            collection_id=collection_id,
            description=description.strip() if description else None
        )
        db.session.add(video)
        db.session.commit()
        return video

    @staticmethod
    def get_video_by_id(video_id: int) -> Optional[Video]:
        """
        Get a video by its ID
        
        Args:
            video_id: The ID of the video
            
        Returns:
            Video: The video object if found, None otherwise
        """
        return Video.query.get(video_id)

    @staticmethod
    def get_all_videos(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        collection_id: Optional[int] = None
    ) -> List[Video]:
        """
        Get all videos with optional pagination and collection filtering
        
        Args:
            limit: Maximum number of videos to return
            offset: Number of videos to skip
            collection_id: Optional collection ID to filter videos by collection
            
        Returns:
            List[Video]: List of video objects
        """
        query = Video.query
        if collection_id is not None:
            query = query.filter_by(collection_id=collection_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def update_video(
        video_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        collection_id: Optional[int] = None
    ) -> Optional[Video]:
        """
        Update a video by its ID
        
        Args:
            video_id: The ID of the video to update
            title: Optional new title for the video
            description: Optional new description for the video
            collection_id: Optional new collection ID for the video
            
        Returns:
            Video: The updated video object if found, None otherwise
            
        Raises:
            ValueError: If collection_id is provided but doesn't exist
        """
        video = VideoService.get_video_by_id(video_id)
        if not video:
            return None
        
        if collection_id is not None:
            if not CollectionService.collection_exists(collection_id):
                raise ValueError(f"Collection with ID {collection_id} does not exist")
            video.collection_id = collection_id
        
        if title is not None:
            if not title.strip():
                raise ValueError("Video title cannot be empty")
            video.title = title.strip()
        
        if description is not None:
            video.description = description.strip() if description.strip() else None
        
        db.session.commit()
        return video

    @staticmethod
    def delete_video(video_id: int) -> bool:
        """
        Delete a video by its ID
        
        Args:
            video_id: The ID of the video to delete
            
        Returns:
            bool: True if video was deleted, False if video not found
        """
        video = VideoService.get_video_by_id(video_id)
        if not video:
            return False
        
        db.session.delete(video)
        db.session.commit()
        return True

    @staticmethod
    def video_exists(video_id: int) -> bool:
        """
        Check if a video exists by ID
        
        Args:
            video_id: The ID of the video to check
            
        Returns:
            bool: True if video exists, False otherwise
        """
        return Video.query.filter_by(id=video_id).first() is not None

    @staticmethod
    def get_videos_by_collection(collection_id: int) -> List[Video]:
        """
        Get all videos for a specific collection
        
        Args:
            collection_id: The ID of the collection
            
        Returns:
            List[Video]: List of video objects for the collection
        """
        return Video.query.filter_by(collection_id=collection_id).all()

    @staticmethod
    def get_video_by_youtube_id(youtube_id: str) -> Optional[Video]:
        """
        Get a video by its YouTube ID
        
        Args:
            youtube_id: The YouTube ID of the video
            
        Returns:
            Video: The video object if found, None otherwise
        """
        return Video.query.filter_by(youtube_id=youtube_id).first()
