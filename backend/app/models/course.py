from datetime import datetime
from enum import Enum
from bson import ObjectId


class CourseLevel(Enum):
    """Course difficulty level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CourseStatus(Enum):
    """Course publication status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Course:
    """Course model for MongoDB"""
    
    COLLECTION_NAME = 'courses'
    
    def __init__(
        self,
        title: str,
        description: str,
        instructor_id: str,
        category: str = '',
        level: str = CourseLevel.BEGINNER.value,
        status: str = CourseStatus.DRAFT.value,
        _id=None,
        thumbnail_url: str = '',
        created_at=None,
        updated_at=None,
        **kwargs
    ):
        self._id = _id or ObjectId()
        self.title = title
        self.description = description
        self.instructor_id = ObjectId(instructor_id) if isinstance(instructor_id, str) else instructor_id
        self.category = category
        self.level = level
        self.status = status
        self.thumbnail_url = thumbnail_url
        self.lesson_ids = kwargs.get('lesson_ids', [])
        self.enrollment_count = kwargs.get('enrollment_count', 0)
        self.average_rating = kwargs.get('average_rating', 0.0)
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self, include_lesson_ids=False):
        """Convert course to dictionary"""
        course_dict = {
            '_id': str(self._id),
            'title': self.title,
            'description': self.description,
            'instructor_id': str(self.instructor_id),
            'category': self.category,
            'level': self.level,
            'status': self.status,
            'thumbnail_url': self.thumbnail_url,
            'enrollment_count': self.enrollment_count,
            'average_rating': self.average_rating,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
        if include_lesson_ids:
            course_dict['lesson_ids'] = [str(lid) for lid in self.lesson_ids]
        return course_dict
    
    @staticmethod
    def from_mongo_dict(data):
        """Create course from MongoDB document"""
        if data is None:
            return None
        return Course(
            title=data.get('title', ''),
            description=data.get('description', ''),
            instructor_id=data.get('instructor_id'),
            category=data.get('category', ''),
            level=data.get('level', CourseLevel.BEGINNER.value),
            status=data.get('status', CourseStatus.DRAFT.value),
            thumbnail_url=data.get('thumbnail_url', ''),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            lesson_ids=data.get('lesson_ids', []),
            enrollment_count=data.get('enrollment_count', 0),
            average_rating=data.get('average_rating', 0.0),
        )


class Lesson:
    """Lesson model for MongoDB"""
    
    COLLECTION_NAME = 'lessons'
    
    def __init__(
        self,
        title: str,
        description: str,
        course_id: str,
        order: int,
        content_type: str = 'text',
        content: str = '',
        _id=None,
        video_url: str = '',
        duration: int = 0,
        learning_objectives=None,
        resources_url=None,
        created_at=None,
        updated_at=None,
        **kwargs
    ):
        self._id = _id or ObjectId()
        self.title = title
        self.description = description
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.order = order
        self.content_type = content_type
        self.content = content
        self.video_url = video_url
        self.duration = duration
        self.learning_objectives = learning_objectives or []
        self.resources_url = resources_url or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert lesson to dictionary"""
        return {
            '_id': str(self._id),
            'title': self.title,
            'description': self.description,
            'course_id': str(self.course_id),
            'order': self.order,
            'content_type': self.content_type,
            'content': self.content,
            'video_url': self.video_url,
            'duration': self.duration,
            'learning_objectives': self.learning_objectives,
            'resources_url': self.resources_url,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
    
    @staticmethod
    def from_mongo_dict(data):
        """Create lesson from MongoDB document"""
        if data is None:
            return None
        return Lesson(
            title=data.get('title', ''),
            description=data.get('description', ''),
            course_id=data.get('course_id'),
            order=data.get('order', 0),
            content_type=data.get('content_type', 'text'),
            content=data.get('content', ''),
            video_url=data.get('video_url', ''),
            duration=data.get('duration', 0),
            learning_objectives=data.get('learning_objectives', []),
            resources_url=data.get('resources_url', []),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )


class Enrollment:
    """Course enrollment model"""
    
    COLLECTION_NAME = 'enrollments'
    
    def __init__(
        self,
        user_id: str,
        course_id: str,
        _id=None,
        progress_percentage: float = 0.0,
        enrolled_at=None,
        completed_at=None,
        **kwargs
    ):
        self._id = _id or ObjectId()
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.progress_percentage = progress_percentage
        self.enrolled_at = enrolled_at or datetime.utcnow()
        self.completed_at = completed_at
    
    def to_dict(self):
        """Convert enrollment to dictionary"""
        return {
            '_id': str(self._id),
            'user_id': str(self.user_id),
            'course_id': str(self.course_id),
            'progress_percentage': self.progress_percentage,
            'enrolled_at': self.enrolled_at.isoformat() if isinstance(self.enrolled_at, datetime) else self.enrolled_at,
            'completed_at': self.completed_at.isoformat() if isinstance(self.completed_at, datetime) else self.completed_at,
        }
    
    @staticmethod
    def from_mongo_dict(data):
        """Create enrollment from MongoDB document"""
        if data is None:
            return None
        return Enrollment(
            user_id=data.get('user_id'),
            course_id=data.get('course_id'),
            progress_percentage=data.get('progress_percentage', 0.0),
            enrolled_at=data.get('enrolled_at'),
            completed_at=data.get('completed_at'),
            _id=data.get('_id'),
        )
