from typing import Optional, List
from app import db
from app.models.models import Collection
from app.services.user_service import UserService


class CollectionService:
    @staticmethod
    def create_collection(name: str, user_id: int, description: Optional[str] = None) -> Collection:
        """
        Create a new collection
        
        Args:
            name: Name of the collection
            user_id: ID of the user who owns the collection
            description: Optional description of the collection
            
        Returns:
            Collection: The created collection object
            
        Raises:
            ValueError: If name is empty or user doesn't exist
        """
        if not name or not name.strip():
            raise ValueError("Collection name cannot be empty")
        
        if not UserService.user_exists(user_id):
            raise ValueError(f"User with ID {user_id} does not exist")
        
        collection = Collection(
            name=name.strip(),
            user_id=user_id,
            description=description.strip() if description else None
        )
        db.session.add(collection)
        db.session.commit()
        return collection

    @staticmethod
    def get_collection_by_id(collection_id: int) -> Optional[Collection]:
        """
        Get a collection by its ID
        
        Args:
            collection_id: The ID of the collection
            
        Returns:
            Collection: The collection object if found, None otherwise
        """
        return Collection.query.get(collection_id)

    @staticmethod
    def get_all_collections(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> List[Collection]:
        """
        Get all collections with optional pagination and user filtering
        
        Args:
            limit: Maximum number of collections to return
            offset: Number of collections to skip
            user_id: Optional user ID to filter collections by user
            
        Returns:
            List[Collection]: List of collection objects
        """
        query = Collection.query
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def delete_collection(collection_id: int) -> bool:
        """
        Delete a collection by its ID
        
        Args:
            collection_id: The ID of the collection to delete
            
        Returns:
            bool: True if collection was deleted, False if collection not found
        """
        collection = CollectionService.get_collection_by_id(collection_id)
        if not collection:
            return False
        
        db.session.delete(collection)
        db.session.commit()
        return True

    @staticmethod
    def collection_exists(collection_id: int) -> bool:
        """
        Check if a collection exists by ID
        
        Args:
            collection_id: The ID of the collection to check
            
        Returns:
            bool: True if collection exists, False otherwise
        """
        return Collection.query.filter_by(id=collection_id).first() is not None

    @staticmethod
    def get_collections_by_user(user_id: int) -> List[Collection]:
        """
        Get all collections for a specific user
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List[Collection]: List of collection objects for the user
        """
        return Collection.query.filter_by(user_id=user_id).all()

