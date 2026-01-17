from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.models import User


class UserService:
    @staticmethod
    def create_user(username: str, password: str) -> User:
        """
        Create a new user with hashed password
        
        Args:
            username: Unique username for the user
            password: Plain text password to be hashed
            
        Returns:
            User: The created user object
            
        Raises:
            ValueError: If username or password is empty or None
            IntegrityError: If username already exists
        """
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        if not password:
            raise ValueError("Password cannot be empty")
        
        # Hash the password before storing
        hashed_password = generate_password_hash(password)
        
        user = User(
            username=username.strip(),
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Get a user by their ID
        
        Args:
            user_id: The ID of the user
            
        Returns:
            User: The user object if found, None otherwise
        """
        return User.query.get(user_id)

    @staticmethod
    def get_all_users(limit: Optional[int] = None, offset: Optional[int] = None) -> List[User]:
        """
        Get all users with optional pagination
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List[User]: List of user objects
        """
        query = User.query
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        Delete a user by their ID
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if user was deleted, False if user not found
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def user_exists(user_id: int) -> bool:
        """
        Check if a user exists by ID
        
        Args:
            user_id: The ID of the user to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        return User.query.filter_by(id=user_id).first() is not None

    @staticmethod
    def username_exists(username: str) -> bool:
        """
        Check if a username already exists
        
        Args:
            username: The username to check
            
        Returns:
            bool: True if username exists, False otherwise
        """
        return User.query.filter_by(username=username).first() is not None

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """
        Get a user by their username
        
        Args:
            username: The username to search for
            
        Returns:
            User: The user object if found, None otherwise
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def login(username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password
        
        Args:
            username: The username to authenticate
            password: The plain text password to verify
            
        Returns:
            User: The user object if authentication succeeds, None otherwise
        """
        if not username or not password:
            return None
        
        user = UserService.get_user_by_username(username)
        if not user:
            return None
        
        if not check_password_hash(user.password, password):
            return None
        
        return user
