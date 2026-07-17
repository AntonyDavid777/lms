from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth, require_role, get_current_user
from app.services.analytics_service import AnalyticsService
from app.models.user import UserRole
from app.utils.errors import NotFoundError

bp = Blueprint('analytics', __name__, url_prefix='/analytics')


@bp.route('/courses/<course_id>', methods=['GET'])
@require_role(UserRole.TEACHER.value, UserRole.ADMIN.value)
def get_course_analytics(course_id):
    """Get overall course analytics (instructor/admin only)"""
    try:
        service = AnalyticsService(current_app.db)
        analytics = service.generate_course_analytics(course_id)
        
        return success_response({'analytics': analytics.to_dict()}, 'Course analytics retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/courses/<course_id>/students/<student_id>', methods=['GET'])
@require_auth
def get_student_course_analytics(course_id, student_id):
    """Get student analytics for a course"""
    try:
        current_user_id = get_current_user()
        user_data = g.user_data
        
        # Students can only view their own analytics, teachers/admins can view anyone
        if current_user_id != student_id and user_data.get('role') not in [UserRole.TEACHER.value, UserRole.ADMIN.value]:
            return error_response('You do not have permission to view these analytics', 403)
        
        service = AnalyticsService(current_app.db)
        analytics = service.generate_student_analytics(student_id, course_id)
        
        return success_response({'analytics': analytics.to_dict()}, 'Student analytics retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/my-analytics/<course_id>', methods=['GET'])
@require_auth
def get_my_analytics(course_id):
    """Get current student's analytics for a course"""
    try:
        student_id = get_current_user()
        
        service = AnalyticsService(current_app.db)
        analytics = service.generate_student_analytics(student_id, course_id)
        
        return success_response({'analytics': analytics.to_dict()}, 'Your analytics retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/courses/<course_id>/lessons/<lesson_id>', methods=['GET'])
@require_role(UserRole.TEACHER.value, UserRole.ADMIN.value)
def get_lesson_analytics(course_id, lesson_id):
    """Get lesson-level analytics (instructor/admin only)"""
    try:
        service = AnalyticsService(current_app.db)
        analytics = service.generate_lesson_analytics(lesson_id, course_id)
        
        return success_response({'analytics': analytics.to_dict()}, 'Lesson analytics retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/admin/dashboard', methods=['GET'])
@require_role(UserRole.ADMIN.value)
def get_admin_dashboard_analytics():
    """Get overall platform analytics for admin dashboard (admin only)"""
    try:
        service = AnalyticsService(current_app.db)
        analytics = service.get_admin_dashboard_analytics()
        
        return success_response(analytics, 'Admin dashboard analytics retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)
