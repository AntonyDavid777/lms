from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.utils.auth import hash_password, verify_password


class UserRole(Enum):
    """User role enumeration"""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class User:
    """User model for MongoDB"""
    
    COLLECTION_NAME = 'users'
    
    def __init__(self, email, password, name, role=UserRole.STUDENT.value, _id=None, created_at=None, updated_at=None, **kwargs):
        self._id = _id or ObjectId()
        self.email = email
        self.password_hash = hash_password(password) if not password.startswith('$2') else password
        self.name = name
        self.role = role
        self.bio = kwargs.get('bio', '')
        self.profile_picture_url = kwargs.get('profile_picture_url', '')
        self.is_active = kwargs.get('is_active', True)
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return verify_password(password, self.password_hash)
    
    def to_dict(self, include_password=False):
        """Convert user to dictionary"""
        user_dict = {
            '_id': str(self._id),
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'bio': self.bio,
            'profile_picture_url': self.profile_picture_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
        if include_password:
            user_dict['password_hash'] = self.password_hash
        return user_dict
    
    def to_public_dict(self):
        """Convert user to public dictionary (safe for external use)"""
        return {
            '_id': str(self._id),
            'name': self.name,
            'bio': self.bio,
            'profile_picture_url': self.profile_picture_url,
            'role': self.role,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
        }
    
    @staticmethod
    def from_dict(data):
        """Create user from dictionary"""
        return User(
            email=data['email'],
            password=data.get('password_hash', ''),
            name=data['name'],
            role=data.get('role', UserRole.STUDENT.value),
            _id=ObjectId(data['_id']) if isinstance(data.get('_id'), str) else data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            **{k: v for k, v in data.items() if k not in ['_id', 'email', 'password', 'password_hash', 'name', 'role', 'created_at', 'updated_at']}
        )
    
    @staticmethod
    def from_mongo_dict(data):
        """Create user from MongoDB document"""
        if data is None:
            return None
        return User(
            email=data.get('email', ''),
            password=data.get('password_hash', ''),
            name=data.get('name', ''),
            role=data.get('role', UserRole.STUDENT.value),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            bio=data.get('bio', ''),
            profile_picture_url=data.get('profile_picture_url', ''),
            is_active=data.get('is_active', True),
        )
