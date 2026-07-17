from bson import ObjectId
from app.models.assessment import Assessment, Question, QuizResult, AssessmentStatus
from app.utils.errors import NotFoundError, ValidationError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AssessmentService:
    """Service layer for assessment operations"""
    
    def __init__(self, db):
        self.db = db
        self.assessments_collection = db.assessments
        self.questions_collection = db.questions
        self.quiz_results_collection = db.quiz_results
    
    # Assessment Operations
    
    def create_assessment(
        self,
        title: str,
        description: str,
        course_id: str,
        instructor_id: str,
        **kwargs
    ):
        """Create a new assessment"""
        assessment = Assessment(
            title=title,
            description=description,
            course_id=course_id,
            instructor_id=instructor_id,
            **kwargs
        )
        
        result = self.assessments_collection.insert_one(assessment.to_dict())
        assessment._id = result.inserted_id
        
        logger.info(f"Assessment created: {assessment._id} in course {course_id}")
        return assessment
    
    def get_assessment_by_id(self, assessment_id: str, include_questions: bool = False):
        """Get assessment by ID"""
        try:
            assessment_doc = self.assessments_collection.find_one({'_id': ObjectId(assessment_id)})
            if not assessment_doc:
                raise NotFoundError(f'Assessment {assessment_id} not found')
            
            assessment = Assessment.from_mongo_dict(assessment_doc)
            
            if include_questions:
                questions_docs = self.questions_collection.find(
                    {'assessment_id': ObjectId(assessment_id)}
                ).sort('order', 1)
                assessment.questions = [Question.from_mongo_dict(doc, include_answer=False) for doc in questions_docs]
            
            return assessment
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise
            raise ValueError(f'Invalid assessment ID: {assessment_id}')
    
    def update_assessment(self, assessment_id: str, **kwargs):
        """Update assessment information"""
        allowed_fields = ['title', 'description', 'assessment_type', 'total_points', 'passing_score', 
                         'time_limit', 'status', 'due_date', 'show_answers', 'shuffle_questions']
        update_data = {}
        
        for field in allowed_fields:
            if field in kwargs:
                update_data[field] = kwargs[field]
        
        if not update_data:
            raise ValidationError('No fields to update')
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.assessments_collection.update_one(
            {'_id': ObjectId(assessment_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            raise NotFoundError(f'Assessment {assessment_id} not found')
        
        logger.info(f"Assessment updated: {assessment_id}")
        return self.get_assessment_by_id(assessment_id)
    
    def delete_assessment(self, assessment_id: str):
        """Delete assessment and all related data"""
        # Delete questions
        self.questions_collection.delete_many({'assessment_id': ObjectId(assessment_id)})
        
        # Delete quiz results
        self.quiz_results_collection.delete_many({'assessment_id': ObjectId(assessment_id)})
        
        # Delete assessment
        result = self.assessments_collection.delete_one({'_id': ObjectId(assessment_id)})
        
        if result.deleted_count == 0:
            raise NotFoundError(f'Assessment {assessment_id} not found')
        
        logger.info(f"Assessment deleted: {assessment_id}")
    
    def list_assessments_by_course(self, course_id: str, page: int = 1, page_size: int = 10, status: str = None):
        """List assessments in a course"""
        query = {'course_id': ObjectId(course_id)}
        
        if status:
            query['status'] = status
        
        total = self.assessments_collection.count_documents(query)
        
        skip = (page - 1) * page_size
        assessments_docs = self.assessments_collection.find(query).skip(skip).limit(page_size).sort('created_at', -1)
        
        assessments = [Assessment.from_mongo_dict(doc) for doc in assessments_docs]
        
        return assessments, total
    
    def list_assessments_by_instructor(self, instructor_id: str, page: int = 1, page_size: int = 10):
        """List assessments created by instructor"""
        query = {'instructor_id': ObjectId(instructor_id)}
        
        total = self.assessments_collection.count_documents(query)
        
        skip = (page - 1) * page_size
        assessments_docs = self.assessments_collection.find(query).skip(skip).limit(page_size).sort('created_at', -1)
        
        assessments = [Assessment.from_mongo_dict(doc) for doc in assessments_docs]
        
        return assessments, total
    
    # Question Operations
    
    def create_question(
        self,
        assessment_id: str,
        question_text: str,
        question_type: str,
        order: int,
        **kwargs
    ):
        """Create a new question"""
        question = Question(
            assessment_id=assessment_id,
            question_text=question_text,
            question_type=question_type,
            order=order,
            **kwargs
        )
        
        result = self.questions_collection.insert_one(question.to_dict(include_answer=True))
        question._id = result.inserted_id
        
        # Update assessment question count
        self.assessments_collection.update_one(
            {'_id': ObjectId(assessment_id)},
            {'$inc': {'questions_count': 1}}
        )
        
        logger.info(f"Question created: {question._id} in assessment {assessment_id}")
        return question
    
    def get_question_by_id(self, question_id: str, include_answer: bool = False):
        """Get question by ID"""
        try:
            question_doc = self.questions_collection.find_one({'_id': ObjectId(question_id)})
            if not question_doc:
                raise NotFoundError(f'Question {question_id} not found')
            
            return Question.from_mongo_dict(question_doc, include_answer=include_answer)
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise
            raise ValueError(f'Invalid question ID: {question_id}')
    
    def update_question(self, question_id: str, **kwargs):
        """Update question"""
        allowed_fields = ['question_text', 'question_type', 'order', 'points', 'options', 'correct_answer', 'explanation']
        update_data = {}
        
        for field in allowed_fields:
            if field in kwargs:
                update_data[field] = kwargs[field]
        
        if not update_data:
            raise ValidationError('No fields to update')
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.questions_collection.update_one(
            {'_id': ObjectId(question_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            raise NotFoundError(f'Question {question_id} not found')
        
        logger.info(f"Question updated: {question_id}")
        return self.get_question_by_id(question_id, include_answer=True)
    
    def delete_question(self, question_id: str, assessment_id: str = None):
        """Delete question"""
        question = self.get_question_by_id(question_id)
        assessment_id = assessment_id or str(question.assessment_id)
        
        result = self.questions_collection.delete_one({'_id': ObjectId(question_id)})
        
        if result.deleted_count == 0:
            raise NotFoundError(f'Question {question_id} not found')
        
        # Update assessment question count
        self.assessments_collection.update_one(
            {'_id': ObjectId(assessment_id)},
            {'$inc': {'questions_count': -1}}
        )
        
        logger.info(f"Question deleted: {question_id}")
    
    def get_assessment_questions(self, assessment_id: str, include_answers: bool = False):
        """Get all questions for an assessment"""
        questions_docs = self.questions_collection.find(
            {'assessment_id': ObjectId(assessment_id)}
        ).sort('order', 1)
        
        questions = [Question.from_mongo_dict(doc, include_answer=include_answers) for doc in questions_docs]
        return questions
    
    def reorder_questions(self, assessment_id: str, question_orders: list):
        """Reorder questions in an assessment"""
        for item in question_orders:
            self.questions_collection.update_one(
                {'_id': ObjectId(item['question_id'])},
                {'$set': {'order': item['order']}}
            )
        
        logger.info(f"Questions reordered in assessment: {assessment_id}")
    
    # Quiz Result Operations
    
    def save_quiz_draft(self, user_id: str, assessment_id: str, course_id: str, answers: dict):
        """Save a quiz draft"""
        existing = self.quiz_results_collection.find_one({
            'user_id': ObjectId(user_id),
            'assessment_id': ObjectId(assessment_id),
            'is_draft': True
        })
        
        if existing:
            # Update existing draft
            self.quiz_results_collection.update_one(
                {'_id': existing['_id']},
                {'$set': {'answers': answers}}
            )
            return QuizResult.from_mongo_dict(existing)
        else:
            # Create new draft
            result = QuizResult(
                user_id=user_id,
                assessment_id=assessment_id,
                course_id=course_id,
                answers=answers,
                is_draft=True
            )
            
            db_result = self.quiz_results_collection.insert_one(result.to_dict())
            result._id = db_result.inserted_id
            
            logger.info(f"Quiz draft saved: {user_id} -> {assessment_id}")
            return result
    
    def submit_quiz(self, user_id: str, assessment_id: str, course_id: str, answers: dict):
        """Submit a quiz"""
        # Get assessment
        assessment = self.get_assessment_by_id(assessment_id)
        
        # Get all questions with answers
        questions = self.get_assessment_questions(assessment_id, include_answers=True)
        
        # Calculate score
        score = 0
        total_points = 0
        
        for question in questions:
            total_points += question.points
            
            # Check if answer is correct
            user_answer = answers.get(str(question._id))
            if self._is_answer_correct(question, user_answer):
                score += question.points
        
        # Calculate percentage
        percentage = (score / total_points * 100) if total_points > 0 else 0
        passed = percentage >= assessment.passing_score
        
        # Delete draft if exists
        self.quiz_results_collection.delete_one({
            'user_id': ObjectId(user_id),
            'assessment_id': ObjectId(assessment_id),
            'is_draft': True
        })
        
        # Create new result
        result = QuizResult(
            user_id=user_id,
            assessment_id=assessment_id,
            course_id=course_id,
            answers=answers,
            score=score,
            percentage=round(percentage, 2),
            passed=passed,
            is_draft=False,
            graded_at=datetime.utcnow()
        )
        
        db_result = self.quiz_results_collection.insert_one(result.to_dict())
        result._id = db_result.inserted_id
        
        logger.info(f"Quiz submitted: {user_id} -> {assessment_id} (Score: {score}/{total_points})")
        return result
    
    def get_quiz_result(self, result_id: str):
        """Get quiz result"""
        try:
            result_doc = self.quiz_results_collection.find_one({'_id': ObjectId(result_id)})
            if not result_doc:
                raise NotFoundError(f'Quiz result {result_id} not found')
            return QuizResult.from_mongo_dict(result_doc)
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise
            raise ValueError(f'Invalid quiz result ID: {result_id}')
    
    def get_student_quiz_results(self, user_id: str, assessment_id: str = None, course_id: str = None, page: int = 1, page_size: int = 10):
        """Get quiz results for a student"""
        query = {
            'user_id': ObjectId(user_id),
            'is_draft': False
        }
        
        if assessment_id:
            query['assessment_id'] = ObjectId(assessment_id)
        
        if course_id:
            query['course_id'] = ObjectId(course_id)
        
        total = self.quiz_results_collection.count_documents(query)
        
        skip = (page - 1) * page_size
        results_docs = self.quiz_results_collection.find(query).skip(skip).limit(page_size).sort('submitted_at', -1)
        
        results = [QuizResult.from_mongo_dict(doc) for doc in results_docs]
        
        return results, total
    
    def get_assessment_results(self, assessment_id: str, page: int = 1, page_size: int = 10):
        """Get all results for an assessment"""
        query = {
            'assessment_id': ObjectId(assessment_id),
            'is_draft': False
        }
        
        total = self.quiz_results_collection.count_documents(query)
        
        skip = (page - 1) * page_size
        results_docs = self.quiz_results_collection.find(query).skip(skip).limit(page_size).sort('submitted_at', -1)
        
        results = [QuizResult.from_mongo_dict(doc) for doc in results_docs]
        
        return results, total
    
    def get_assessment_statistics(self, assessment_id: str):
        """Get statistics for an assessment"""
        results = self.quiz_results_collection.find({
            'assessment_id': ObjectId(assessment_id),
            'is_draft': False
        })
        
        results_list = list(results)
        
        if not results_list:
            return {
                'total_submissions': 0,
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'pass_rate': 0
            }
        
        scores = [r['score'] for r in results_list]
        percentages = [r['percentage'] for r in results_list]
        passed_count = len([r for r in results_list if r['passed']])
        
        return {
            'total_submissions': len(results_list),
            'average_score': round(sum(scores) / len(scores), 2),
            'average_percentage': round(sum(percentages) / len(percentages), 2),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'pass_rate': round(passed_count / len(results_list) * 100, 2)
        }
    
    def _is_answer_correct(self, question, user_answer):
        """Check if user answer is correct"""
        if question.question_type == 'multiple_choice':
            return user_answer == question.correct_answer
        elif question.question_type == 'true_false':
            return user_answer == question.correct_answer
        elif question.question_type == 'short_answer':
            # Case-insensitive comparison
            if isinstance(user_answer, str) and isinstance(question.correct_answer, str):
                return user_answer.lower().strip() == question.correct_answer.lower().strip()
            return user_answer == question.correct_answer
        else:
            # Essay and matching questions require manual grading
            return False
