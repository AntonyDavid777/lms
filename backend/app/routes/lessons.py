from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth, require_role, get_current_user
from app.services.course_service import CourseService
from app.models.user import UserRole
from app.utils.errors import ValidationError, NotFoundError
from bson import ObjectId

bp = Blueprint('lessons', __name__, url_prefix='/lessons')


@bp.route('/<lesson_id>', methods=['GET'])
@require_auth
def get_lesson(lesson_id):
    """Get lesson details"""
    try:
        service = CourseService(current_app.db)
        lesson = service.get_lesson_by_id(lesson_id)
        
        return success_response({'lesson': lesson.to_dict()}, 'Lesson retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<lesson_id>', methods=['PUT'])
@require_auth
def update_lesson(lesson_id):
    """Update lesson information"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        service = CourseService(current_app.db)
        lesson = service.get_lesson_by_id(lesson_id)
        course = service.get_course_by_id(str(lesson.course_id))
        
        # Check authorization
        if user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to update this lesson', 403)
        
        updated_lesson = service.update_lesson(lesson_id, **data)
        
        return success_response({'lesson': updated_lesson.to_dict()}, 'Lesson updated successfully')
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<lesson_id>', methods=['DELETE'])
@require_auth
def delete_lesson(lesson_id):
    """Delete lesson"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        
        service = CourseService(current_app.db)
        lesson = service.get_lesson_by_id(lesson_id)
        course = service.get_course_by_id(str(lesson.course_id))
        
        # Check authorization
        if user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to delete this lesson', 403)
        
        service.delete_lesson(lesson_id)
        
        return success_response(None, 'Lesson deleted successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)
