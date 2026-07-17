from datetime import datetime
from bson import ObjectId
from app.models.progress import (
    LessonProgress, ProgressStatus, CourseProgress, AssessmentProgress
)
from app.utils.errors import NotFoundError, ValidationError


class ProgressService:
    """Service for managing student progress tracking"""
    
    def __init__(self, db):
        self.db = db
        self.lesson_progress_collection = db.lesson_progress
        self.course_progress_collection = db.course_progress
        self.assessment_progress_collection = db.assessment_progress
    
    # Lesson Progress Methods
    def start_lesson(self, student_id, lesson_id, course_id):
        """Mark lesson as started"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            lesson_id = ObjectId(lesson_id) if isinstance(lesson_id, str) else lesson_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            progress = LessonProgress(
                student_id=student_id,
                lesson_id=lesson_id,
                course_id=course_id,
                status=ProgressStatus.IN_PROGRESS.value
            )
            
            # Check if already exists
            existing = self.lesson_progress_collection.find_one({
                'student_id': student_id,
                'lesson_id': lesson_id,
            })
            
            if existing:
                # Update existing
                result = self.lesson_progress_collection.update_one(
                    {'_id': existing['_id']},
                    {'$set': {
                        'status': ProgressStatus.IN_PROGRESS.value,
                        'updated_at': datetime.utcnow()
                    }}
                )
                return LessonProgress.from_dict(existing)
            
            # Create new
            result = self.lesson_progress_collection.insert_one(progress.__dict__)
            progress._id = result.inserted_id
            return progress
        
        except Exception as e:
            raise Exception(f"Failed to start lesson: {str(e)}")
    
    def complete_lesson(self, student_id, lesson_id):
        """Mark lesson as completed"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            lesson_id = ObjectId(lesson_id) if isinstance(lesson_id, str) else lesson_id
            
            result = self.lesson_progress_collection.find_one_and_update(
                {'student_id': student_id, 'lesson_id': lesson_id},
                {'$set': {
                    'status': ProgressStatus.COMPLETED.value,
                    'completed_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }},
                return_document=True
            )
            
            if not result:
                raise NotFoundError('Lesson progress not found')
            
            return LessonProgress.from_dict(result)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to complete lesson: {str(e)}")
    
    def get_lesson_progress(self, student_id, lesson_id):
        """Get lesson progress for a student"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            lesson_id = ObjectId(lesson_id) if isinstance(lesson_id, str) else lesson_id
            
            progress = self.lesson_progress_collection.find_one({
                'student_id': student_id,
                'lesson_id': lesson_id
            })
            
            if not progress:
                raise NotFoundError('Lesson progress not found')
            
            return LessonProgress.from_dict(progress)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get lesson progress: {str(e)}")
    
    def get_course_lessons_progress(self, student_id, course_id):
        """Get all lesson progress for a course"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            progress_list = list(self.lesson_progress_collection.find({
                'student_id': student_id,
                'course_id': course_id
            }))
            
            return [LessonProgress.from_dict(p) for p in progress_list]
        
        except Exception as e:
            raise Exception(f"Failed to get course lesson progress: {str(e)}")
    
    # Course Progress Methods
    def initialize_course_progress(self, student_id, course_id, total_lessons=0):
        """Initialize course progress for a student"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            existing = self.course_progress_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if existing:
                return CourseProgress.from_dict(existing)
            
            progress = CourseProgress(
                student_id=student_id,
                course_id=course_id,
                total_lessons=total_lessons
            )
            
            result = self.course_progress_collection.insert_one(progress.__dict__)
            progress._id = result.inserted_id
            return progress
        
        except Exception as e:
            raise Exception(f"Failed to initialize course progress: {str(e)}")
    
    def update_course_progress(self, student_id, course_id):
        """Update overall course progress based on lesson completions"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            # Get all lesson progress
            lessons = list(self.lesson_progress_collection.find({
                'student_id': student_id,
                'course_id': course_id
            }))
            
            total_lessons = len(lessons)
            completed_lessons = sum(1 for l in lessons if l['status'] == ProgressStatus.COMPLETED.value)
            
            overall_progress = 0
            if total_lessons > 0:
                overall_progress = int((completed_lessons / total_lessons) * 100)
            
            result = self.course_progress_collection.find_one_and_update(
                {'student_id': student_id, 'course_id': course_id},
                {'$set': {
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_lessons,
                    'overall_progress': overall_progress,
                    'last_accessed': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }},
                return_document=True
            )
            
            if not result:
                raise NotFoundError('Course progress not found')
            
            return CourseProgress.from_dict(result)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to update course progress: {str(e)}")
    
    def get_course_progress(self, student_id, course_id):
        """Get course progress for a student"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            progress = self.course_progress_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if not progress:
                raise NotFoundError('Course progress not found')
            
            return CourseProgress.from_dict(progress)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get course progress: {str(e)}")
    
    def get_student_courses_progress(self, student_id, page=1, page_size=10):
        """Get all course progress for a student"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            
            skip = (page - 1) * page_size
            
            total = self.course_progress_collection.count_documents({'student_id': student_id})
            
            progress_list = list(self.course_progress_collection.find({
                'student_id': student_id
            }).sort('last_accessed', -1).skip(skip).limit(page_size))
            
            return [CourseProgress.from_dict(p) for p in progress_list], total
        
        except Exception as e:
            raise Exception(f"Failed to get student courses progress: {str(e)}")
    
    # Assessment Progress Methods
    def update_assessment_progress(self, student_id, assessment_id, course_id, score):
        """Update assessment progress after submission"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            assessment_id = ObjectId(assessment_id) if isinstance(assessment_id, str) else assessment_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            if not isinstance(score, (int, float)):
                raise ValidationError('Score must be a number')
            
            existing = self.assessment_progress_collection.find_one({
                'student_id': student_id,
                'assessment_id': assessment_id
            })
            
            if existing:
                # Update existing record
                best_score = max(existing['best_score'], score)
                attempts = existing['attempts'] + 1
                
                result = self.assessment_progress_collection.find_one_and_update(
                    {'_id': existing['_id']},
                    {'$set': {
                        'best_score': best_score,
                        'last_score': score,
                        'attempts': attempts,
                        'last_attempt_date': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }},
                    return_document=True
                )
                
                return AssessmentProgress.from_dict(result)
            else:
                # Create new record
                progress = AssessmentProgress(
                    student_id=student_id,
                    assessment_id=assessment_id,
                    course_id=course_id,
                    best_score=score,
                    last_score=score,
                    attempts=1,
                    first_attempt_date=datetime.utcnow()
                )
                
                insert_result = self.assessment_progress_collection.insert_one(progress.__dict__)
                progress._id = insert_result.inserted_id
                return progress
        
        except ValidationError:
            raise
        except Exception as e:
            raise Exception(f"Failed to update assessment progress: {str(e)}")
    
    def get_assessment_progress(self, student_id, assessment_id):
        """Get assessment progress for a student"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            assessment_id = ObjectId(assessment_id) if isinstance(assessment_id, str) else assessment_id
            
            progress = self.assessment_progress_collection.find_one({
                'student_id': student_id,
                'assessment_id': assessment_id
            })
            
            if not progress:
                raise NotFoundError('Assessment progress not found')
            
            return AssessmentProgress.from_dict(progress)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get assessment progress: {str(e)}")
    
    def get_course_assessments_progress(self, student_id, course_id):
        """Get assessment progress for all assessments in a course"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            progress_list = list(self.assessment_progress_collection.find({
                'student_id': student_id,
                'course_id': course_id
            }))
            
            return [AssessmentProgress.from_dict(p) for p in progress_list]
        
        except Exception as e:
            raise Exception(f"Failed to get course assessments progress: {str(e)}")
