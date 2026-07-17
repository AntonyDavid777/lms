from datetime import datetime, timedelta
from bson import ObjectId
from app.models.gamification import (
    Badge, StudentBadge, Points, LeaderboardEntry, Streak
)
from app.utils.errors import NotFoundError, ValidationError


class GamificationService:
    """Service for managing gamification features"""
    
    def __init__(self, db):
        self.db = db
        self.badges_collection = db.badges
        self.student_badges_collection = db.student_badges
        self.points_collection = db.points
        self.leaderboard_collection = db.leaderboard
        self.streaks_collection = db.streaks
    
    # Badge Management
    def create_badge(self, name, description, badge_type, icon_url="", 
                     requirement_type="", requirement_value=0):
        """Create a new badge"""
        try:
            if not name or not description:
                raise ValidationError("Badge name and description are required")
            
            badge = Badge(
                name=name,
                description=description,
                badge_type=badge_type,
                icon_url=icon_url,
                requirement_type=requirement_type,
                requirement_value=requirement_value
            )
            
            result = self.badges_collection.insert_one(badge.__dict__)
            badge._id = result.inserted_id
            return badge
        
        except ValidationError:
            raise
        except Exception as e:
            raise Exception(f"Failed to create badge: {str(e)}")
    
    def get_badge_by_id(self, badge_id):
        """Get badge by ID"""
        try:
            badge_id = ObjectId(badge_id) if isinstance(badge_id, str) else badge_id
            badge_data = self.badges_collection.find_one({'_id': badge_id})
            
            if not badge_data:
                raise NotFoundError('Badge not found')
            
            return Badge.from_dict(badge_data)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get badge: {str(e)}")
    
    def award_badge(self, student_id, badge_id):
        """Award a badge to a student"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            badge_id = ObjectId(badge_id) if isinstance(badge_id, str) else badge_id
            
            # Check if already earned
            existing = self.student_badges_collection.find_one({
                'student_id': student_id,
                'badge_id': badge_id
            })
            
            if existing:
                raise ValidationError('Student already has this badge')
            
            student_badge = StudentBadge(student_id=student_id, badge_id=badge_id)
            result = self.student_badges_collection.insert_one(student_badge.__dict__)
            student_badge._id = result.inserted_id
            return student_badge
        
        except ValidationError:
            raise
        except Exception as e:
            raise Exception(f"Failed to award badge: {str(e)}")
    
    def get_student_badges(self, student_id):
        """Get all badges for a student"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            
            badges = list(self.student_badges_collection.find({'student_id': student_id}))
            return [StudentBadge.from_dict(b) for b in badges]
        
        except Exception as e:
            raise Exception(f"Failed to get student badges: {str(e)}")
    
    # Points Management
    def initialize_points(self, student_id, course_id):
        """Initialize points for a student in a course"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            existing = self.points_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if existing:
                return Points.from_dict(existing)
            
            points = Points(student_id=student_id, course_id=course_id)
            result = self.points_collection.insert_one(points.__dict__)
            points._id = result.inserted_id
            return points
        
        except Exception as e:
            raise Exception(f"Failed to initialize points: {str(e)}")
    
    def add_points(self, student_id, course_id, point_type, points_value):
        """Add points to a student for a specific activity"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            if point_type not in ['lesson', 'quiz', 'assignment', 'participation']:
                raise ValidationError('Invalid point type')
            
            if not isinstance(points_value, (int, float)) or points_value < 0:
                raise ValidationError('Points value must be non-negative')
            
            # Get or create points record
            existing = self.points_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if not existing:
                self.initialize_points(student_id, course_id)
                existing = self.points_collection.find_one({
                    'student_id': student_id,
                    'course_id': course_id
                })
            
            # Update points
            update_data = {}
            if point_type == 'lesson':
                update_data['lesson_points'] = existing.get('lesson_points', 0) + points_value
            elif point_type == 'quiz':
                update_data['quiz_points'] = existing.get('quiz_points', 0) + points_value
            elif point_type == 'assignment':
                update_data['assignment_points'] = existing.get('assignment_points', 0) + points_value
            elif point_type == 'participation':
                update_data['participation_points'] = existing.get('participation_points', 0) + points_value
            
            update_data['total_points'] = (
                existing.get('lesson_points', 0) +
                existing.get('quiz_points', 0) +
                existing.get('assignment_points', 0) +
                existing.get('participation_points', 0) +
                sum(update_data.values())
            )
            update_data['updated_at'] = datetime.utcnow()
            
            result = self.points_collection.find_one_and_update(
                {'_id': existing['_id']},
                {'$set': update_data},
                return_document=True
            )
            
            return Points.from_dict(result)
        
        except ValidationError:
            raise
        except Exception as e:
            raise Exception(f"Failed to add points: {str(e)}")
    
    def get_student_points(self, student_id, course_id):
        """Get points for a student in a course"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            points = self.points_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if not points:
                raise NotFoundError('Points record not found')
            
            return Points.from_dict(points)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get student points: {str(e)}")
    
    # Leaderboard Management
    def update_leaderboard(self, course_id):
        """Update leaderboard rankings for a course"""
        try:
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            # Get all points for the course, sorted by total_points
            points_list = list(self.points_collection.find(
                {'course_id': course_id}
            ).sort('total_points', -1))
            
            # Clear existing leaderboard for this course
            self.leaderboard_collection.delete_many({'course_id': course_id})
            
            # Create new leaderboard entries
            for rank, points_data in enumerate(points_list, 1):
                # Get student name
                from app.models.user import User
                student = self.db.users.find_one({'_id': points_data['student_id']})
                student_name = student.get('name', 'Unknown') if student else 'Unknown'
                
                entry = LeaderboardEntry(
                    student_id=points_data['student_id'],
                    student_name=student_name,
                    course_id=course_id,
                    total_points=points_data['total_points'],
                    rank=rank
                )
                
                self.leaderboard_collection.insert_one(entry.__dict__)
            
            return True
        
        except Exception as e:
            raise Exception(f"Failed to update leaderboard: {str(e)}")
    
    def get_leaderboard(self, course_id, limit=10):
        """Get top students on leaderboard"""
        try:
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            entries = list(self.leaderboard_collection.find(
                {'course_id': course_id}
            ).sort('rank', 1).limit(limit))
            
            return [LeaderboardEntry.from_dict(e) for e in entries]
        
        except Exception as e:
            raise Exception(f"Failed to get leaderboard: {str(e)}")
    
    def get_student_rank(self, student_id, course_id):
        """Get student's rank on leaderboard"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            entry = self.leaderboard_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if not entry:
                raise NotFoundError('Leaderboard entry not found')
            
            return LeaderboardEntry.from_dict(entry)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get student rank: {str(e)}")
    
    # Streak Management
    def initialize_streak(self, student_id, course_id):
        """Initialize streak for a student in a course"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            existing = self.streaks_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if existing:
                return Streak.from_dict(existing)
            
            streak = Streak(student_id=student_id, course_id=course_id)
            result = self.streaks_collection.insert_one(streak.__dict__)
            streak._id = result.inserted_id
            return streak
        
        except Exception as e:
            raise Exception(f"Failed to initialize streak: {str(e)}")
    
    def update_streak(self, student_id, course_id):
        """Update streak when student completes activity"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            existing = self.streaks_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if not existing:
                self.initialize_streak(student_id, course_id)
                existing = self.streaks_collection.find_one({
                    'student_id': student_id,
                    'course_id': course_id
                })
            
            last_activity = existing.get('last_activity_date')
            now = datetime.utcnow()
            
            # Check if streak continues (activity within last 24 hours + some buffer)
            if last_activity and (now - last_activity).days <= 1:
                # Continue or increment streak
                current_streak = existing.get('current_streak', 0) + 1
            else:
                # Reset streak
                current_streak = 1
            
            # Update longest streak if needed
            longest_streak = existing.get('longest_streak', 0)
            if current_streak > longest_streak:
                longest_streak = current_streak
            
            result = self.streaks_collection.find_one_and_update(
                {'_id': existing['_id']},
                {'$set': {
                    'current_streak': current_streak,
                    'longest_streak': longest_streak,
                    'last_activity_date': now,
                    'updated_at': now
                }},
                return_document=True
            )
            
            return Streak.from_dict(result)
        
        except Exception as e:
            raise Exception(f"Failed to update streak: {str(e)}")
    
    def get_streak(self, student_id, course_id):
        """Get streak information"""
        try:
            student_id = ObjectId(student_id) if isinstance(student_id, str) else student_id
            course_id = ObjectId(course_id) if isinstance(course_id, str) else course_id
            
            streak = self.streaks_collection.find_one({
                'student_id': student_id,
                'course_id': course_id
            })
            
            if not streak:
                raise NotFoundError('Streak not found')
            
            return Streak.from_dict(streak)
        
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get streak: {str(e)}")
