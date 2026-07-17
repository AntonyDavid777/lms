from datetime import datetime
from bson import ObjectId


class CourseAnalytics:
    """Model for course-level analytics"""
    
    def __init__(self, course_id, total_students=0, active_students=0, completed_students=0,
                 average_progress=0.0, average_score=0.0, completion_rate=0.0, _id=None):
        self._id = _id or ObjectId()
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.total_students = total_students
        self.active_students = active_students
        self.completed_students = completed_students
        self.average_progress = average_progress
        self.average_score = average_score
        self.completion_rate = completion_rate
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'course_id': str(self.course_id),
            'total_students': self.total_students,
            'active_students': self.active_students,
            'completed_students': self.completed_students,
            'average_progress': round(self.average_progress, 2),
            'average_score': round(self.average_score, 2),
            'completion_rate': round(self.completion_rate, 2),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return CourseAnalytics(
            course_id=data.get('course_id'),
            total_students=data.get('total_students', 0),
            active_students=data.get('active_students', 0),
            completed_students=data.get('completed_students', 0),
            average_progress=data.get('average_progress', 0.0),
            average_score=data.get('average_score', 0.0),
            completion_rate=data.get('completion_rate', 0.0),
            _id=data.get('_id'),
        )


class StudentAnalytics:
    """Model for student-level analytics"""
    
    def __init__(self, student_id, course_id, total_lessons=0, completed_lessons=0,
                 lessons_progress=0.0, total_assessments=0, completed_assessments=0,
                 assessments_completion=0.0, average_assessment_score=0.0, total_points=0,
                 total_time_spent=0, last_activity=None, _id=None):
        self._id = _id or ObjectId()
        self.student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.total_lessons = total_lessons
        self.completed_lessons = completed_lessons
        self.lessons_progress = lessons_progress
        self.total_assessments = total_assessments
        self.completed_assessments = completed_assessments
        self.assessments_completion = assessments_completion
        self.average_assessment_score = average_assessment_score
        self.total_points = total_points
        self.total_time_spent = total_time_spent
        self.last_activity = last_activity or datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'student_id': str(self.student_id),
            'course_id': str(self.course_id),
            'total_lessons': self.total_lessons,
            'completed_lessons': self.completed_lessons,
            'lessons_progress': round(self.lessons_progress, 2),
            'total_assessments': self.total_assessments,
            'completed_assessments': self.completed_assessments,
            'assessments_completion': round(self.assessments_completion, 2),
            'average_assessment_score': round(self.average_assessment_score, 2),
            'total_points': self.total_points,
            'total_time_spent': self.total_time_spent,
            'last_activity': self.last_activity.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return StudentAnalytics(
            student_id=data.get('student_id'),
            course_id=data.get('course_id'),
            total_lessons=data.get('total_lessons', 0),
            completed_lessons=data.get('completed_lessons', 0),
            lessons_progress=data.get('lessons_progress', 0.0),
            total_assessments=data.get('total_assessments', 0),
            completed_assessments=data.get('completed_assessments', 0),
            assessments_completion=data.get('assessments_completion', 0.0),
            average_assessment_score=data.get('average_assessment_score', 0.0),
            total_points=data.get('total_points', 0),
            total_time_spent=data.get('total_time_spent', 0),
            last_activity=data.get('last_activity'),
            _id=data.get('_id'),
        )


class LessonAnalytics:
    """Model for lesson-level analytics"""
    
    def __init__(self, lesson_id, course_id, total_started=0, total_completed=0,
                 completion_rate=0.0, average_time_spent=0, _id=None):
        self._id = _id or ObjectId()
        self.lesson_id = ObjectId(lesson_id) if isinstance(lesson_id, str) else lesson_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.total_started = total_started
        self.total_completed = total_completed
        self.completion_rate = completion_rate
        self.average_time_spent = average_time_spent
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_id=True):
        data = {
            'lesson_id': str(self.lesson_id),
            'course_id': str(self.course_id),
            'total_started': self.total_started,
            'total_completed': self.total_completed,
            'completion_rate': round(self.completion_rate, 2),
            'average_time_spent': round(self.average_time_spent, 2),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_id:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def from_dict(data):
        return LessonAnalytics(
            lesson_id=data.get('lesson_id'),
            course_id=data.get('course_id'),
            total_started=data.get('total_started', 0),
            total_completed=data.get('total_completed', 0),
            completion_rate=data.get('completion_rate', 0.0),
            average_time_spent=data.get('average_time_spent', 0),
            _id=data.get('_id'),
        )
