from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response, paginated_response
from app.utils.auth import require_auth, require_role, get_current_user
from app.services.assessment_service import AssessmentService
from app.models.user import UserRole
from app.utils.errors import ValidationError, NotFoundError, ConflictError
from bson import ObjectId

bp = Blueprint('assessments', __name__, url_prefix='/assessments')


@bp.route('', methods=['GET'])
@require_auth
def list_assessments():
    """List assessments with optional course filter"""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        course_id = request.args.get('course_id')
        assessment_type = request.args.get('type')
        
        if page < 1 or page_size < 1 or page_size > current_app.config['MAX_PAGE_SIZE']:
            return error_response('Invalid pagination parameters', 400)
        
        service = AssessmentService(current_app.db)
        filters = {}
        if course_id:
            filters['course_id'] = course_id
        if assessment_type:
            filters['type'] = assessment_type
        
        assessments, total = service.list_assessments(page, page_size, filters)
        assessments_data = [assessment.to_dict() for assessment in assessments]
        
        return paginated_response(assessments_data, total, page, page_size, 'Assessments retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<assessment_id>', methods=['GET'])
@require_auth
def get_assessment(assessment_id):
    """Get assessment details"""
    try:
        service = AssessmentService(current_app.db)
        assessment = service.get_assessment_by_id(assessment_id, include_questions=True)
        
        assessment_data = assessment.to_dict()
        if hasattr(assessment, 'questions'):
            assessment_data['questions'] = [q.to_dict() for q in assessment.questions]
        
        return success_response({'assessment': assessment_data}, 'Assessment retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('', methods=['POST'])
@require_role(UserRole.TEACHER.value, UserRole.ADMIN.value)
def create_assessment():
    """Create a new assessment"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['title', 'course_id', 'assessment_type']):
            return error_response('Missing required fields: title, course_id, assessment_type', 400)
        
        title = data.get('title', '').strip()
        assessment_type = data.get('assessment_type', '').lower()
        
        if len(title) < 3:
            return error_response('Title must be at least 3 characters', 400)
        if assessment_type not in ['quiz', 'assignment', 'exam', 'practice']:
            return error_response('Invalid assessment type', 400)
        
        service = AssessmentService(current_app.db)
        assessment = service.create_assessment(
            title=title,
            course_id=data.get('course_id'),
            assessment_type=assessment_type,
            description=data.get('description', ''),
            instructions=data.get('instructions', ''),
            due_date=data.get('due_date'),
            total_points=data.get('total_points', 100),
            time_limit=data.get('time_limit'),
            attempts_allowed=data.get('attempts_allowed', 1),
            shuffle_questions=data.get('shuffle_questions', False),
            show_answers=data.get('show_answers', False),
            is_published=data.get('is_published', False),
        )
        
        return success_response({'assessment': assessment.to_dict()}, 'Assessment created successfully', 201), 201
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<assessment_id>', methods=['PUT'])
@require_auth
def update_assessment(assessment_id):
    """Update assessment information"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        service = AssessmentService(current_app.db)
        assessment = service.get_assessment_by_id(assessment_id)
        
        # Check authorization (course instructor or admin)
        if user_data.get('role') != UserRole.ADMIN.value:
            # Verify user is the course instructor
            from app.services.course_service import CourseService
            course_service = CourseService(current_app.db)
            course = course_service.get_course_by_id(str(assessment.course_id))
            if user_id != str(course.instructor_id):
                return error_response('You do not have permission to update this assessment', 403)
        
        updated_assessment = service.update_assessment(assessment_id, **data)
        
        return success_response({'assessment': updated_assessment.to_dict()}, 'Assessment updated successfully')
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<assessment_id>', methods=['DELETE'])
@require_auth
def delete_assessment(assessment_id):
    """Delete assessment"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        
        service = AssessmentService(current_app.db)
        assessment = service.get_assessment_by_id(assessment_id)
        
        # Check authorization
        if user_data.get('role') != UserRole.ADMIN.value:
            from app.services.course_service import CourseService
            course_service = CourseService(current_app.db)
            course = course_service.get_course_by_id(str(assessment.course_id))
            if user_id != str(course.instructor_id):
                return error_response('You do not have permission to delete this assessment', 403)
        
        service.delete_assessment(assessment_id)
        
        return success_response(None, 'Assessment deleted successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<assessment_id>/questions', methods=['POST'])
@require_auth
def add_question(assessment_id):
    """Add a question to an assessment"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        data = request.get_json()
        
        if not data or not all(k in data for k in ['question_text', 'question_type']):
            return error_response('Missing required fields: question_text, question_type', 400)
        
        service = AssessmentService(current_app.db)
        assessment = service.get_assessment_by_id(assessment_id)
        
        # Check authorization
        if user_data.get('role') != UserRole.ADMIN.value:
            from app.services.course_service import CourseService
            course_service = CourseService(current_app.db)
            course = course_service.get_course_by_id(str(assessment.course_id))
            if user_id != str(course.instructor_id):
                return error_response('You do not have permission to add questions', 403)
        
        question_type = data.get('question_type', '').lower()
        if question_type not in ['multiple_choice', 'short_answer', 'essay', 'true_false']:
            return error_response('Invalid question type', 400)
        
        question = service.create_question(
            assessment_id=assessment_id,
            question_text=data.get('question_text'),
            question_type=question_type,
            points=data.get('points', 1),
            order=data.get('order', 0),
            explanation=data.get('explanation', ''),
            options=data.get('options', []),
            correct_answer=data.get('correct_answer'),
        )
        
        return success_response({'question': question.to_dict()}, 'Question added successfully', 201), 201
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<assessment_id>/submit', methods=['POST'])
@require_auth
def submit_assessment(assessment_id):
    """Submit assessment answers"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        
        if not data or 'answers' not in data:
            return error_response('Missing required field: answers', 400)
        
        answers = data.get('answers', {})  # Dict of question_id: answer
        
        service = AssessmentService(current_app.db)
        assessment = service.get_assessment_by_id(assessment_id)
        
        # Check if assessment is published
        if not assessment.is_published:
            return error_response('This assessment is not available yet', 400)
        
        # Submit the assessment
        submission = service.submit_assessment(user_id, assessment_id, answers)
        
        return success_response({'submission': submission.to_dict()}, 'Assessment submitted successfully', 201), 201
    
    except (ValidationError, NotFoundError, ConflictError) as e:
        if isinstance(e, ConflictError):
            status_code = 409
        elif isinstance(e, ValidationError):
            status_code = 400
        else:
            status_code = 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<assessment_id>/submissions', methods=['GET'])
@require_auth
def get_assessment_submissions(assessment_id):
    """Get all submissions for an assessment (instructor only)"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        service = AssessmentService(current_app.db)
        assessment = service.get_assessment_by_id(assessment_id)
        
        # Check authorization (course instructor or admin)
        if user_data.get('role') != UserRole.ADMIN.value:
            from app.services.course_service import CourseService
            course_service = CourseService(current_app.db)
            course = course_service.get_course_by_id(str(assessment.course_id))
            if user_id != str(course.instructor_id):
                return error_response('You do not have permission to view submissions', 403)
        
        submissions, total = service.get_assessment_submissions(assessment_id, page, page_size)
        submissions_data = [submission.to_dict() for submission in submissions]
        
        return paginated_response(submissions_data, total, page, page_size, 'Submissions retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/submissions/<submission_id>', methods=['GET'])
@require_auth
def get_submission(submission_id):
    """Get a specific submission"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        
        service = AssessmentService(current_app.db)
        submission = service.get_submission_by_id(submission_id)
        
        # Check authorization (student who submitted, or instructor/admin)
        if user_id != str(submission.student_id) and user_data.get('role') != UserRole.ADMIN.value:
            if user_data.get('role') != UserRole.TEACHER.value:
                return error_response('You do not have permission to view this submission', 403)
        
        submission_data = submission.to_dict()
        return success_response({'submission': submission_data}, 'Submission retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/submissions/<submission_id>/grade', methods=['POST'])
@require_auth
def grade_submission(submission_id):
    """Grade a submission (instructor only)"""
    try:
        user_id = get_current_user()
        user_data = g.user_data
        data = request.get_json()
        
        if not data or 'score' not in data:
            return error_response('Missing required field: score', 400)
        
        service = AssessmentService(current_app.db)
        submission = service.get_submission_by_id(submission_id)
        
        # Check authorization (instructor of the course)
        from app.services.course_service import CourseService
        course_service = CourseService(current_app.db)
        assessment = service.get_assessment_by_id(str(submission.assessment_id))
        course = course_service.get_course_by_id(str(assessment.course_id))
        
        if user_id != str(course.instructor_id) and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to grade this submission', 403)
        
        score = data.get('score')
        feedback = data.get('feedback', '')
        
        if not isinstance(score, (int, float)) or score < 0:
            return error_response('Score must be a non-negative number', 400)
        
        graded_submission = service.grade_submission(submission_id, score, feedback)
        
        return success_response({'submission': graded_submission.to_dict()}, 'Submission graded successfully')
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)
