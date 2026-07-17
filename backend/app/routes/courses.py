from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response, paginated_response
from app.utils.auth import require_auth, require_role, get_current_user
from app.services.course_service import CourseService
from app.models.user import UserRole
from app.utils.errors import ValidationError, NotFoundError, ConflictError
from bson import ObjectId

bp = Blueprint('courses', __name__, url_prefix='/courses')


@bp.route('', methods=['GET'])
def list_courses():
    """List all published courses with optional filters"""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        category = request.args.get('category')
        level = request.args.get('level')
        search = request.args.get('search')
        
        # Validate pagination
        if page < 1:
            return error_response('Page must be >= 1', 400)
        if page_size < 1 or page_size > current_app.config['MAX_PAGE_SIZE']:
            return error_response(f'Page size must be between 1 and {current_app.config["MAX_PAGE_SIZE"]}', 400)
        
        service = CourseService(current_app.db)
        
        filters = {}
        if category:
            filters['category'] = category
        if level:
            filters['level'] = level
        if search:
            filters['search'] = search
        
        # Non-authenticated users can only see published courses
        status = 'published' if not get_current_user() else None
        
        courses, total = service.list_courses(page, page_size, filters, status)
        courses_data = [course.to_dict() for course in courses]
        
        return paginated_response(courses_data, total, page, page_size, 'Courses retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    """Get course details"""
    try:
        service = CourseService(current_app.db)
        course = service.get_course_by_id(course_id, include_lessons=True)
        
        # Check if user has access to see this course
        user_id = get_current_user()
        user_data = g.user_data if hasattr(g, 'user_data') else {}
        
        if course.status == 'draft' and user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('This course is not available', 404)
        
        course_data = course.to_dict(include_lesson_ids=True)
        
        # Add lessons if they exist
        if hasattr(course, 'lessons'):
            course_data['lessons'] = [lesson.to_dict() for lesson in course.lessons]
        
        return success_response({'course': course_data}, 'Course retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('', methods=['POST'])
@require_role(UserRole.TEACHER.value, UserRole.ADMIN.value)
def create_course():
    """Create a new course"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['title', 'description']):
            return error_response('Missing required fields: title, description', 400)
        
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        category = data.get('category', '').strip()
        level = data.get('level', 'beginner')
        
        if len(title) < 3:
            return error_response('Title must be at least 3 characters', 400)
        if len(description) < 10:
            return error_response('Description must be at least 10 characters', 400)
        
        service = CourseService(current_app.db)
        course = service.create_course(
            title=title,
            description=description,
            instructor_id=get_current_user(),
            category=category,
            level=level,
            thumbnail_url=data.get('thumbnail_url', ''),
        )
        
        return success_response({'course': course.to_dict()}, 'Course created successfully', 201), 201
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>', methods=['PUT'])
@require_auth
def update_course(course_id):
    """Update course information"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        service = CourseService(current_app.db)
        course = service.get_course_by_id(course_id)
        
        # Check authorization
        if user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to update this course', 403)
        
        updated_course = service.update_course(course_id, **data)
        
        return success_response({'course': updated_course.to_dict()}, 'Course updated successfully')
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>', methods=['DELETE'])
@require_auth
def delete_course(course_id):
    """Delete course"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        
        service = CourseService(current_app.db)
        course = service.get_course_by_id(course_id)
        
        # Check authorization
        if user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to delete this course', 403)
        
        service.delete_course(course_id)
        
        return success_response(None, 'Course deleted successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>/enroll', methods=['POST'])
@require_auth
def enroll_course(course_id):
    """Enroll student in a course"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        
        # Only students can enroll
        if user_data.get('role') != UserRole.STUDENT.value:
            return error_response('Only students can enroll in courses', 403)
        
        service = CourseService(current_app.db)
        course = service.get_course_by_id(course_id)
        
        # Check if course is published
        if course.status != 'published':
            return error_response('This course is not available for enrollment', 400)
        
        enrollment = service.enroll_student(user_id, course_id)
        
        return success_response({'enrollment': enrollment.to_dict()}, 'Successfully enrolled in course', 201), 201
    
    except (ConflictError, NotFoundError) as e:
        status_code = 409 if isinstance(e, ConflictError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>/unenroll', methods=['DELETE'])
@require_auth
def unenroll_course(course_id):
    """Unenroll student from a course"""
    try:
        user_id = get_current_user()
        
        service = CourseService(current_app.db)
        service.unenroll_student(user_id, course_id)
        
        return success_response(None, 'Successfully unenrolled from course')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>/enrolled-students', methods=['GET'])
@require_auth
def get_enrolled_students(course_id):
    """Get students enrolled in a course"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        service = CourseService(current_app.db)
        course = service.get_course_by_id(course_id)
        
        # Check authorization (teacher or admin of the course)
        if user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to view this', 403)
        
        enrollments, total = service.get_enrolled_students(course_id, page, page_size)
        enrollments_data = [enrollment.to_dict() for enrollment in enrollments]
        
        return paginated_response(enrollments_data, total, page, page_size, 'Enrolled students retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>/lessons', methods=['GET'])
@require_auth
def get_course_lessons(course_id):
    """Get all lessons in a course"""
    try:
        service = CourseService(current_app.db)
        course = service.get_course_by_id(course_id)
        
        lessons = service.get_course_lessons(course_id)
        lessons_data = [lesson.to_dict() for lesson in lessons]
        
        return success_response({
            'course_id': course_id,
            'lessons': lessons_data,
            'total': len(lessons_data)
        }, 'Lessons retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<course_id>/lessons', methods=['POST'])
@require_auth
def add_lesson(course_id):
    """Add a lesson to a course"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        data = request.get_json()
        
        if not data or not all(k in data for k in ['title', 'description', 'order']):
            return error_response('Missing required fields: title, description, order', 400)
        
        service = CourseService(current_app.db)
        course = service.get_course_by_id(course_id)
        
        # Check authorization
        if user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to add lessons to this course', 403)
        
        lesson = service.create_lesson(
            title=data.get('title'),
            description=data.get('description'),
            course_id=course_id,
            order=data.get('order'),
            content=data.get('content', ''),
            content_type=data.get('content_type', 'text'),
            video_url=data.get('video_url', ''),
            duration=data.get('duration', 0),
            learning_objectives=data.get('learning_objectives', []),
            resources_url=data.get('resources_url', []),
        )
        
        return success_response({'lesson': lesson.to_dict()}, 'Lesson created successfully', 201), 201
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)
