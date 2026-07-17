try:
    import motor.motor_asyncio
except ImportError:
    motor = None  # motor not required for synchronous usage
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Synchronous MongoDB connection wrapper"""
    
    _client = None
    _db = None
    
    @classmethod
    def connect(cls, mongodb_uri, database_name):
        """Initialize synchronous MongoDB connection"""
        try:
            cls._client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                retryWrites=True,
                w='majority'
            )
            # Test connection
            cls._client.admin.command('ping')
            cls._db = cls._client[database_name]
            logger.info(f"Connected to MongoDB database: {database_name}")
            return cls._db
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return cls._db
    
    @classmethod
    def get_client(cls):
        """Get MongoDB client"""
        if cls._client is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return cls._client
    
    @classmethod
    def disconnect(cls):
        """Close database connection"""
        if cls._client:
            cls._client.close()
            cls._db = None
            cls._client = None
            logger.info("Disconnected from MongoDB")


class AsyncDatabaseConnection:
    """Asynchronous MongoDB connection wrapper using Motor"""
    
    _client = None
    _db = None
    
    @classmethod
    async def connect(cls, mongodb_uri, database_name):
        """Initialize async MongoDB connection"""
        try:
            cls._client = motor.motor_asyncio.AsyncMongoClient(mongodb_uri)
            # Test connection
            await cls._client.admin.command('ping')
            cls._db = cls._client[database_name]
            logger.info(f"Connected to async MongoDB database: {database_name}")
            return cls._db
        except Exception as e:
            logger.error(f"Failed to connect to async MongoDB: {e}")
            raise
    
    @classmethod
    def get_db(cls):
        """Get async database instance"""
        if cls._db is None:
            raise RuntimeError("Async database not connected. Call connect() first.")
        return cls._db
    
    @classmethod
    async def disconnect(cls):
        """Close async database connection"""
        if cls._client:
            cls._client.close()
            cls._db = None
            cls._client = None
            logger.info("Disconnected from async MongoDB")


def init_indexes(db):
    """Initialize MongoDB indexes for performance"""
    try:
        # Users collection
        db.users.create_index('email', unique=True)
        db.users.create_index('created_at')
        
        # Courses collection
        db.courses.create_index('instructor_id')
        db.courses.create_index('category')
        db.courses.create_index('status')
        db.courses.create_index('created_at')
        
        # Lessons collection
        db.lessons.create_index('course_id')
        db.lessons.create_index([('course_id', 1), ('order', 1)])
        
        # Assessments collection
        db.assessments.create_index('course_id')
        db.assessments.create_index('instructor_id')
        
        # Quiz results collection
        db.quiz_results.create_index('user_id')
        db.quiz_results.create_index('assessment_id')
        db.quiz_results.create_index([('user_id', 1), ('assessment_id', 1)])
        
        # Enrollments collection
        db.enrollments.create_index([('user_id', 1), ('course_id', 1)], unique=True)
        db.enrollments.create_index('user_id')
        db.enrollments.create_index('course_id')
        
        # Progress collection
        db.progress.create_index([('user_id', 1), ('course_id', 1)])
        db.progress.create_index([('user_id', 1), ('lesson_id', 1)], unique=True)
        
        # User badges collection
        db.user_badges.create_index([('user_id', 1), ('badge_id', 1)], unique=True)
        db.user_badges.create_index('user_id')
        
        # Analytics collection
        db.analytics.create_index('event_type')
        db.analytics.create_index('user_id')
        db.analytics.create_index('timestamp')
        db.analytics.create_index([('event_type', 1), ('timestamp', -1)])
        
        logger.info("MongoDB indexes initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing indexes: {e}")
        raise
