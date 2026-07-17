from datetime import datetime
from bson import ObjectId
from app.models.analytics import CourseAnalytics, StudentAnalytics, LessonAnalytics
from app.utils.errors import NotFoundError


class AnalyticsService:
    """Service for generating analytics and reports"""
    
    def __init__(self, db):
        self.db = db
        self.course_analytics_collection = db.course_analytics
        self.student_analytics_collection = db.student_analytics
        self.lesson_analytics_collection = db.lesson_analytics
    
    # Course Analytics
    def generate_course_analytics(self, course_id):
        """Generate overall analytics for a course"""
        try:
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            # Get enrollment data
            enrollments = list(self.db.enrollments.find({'course_id': course_id}))
            total_students = len(enrollments)
            
            if total_students == 0:
                analytics = CourseAnalytics(course_id=course_id)
                return analytics
            
            # Get student progress data
            progress_records = list(self.db.course_progress.find({'course_id': course_id}))
            
            completed_students = sum(1 for p in progress_records if p.get('overall_progress', 0) == 100)
            active_students = len(progress_records)
            
            avg_progress = 0
            if progress_records:
                avg_progress = sum(p.get('overall_progress', 0) for p in progress_records) / len(progress_records)
            
            # Get assessment scores
            assessments = list(self.db.assessments.find({'course_id': course_id}))
            avg_score = 0
            
            if assessments:
                all_scores = []
                for assessment in assessments:
                    submissions = list(self.db.assessment_submissions.find(
                        {'assessment_id': assessment['_id'], 'is_graded': True}
                    ))
                    all_scores.extend([s.get('final_score', 0) for s in submissions])
                
                if all_scores:
                    avg_score = sum(all_scores) / len(all_scores)
            
            completion_rate = (completed_students / total_students * 100) if total_students > 0 else 0
            
            analytics = CourseAnalytics(
                course_id=course_id,
                total_students=total_students,
                active_students=active_students,
                completed_students=completed_students,
                average_progress=avg_progress,
                average_score=avg_score,
                completion_rate=completion_rate
            )
            
            # Update or insert
            existing = self.course_analytics_collection.find_one({'course_id': course_id})
            if existing:
                self.course_analytics_collection.update_one(
                    {'_id': existing['_id']},
                    {'$set': analytics.__dict__}
                )
                analytics._id = existing['_id']
            else:
                result = self.course_analytics_collection.insert_one(analytics.__dict__)
                analytics._id = result.inserted_id
            
            return analytics
        
        except Exception as e:
            raise Exception(f"Failed to generate course analytics: {str(e)}")
    
    def get_course_analytics(self, course_id):
        """Get analytics for a course"""
        try:
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            analytics = self.course_analytics_collection.find_one({'course_id': course_id})
            if not analytics:
                # Generate if doesn't exist
                return self.generate_course_analytics(course_id)
            
            return CourseAnalytics.from_dict(analytics)
        
        except Exception as e:
            raise Exception(f"Failed to get course analytics: {str(e)}")
    
    # Student Analytics
    def generate_student_analytics(self, student_id, course_id):
        """Generate analytics for a student in a course"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            # Lesson progress
            lesson_progress = list(self.db.lesson_progress.find({
                'student_id': student_id,
                'course_id': course_id
            }))
            
            total_lessons = len(lesson_progress)
            completed_lessons = sum(1 for lp in lesson_progress if lp.get('status') == 'completed')
            lessons_progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
            
            # Assessment progress
            assessments = list(self.db.assessments.find({'course_id': course_id}))
            total_assessments = len(assessments)
            
            completed_assessments = 0
            total_assessment_score = 0
            graded_count = 0
            
            for assessment in assessments:
                submission = self.db.assessment_submissions.find_one({
                    'student_id': student_id,
                    'assessment_id': assessment['_id']
                })
                
                if submission:
                    completed_assessments += 1
                    if submission.get('is_graded'):
                        total_assessment_score += submission.get('final_score', 0)
                        graded_count += 1
            
            assessments_completion = (completed_assessments / total_assessments * 100) if total_assessments > 0 else 0
            avg_assessment_score = (total_assessment_score / graded_count) if graded_count > 0 else 0
            
            # Points
            points_record = self.db.points.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            total_points = points_record.get('total_points', 0) if points_record else 0
            
            # Time spent
            total_time_spent = sum(lp.get('time_spent', 0) for lp in lesson_progress)
            
            # Last activity
            course_progress = self.db.course_progress.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            last_activity = course_progress.get('last_accessed') if course_progress else datetime.utcnow()
            
            analytics = StudentAnalytics(
                student_id=student_id,
                course_id=course_id,
                total_lessons=total_lessons,
                completed_lessons=completed_lessons,
                lessons_progress=lessons_progress,
                total_assessments=total_assessments,
                completed_assessments=completed_assessments,
                assessments_completion=assessments_completion,
                average_assessment_score=avg_assessment_score,
                total_points=total_points,
                total_time_spent=total_time_spent,
                last_activity=last_activity
            )
            
            # Update or insert
            existing = self.student_analytics_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            if existing:
                self.student_analytics_collection.update_one(
                    {'_id': existing['_id']},
                    {'$set': analytics.__dict__}
                )
                analytics._id = existing['_id']
            else:
                result = self.student_analytics_collection.insert_one(analytics.__dict__)
                analytics._id = result.inserted_id
            
            return analytics
        
        except Exception as e:
            raise Exception(f"Failed to generate student analytics: {str(e)}")
    
    def get_student_analytics(self, student_id, course_id):
        """Get analytics for a student in a course"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            analytics = self.student_analytics_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            if not analytics:
                return self.generate_student_analytics(student_id, course_id)
            
            return StudentAnalytics.from_dict(analytics)
        
        except Exception as e:
            raise Exception(f"Failed to get student analytics: {str(e)}")
    
    # Lesson Analytics
    def generate_lesson_analytics(self, lesson_id, course_id):
        """Generate analytics for a lesson"""
        try:
            lesson_id = ObjectId(lesson_id) if isinstance(lesson_id, str) else lesson_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            # Get all lesson progress records
            lesson_progress = list(self.db.lesson_progress.find({
                'lesson_id': lesson_id,
                'course_id': course_id
            }))
            
            total_started = len(lesson_progress)
            completed = sum(1 for lp in lesson_progress if lp.get('status') == 'completed')
            completion_rate = (completed / total_started * 100) if total_started > 0 else 0
            
            avg_time_spent = 0
            if lesson_progress:
                total_time = sum(lp.get('time_spent', 0) for lp in lesson_progress)
                avg_time_spent = total_time / len(lesson_progress)
            
            analytics = LessonAnalytics(
                lesson_id=lesson_id,
                course_id=course_id,
                total_started=total_started,
                total_completed=completed,
                completion_rate=completion_rate,
                average_time_spent=avg_time_spent
            )
            
            # Update or insert
            existing = self.lesson_analytics_collection.find_one({
                'lesson_id': lesson_id,
                'course_id': course_id
            })
            if existing:
                self.lesson_analytics_collection.update_one(
                    {'_id': existing['_id']},
                    {'$set': analytics.__dict__}
                )
                analytics._id = existing['_id']
            else:
                result = self.lesson_analytics_collection.insert_one(analytics.__dict__)
                analytics._id = result.inserted_id
            
            return analytics
        
        except Exception as e:
            raise Exception(f"Failed to generate lesson analytics: {str(e)}")
    
    def get_lesson_analytics(self, lesson_id, course_id):
        """Get analytics for a lesson"""
        try:
            lesson_id = ObjectId(lesson_id) if isinstance(lesson_id, str) else lesson_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            analytics = self.lesson_analytics_collection.find_one({
                'lesson_id': lesson_id,
                'course_id': course_id
            })
            if not analytics:
                return self.generate_lesson_analytics(lesson_id, course_id)
            
            return LessonAnalytics.from_dict(analytics)
        
        except Exception as e:
            raise Exception(f"Failed to get lesson analytics: {str(e)}")
