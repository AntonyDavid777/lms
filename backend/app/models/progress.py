from datetime import datetime
from enum import Enum
from bson import ObjectId


class ProgressStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class LessonProgress:
    """Model for tracking lesson progress"""
    
    def __init__(self, student_id, lesson_id, course_id, status=ProgressStatus.NOT_STARTED.value,
                 started_at=None, completed_at=None, time_spent=0, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.lesson_id = ObjectId(lesson_id) if isinstance(lesson_id, str) else lesson_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.status = status
        self.started_at = started_at or datetime.utcnow()
        self.completed_at = completed_at
        self.time_spent = time_spent  # in seconds
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'lesson_id': str(self.lesson_id),
            'course_id': str(self.course_id),
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_spent': self.time_spent,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return LessonProgress(
            student_id=data.get('student_id'),
            lesson_id=data.get('lesson_id'),
            course_id=data.get('course_id'),
            status=data.get('status', ProgressStatus.NOT_STARTED.value),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at'),
            time_spent=data.get('time_spent', 0),
            _id=data.get('_id'),
        )


class CourseProgress:
    """Model for tracking overall course progress"""
    
    def __init__(self, student_id, course_id, total_lessons=0, completed_lessons=0,
                 overall_progress=0, last_accessed=None, enrollment_date=None, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.total_lessons = total_lessons
        self.completed_lessons = completed_lessons
        self.overall_progress = overall_progress  # percentage 0-100
        self.last_accessed = last_accessed or datetime.utcnow()
        self.enrollment_date = enrollment_date or datetime.utcnow()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'course_id': str(self.course_id),
            'total_lessons': self.total_lessons,
            'completed_lessons': self.completed_lessons,
            'overall_progress': self.overall_progress,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return CourseProgress(
            student_id=data.get('student_id'),
            course_id=data.get('course_id'),
            total_lessons=data.get('total_lessons', 0),
            completed_lessons=data.get('completed_lessons', 0),
            overall_progress=data.get('overall_progress', 0),
            last_accessed=data.get('last_accessed'),
            enrollment_date=data.get('enrollment_date'),
            _id=data.get('_id'),
        )


class AssessmentProgress:
    """Model for tracking assessment performance"""
    
    def __init__(self, student_id, assessment_id, course_id, best_score=0, last_score=0,
                 attempts=0, first_attempt_date=None, last_attempt_date=None, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.assessment_id = ObjectId(assessment_id) if isinstance(assessment_id, str) else assessment_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.best_score = best_score
        self.last_score = last_score
        self.attempts = attempts
        self.first_attempt_date = first_attempt_date
        self.last_attempt_date = last_attempt_date or datetime.utcnow()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'assessment_id': str(self.assessment_id),
            'course_id': str(self.course_id),
            'best_score': self.best_score,
            'last_score': self.last_score,
            'attempts': self.attempts,
            'first_attempt_date': self.first_attempt_date.isoformat() if self.first_attempt_date else None,
            'last_attempt_date': self.last_attempt_date.isoformat() if self.last_attempt_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return AssessmentProgress(
            student_id=data.get('student_id'),
            assessment_id=data.get('assessment_id'),
            course_id=data.get('course_id'),
            best_score=data.get('best_score', 0),
            last_score=data.get('last_score', 0),
            attempts=data.get('attempts', 0),
            first_attempt_date=data.get('first_attempt_date'),
            last_attempt_date=data.get('last_attempt_date'),
            _id=data.get('_id'),
        )
