from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response, paginated_response
from app.utils.auth import require_auth, get_current_user
from app.services.progress_service import ProgressService
from app.utils.errors import NotFoundError, ValidationError

bp = Blueprint('progress', __name__, url_prefix='/progress')


@bp.route('/lessons/<lesson_id>/start', methods=['POST'])
@require_auth
def start_lesson(lesson_id):
    """Mark a lesson as started"""
    try:
        student_id = get_current_user()
        data = request.get_json()
        
        if not data or 'course_id' not in data:
            return error_response('Missing required field: course_id', 400)
        
        course_id = data.get('course_id')
        
        service = ProgressService(current_app.db)
        progress = service.start_lesson(student_id, lesson_id, course_id)
        
        return success_response({'progress': progress.to_dict()}, 'Lesson started successfully', 201), 201
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/lessons/<lesson_id>/complete', methods=['POST'])
@require_auth
def complete_lesson(lesson_id):
    """Mark a lesson as completed"""
    try:
        student_id = get_current_user()
        data = request.get_json()
        
        if not data or 'course_id' not in data:
            return error_response('Missing required field: course_id', 400)
        
        course_id = data.get('course_id')
        
        service = ProgressService(current_app.db)
        progress = service.complete_lesson(student_id, lesson_id)
        
        # Update course progress
        service.update_course_progress(student_id, course_id)
        
        return success_response({'progress': progress.to_dict()}, 'Lesson completed successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/lessons/<lesson_id>', methods=['GET'])
@require_auth
def get_lesson_progress(lesson_id):
    """Get progress for a specific lesson"""
    try:
        student_id = get_current_user()
        
        service = ProgressService(current_app.db)
        progress = service.get_lesson_progress(student_id, lesson_id)
        
        return success_response({'progress': progress.to_dict()}, 'Lesson progress retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/courses/<course_id>/lessons', methods=['GET'])
@require_auth
def get_course_lessons_progress(course_id):
    """Get progress for all lessons in a course"""
    try:
        student_id = get_current_user()
        
        service = ProgressService(current_app.db)
        progress_list = service.get_course_lessons_progress(student_id, course_id)
        
        progress_data = [p.to_dict() for p in progress_list]
        
        return success_response({
            'course_id': course_id,
            'lessons_progress': progress_data,
            'total': len(progress_data)
        }, 'Lesson progress retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/courses/<course_id>', methods=['GET'])
@require_auth
def get_course_progress(course_id):
    """Get overall course progress"""
    try:
        student_id = get_current_user()
        
        service = ProgressService(current_app.db)
        progress = service.get_course_progress(student_id, course_id)
        
        return success_response({'progress': progress.to_dict()}, 'Course progress retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/courses', methods=['GET'])
@require_auth
def get_all_courses_progress():
    """Get progress for all enrolled courses"""
    try:
        student_id = get_current_user()
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        if page < 1 or page_size < 1 or page_size > current_app.config['MAX_PAGE_SIZE']:
            return error_response('Invalid pagination parameters', 400)
        
        service = ProgressService(current_app.db)
        progress_list, total = service.get_student_courses_progress(student_id, page, page_size)
        
        progress_data = [p.to_dict() for p in progress_list]
        
        return paginated_response(progress_data, total, page, page_size, 'Courses progress retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/assessments/<assessment_id>', methods=['GET'])
@require_auth
def get_assessment_progress(assessment_id):
    """Get assessment progress for a student"""
    try:
        student_id = get_current_user()
        
        service = ProgressService(current_app.db)
        progress = service.get_assessment_progress(student_id, assessment_id)
        
        return success_response({'progress': progress.to_dict()}, 'Assessment progress retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/courses/<course_id>/assessments', methods=['GET'])
@require_auth
def get_course_assessments_progress(course_id):
    """Get assessment progress for all assessments in a course"""
    try:
        student_id = get_current_user()
        
        service = ProgressService(current_app.db)
        progress_list = service.get_course_assessments_progress(student_id, course_id)
        
        progress_data = [p.to_dict() for p in progress_list]
        
        return success_response({
            'course_id': course_id,
            'assessments_progress': progress_data,
            'total': len(progress_data)
        }, 'Assessment progress retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)
