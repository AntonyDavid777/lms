from datetime import datetime
from enum import Enum
from bson import ObjectId


class QuestionType(Enum):
    """Question type enumeration"""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    TRUE_FALSE = "true_false"
    ESSAY = "essay"
    MATCHING = "matching"


class AssessmentType(Enum):
    """Assessment type enumeration"""
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    PRACTICE = "practice"


class AssessmentStatus(Enum):
    """Assessment status enumeration"""
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
    ARCHIVED = "archived"


class Assessment:
    """Assessment/Quiz model for MongoDB"""
    
    COLLECTION_NAME = 'assessments'
    
    def __init__(
        self,
        title: str,
        description: str,
        course_id: str,
        instructor_id: str,
        assessment_type: str = AssessmentType.QUIZ.value,
        _id=None,
        total_points: int = 100,
        passing_score: float = 70.0,
        time_limit: int = None,  # in minutes
        status: str = AssessmentStatus.DRAFT.value,
        questions_count: int = 0,
        created_at=None,
        updated_at=None,
        due_date=None,
        show_answers: bool = False,
        shuffle_questions: bool = False,
        **kwargs
    ):
        self._id = _id or ObjectId()
        self.title = title
        self.description = description
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.instructor_id = ObjectId(instructor_id) if isinstance(instructor_id, str) else instructor_id
        self.assessment_type = assessment_type
        self.total_points = total_points
        self.passing_score = passing_score
        self.time_limit = time_limit
        self.status = status
        self.questions_count = questions_count
        self.due_date = due_date
        self.show_answers = show_answers
        self.shuffle_questions = shuffle_questions
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self, include_questions=False):
        """Convert assessment to dictionary"""
        assessment_dict = {
            '_id': str(self._id),
            'title': self.title,
            'description': self.description,
            'course_id': str(self.course_id),
            'instructor_id': str(self.instructor_id),
            'assessment_type': self.assessment_type,
            'total_points': self.total_points,
            'passing_score': self.passing_score,
            'time_limit': self.time_limit,
            'status': self.status,
            'questions_count': self.questions_count,
            'due_date': self.due_date.isoformat() if isinstance(self.due_date, datetime) else self.due_date,
            'show_answers': self.show_answers,
            'shuffle_questions': self.shuffle_questions,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
        return assessment_dict
    
    @staticmethod
    def from_mongo_dict(data):
        """Create assessment from MongoDB document"""
        if data is None:
            return None
        return Assessment(
            title=data.get('title', ''),
            description=data.get('description', ''),
            course_id=data.get('course_id'),
            instructor_id=data.get('instructor_id'),
            assessment_type=data.get('assessment_type', AssessmentType.QUIZ.value),
            total_points=data.get('total_points', 100),
            passing_score=data.get('passing_score', 70.0),
            time_limit=data.get('time_limit'),
            status=data.get('status', AssessmentStatus.DRAFT.value),
            questions_count=data.get('questions_count', 0),
            due_date=data.get('due_date'),
            show_answers=data.get('show_answers', False),
            shuffle_questions=data.get('shuffle_questions', False),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )


class Question:
    """Quiz question model"""
    
    COLLECTION_NAME = 'questions'
    
    def __init__(
        self,
        assessment_id: str,
        question_text: str,
        question_type: str,
        order: int,
        points: int = 1,
        _id=None,
        options=None,
        correct_answer=None,
        explanation: str = '',
        created_at=None,
        updated_at=None,
        **kwargs
    ):
        self._id = _id or ObjectId()
        self.assessment_id = ObjectId(assessment_id) if isinstance(assessment_id, str) else assessment_id
        self.question_text = question_text
        self.question_type = question_type
        self.order = order
        self.points = points
        self.options = options or []  # For multiple choice/true-false
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self, include_answer=False):
        """Convert question to dictionary"""
        question_dict = {
            '_id': str(self._id),
            'assessment_id': str(self.assessment_id),
            'question_text': self.question_text,
            'question_type': self.question_type,
            'order': self.order,
            'points': self.points,
            'options': self.options,
            'explanation': self.explanation,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
        if include_answer:
            question_dict['correct_answer'] = self.correct_answer
        return question_dict
    
    @staticmethod
    def from_mongo_dict(data, include_answer=False):
        """Create question from MongoDB document"""
        if data is None:
            return None
        return Question(
            assessment_id=data.get('assessment_id'),
            question_text=data.get('question_text', ''),
            question_type=data.get('question_type', ''),
            order=data.get('order', 0),
            points=data.get('points', 1),
            options=data.get('options', []),
            correct_answer=data.get('correct_answer'),
            explanation=data.get('explanation', ''),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )


class QuizResult:
    """Quiz result/submission model"""
    
    COLLECTION_NAME = 'quiz_results'
    
    def __init__(
        self,
        user_id: str,
        assessment_id: str,
        course_id: str,
        _id=None,
        answers: dict = None,
        score: float = 0.0,
        percentage: float = 0.0,
        passed: bool = False,
        feedback: str = '',
        time_spent: int = 0,  # in seconds
        submitted_at=None,
        graded_at=None,
        is_draft: bool = True,
        **kwargs
    ):
        self._id = _id or ObjectId()
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        self.assessment_id = ObjectId(assessment_id) if isinstance(assessment_id, str) else assessment_id
        self.course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
        self.answers = answers or {}
        self.score = score
        self.percentage = percentage
        self.passed = passed
        self.feedback = feedback
        self.time_spent = time_spent
        self.submitted_at = submitted_at or datetime.utcnow()
        self.graded_at = graded_at
        self.is_draft = is_draft
    
    def to_dict(self):
        """Convert quiz result to dictionary"""
        return {
            '_id': str(self._id),
            'user_id': str(self.user_id),
            'assessment_id': str(self.assessment_id),
            'course_id': str(self.course_id),
            'answers': self.answers,
            'score': self.score,
            'percentage': self.percentage,
            'passed': self.passed,
            'feedback': self.feedback,
            'time_spent': self.time_spent,
            'submitted_at': self.submitted_at.isoformat() if isinstance(self.submitted_at, datetime) else self.submitted_at,
            'graded_at': self.graded_at.isoformat() if isinstance(self.graded_at, datetime) else self.graded_at,
            'is_draft': self.is_draft,
        }
    
    @staticmethod
    def from_mongo_dict(data):
        """Create quiz result from MongoDB document"""
        if data is None:
            return None
        return QuizResult(
            user_id=data.get('user_id'),
            assessment_id=data.get('assessment_id'),
            course_id=data.get('course_id'),
            answers=data.get('answers', {}),
            score=data.get('score', 0.0),
            percentage=data.get('percentage', 0.0),
            passed=data.get('passed', False),
            feedback=data.get('feedback', ''),
            time_spent=data.get('time_spent', 0),
            submitted_at=data.get('submitted_at'),
            graded_at=data.get('graded_at'),
            is_draft=data.get('is_draft', True),
            _id=data.get('_id'),
        )
