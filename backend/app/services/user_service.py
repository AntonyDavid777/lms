from bson import ObjectId
from app.models.user import User, UserRole
from app.utils.errors import NotFoundError, ConflictError, ValidationError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service layer for user operations"""
    
    def __init__(self, db):
        self.db = db
        self.users_collection = db.users
    
    def create_user(self, email, password, name, role=UserRole.STUDENT.value, **kwargs):
        """Create a new user"""
        # Check if email already exists
        existing_user = self.users_collection.find_one({'email': email.lower()})
        if existing_user:
            raise ConflictError(f'Email {email} is already registered')
        
        # Create user
        user = User(
            email=email.lower(),
            password=password,
            name=name,
            role=role,
            **kwargs
        )
        
        # Insert into database
        result = self.users_collection.insert_one(user.to_dict(include_password=True))
        user._id = result.inserted_id
        
        logger.info(f"User created: {user._id} ({email})")
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user_doc = self.users_collection.find_one({'_id': ObjectId(user_id)})
            if not user_doc:
                raise NotFoundError(f'User {user_id} not found')
            return User.from_mongo_dict(user_doc)
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise
            raise ValueError(f'Invalid user ID: {user_id}')
    
    def get_user_by_email(self, email):
        """Get user by email"""
        user_doc = self.users_collection.find_one({'email': email.lower()})
        if not user_doc:
            return None
        return User.from_mongo_dict(user_doc)
    
    def update_user(self, user_id, **kwargs):
        """Update user information"""
        allowed_fields = ['name', 'bio', 'profile_picture_url', 'role', 'is_active']
        update_data = {}
        
        for field in allowed_fields:
            if field in kwargs:
                update_data[field] = kwargs[field]
        
        if not update_data:
            raise ValidationError('No fields to update')
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            raise NotFoundError(f'User {user_id} not found')
        
        logger.info(f"User updated: {user_id}")
        return self.get_user_by_id(user_id)
    
    def delete_user(self, user_id):
        """Soft delete user (deactivate)"""
        result = self.users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'is_active': False,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise NotFoundError(f'User {user_id} not found')
        
        logger.info(f"User deactivated: {user_id}")
    
    def list_users(self, page=1, page_size=10, role=None, is_active=None):
        """List users with pagination and filtering"""
        query = {}
        
        if role:
            query['role'] = role
        
        if is_active is not None:
            query['is_active'] = is_active
        
        total = self.users_collection.count_documents(query)
        
        skip = (page - 1) * page_size
        users_docs = self.users_collection.find(query).skip(skip).limit(page_size)
        
        users = [User.from_mongo_dict(doc) for doc in users_docs]
        
        return users, total
    
    def search_users(self, search_query, page=1, page_size=10):
        """Search users by name or email"""
        query = {
            '$or': [
                {'name': {'$regex': search_query, '$options': 'i'}},
                {'email': {'$regex': search_query, '$options': 'i'}}
            ]
        }
        
        total = self.users_collection.count_documents(query)
        
        skip = (page - 1) * page_size
        users_docs = self.users_collection.find(query).skip(skip).limit(page_size)
        
        users = [User.from_mongo_dict(doc) for doc in users_docs]
        
        return users, total
    
    def get_user_courses(self, user_id):
        """Get all courses enrolled by a user"""
        enrollments = self.db.enrollments.find(
            {'user_id': ObjectId(user_id)}
        ).project({'course_id': 1})
        
        course_ids = [ObjectId(e['course_id']) for e in enrollments]
        
        if not course_ids:
            return []
        
        courses = list(self.db.courses.find({'_id': {'$in': course_ids}}))
        return courses
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        user = self.get_user_by_id(user_id)
        
        # Verify old password
        if not user.verify_password(old_password):
            raise ValidationError('Current password is incorrect')
        
        # Hash new password
        from app.utils.auth import hash_password
        new_hash = hash_password(new_password)
        
        # Update password
        self.users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'password_hash': new_hash,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        logger.info(f"Password changed for user: {user_id}")
    
    def deactivate_user(self, user_id):
        """Deactivate user account"""
        result = self.users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'is_active': False,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise NotFoundError(f'User {user_id} not found')
        
        logger.info(f"User deactivated: {user_id}")
    
    def activate_user(self, user_id):
        """Reactivate user account"""
        result = self.users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'is_active': True,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise NotFoundError(f'User {user_id} not found')
        
        logger.info(f"User reactivated: {user_id}")
