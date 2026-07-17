from datetime import datetime
from enum import Enum
from bson import ObjectId


class BadgeType(Enum):
    ACHIEVEMENT = "achievement"
    MILESTONE = "milestone"
    CHALLENGE = "challenge"
    STREAK = "streak"


class Badge:
    """Model for badges earned by students"""
    
    def __init__(self, name, description, badge_type=BadgeType.ACHIEVEMENT.value, icon_url="",
                 requirement_type="", requirement_value=0, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.description = description
        self.badge_type = badge_type
        self.icon_url = icon_url
        self.requirement_type = requirement_type  # e.g., "lessons_completed", "quiz_score", "streak"
        self.requirement_value = requirement_value
        self.created_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'name': self.name,
            'description': self.description,
            'badge_type': self.badge_type,
            'icon_url': self.icon_url,
            'requirement_type': self.requirement_type,
            'requirement_value': self.requirement_value,
            'created_at': self.created_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return Badge(
            name=data.get('name'),
            description=data.get('description'),
            badge_type=data.get('badge_type', BadgeType.ACHIEVEMENT.value),
            icon_url=data.get('icon_url', ''),
            requirement_type=data.get('requirement_type', ''),
            requirement_value=data.get('requirement_value', 0),
            _id=data.get('_id'),
        )


class StudentBadge:
    """Model for badges earned by a student"""
    
    def __init__(self, student_id, badge_id, earned_at=None, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.badge_id = ObjectId(badge_id) if isinstance(badge_id, str) else badge_id
        self.earned_at = earned_at or datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'badge_id': str(self.badge_id),
            'earned_at': self.earned_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return StudentBadge(
            student_id=data.get('student_id'),
            badge_id=data.get('badge_id'),
            earned_at=data.get('earned_at'),
            _id=data.get('_id'),
        )


class Points:
    """Model for tracking student points"""
    
    def __init__(self, student_id, course_id, total_points=0, lesson_points=0, quiz_points=0,
                 assignment_points=0, participation_points=0, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.total_points = total_points
        self.lesson_points = lesson_points
        self.quiz_points = quiz_points
        self.assignment_points = assignment_points
        self.participation_points = participation_points
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'course_id': str(self.course_id),
            'total_points': self.total_points,
            'lesson_points': self.lesson_points,
            'quiz_points': self.quiz_points,
            'assignment_points': self.assignment_points,
            'participation_points': self.participation_points,
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return Points(
            student_id=data.get('student_id'),
            course_id=data.get('course_id'),
            total_points=data.get('total_points', 0),
            lesson_points=data.get('lesson_points', 0),
            quiz_points=data.get('quiz_points', 0),
            assignment_points=data.get('assignment_points', 0),
            participation_points=data.get('participation_points', 0),
            _id=data.get('_id'),
        )


class LeaderboardEntry:
    """Model for leaderboard entries"""
    
    def __init__(self, student_id, student_name, course_id, total_points=0, rank=0, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.student_name = student_name
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.total_points = total_points
        self.rank = rank
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'student_name': self.student_name,
            'course_id': str(self.course_id),
            'total_points': self.total_points,
            'rank': self.rank,
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return LeaderboardEntry(
            student_id=data.get('student_id'),
            student_name=data.get('student_name'),
            course_id=data.get('course_id'),
            total_points=data.get('total_points', 0),
            rank=data.get('rank', 0),
            _id=data.get('_id'),
        )


class Streak:
    """Model for tracking learning streaks"""
    
    def __init__(self, student_id, course_id, current_streak=0, longest_streak=0,
                 last_activity_date=None, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.last_activity_date = last_activity_date or datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'course_id': str(self.course_id),
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_activity_date': self.last_activity_date.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return Streak(
            student_id=data.get('student_id'),
            course_id=data.get('course_id'),
            current_streak=data.get('current_streak', 0),
            longest_streak=data.get('longest_streak', 0),
            last_activity_date=data.get('last_activity_date'),
            _id=data.get('_id'),
        )
