from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth, require_role, get_current_user
from app.services.gamification_service import GamificationService
from app.models.user import UserRole
from app.utils.errors import NotFoundError, ValidationError

bp = Blueprint('gamification', __name__, url_prefix='/gamification')


@bp.route('/badges', methods=['GET'])
def list_badges():
    """List all available badges"""
    try:
        service = GamificationService(current_app.db)
        badges = list(current_app.db.badges.find())
        
        badges_data = []
        for badge in badges:
            from app.models.gamification import Badge
            b = Badge.from_dict(badge)
            badges_data.append(b.to_dict())
        
        return success_response({
            'badges': badges_data,
            'total': len(badges_data)
        }, 'Badges retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/badges', methods=['POST'])
@require_role(UserRole.ADMIN.value)
def create_badge():
    """Create a new badge (admin only)"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'description', 'badge_type']):
            return error_response('Missing required fields: name, description, badge_type', 400)
        
        service = GamificationService(current_app.db)
        badge = service.create_badge(
            name=data.get('name'),
            description=data.get('description'),
            badge_type=data.get('badge_type'),
            icon_url=data.get('icon_url', ''),
            requirement_type=data.get('requirement_type', ''),
            requirement_value=data.get('requirement_value', 0)
        )
        
        return success_response({'badge': badge.to_dict()}, 'Badge created successfully', 201), 201
    
    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/badges/<badge_id>', methods=['GET'])
def get_badge(badge_id):
    """Get badge details"""
    try:
        service = GamificationService(current_app.db)
        badge = service.get_badge_by_id(badge_id)
        
        return success_response({'badge': badge.to_dict()}, 'Badge retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/my-badges', methods=['GET'])
@require_auth
def get_my_badges():
    """Get badges earned by current student"""
    try:
        student_id = get_current_user()
        
        service = GamificationService(current_app.db)
        student_badges = service.get_student_badges(student_id)
        
        # Fetch badge details for each earned badge
        badges_data = []
        for sb in student_badges:
            badge = service.get_badge_by_id(str(sb.badge_id))
            badge_dict = badge.to_dict()
            badge_dict['earned_at'] = sb.earned_at.isoformat()
            badges_data.append(badge_dict)
        
        return success_response({
            'badges': badges_data,
            'total': len(badges_data)
        }, 'Student badges retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/points/<course_id>', methods=['GET'])
@require_auth
def get_my_points(course_id):
    """Get current student's points in a course"""
    try:
        student_id = get_current_user()
        
        service = GamificationService(current_app.db)
        points = service.get_student_points(student_id, course_id)
        
        return success_response({'points': points.to_dict()}, 'Points retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/leaderboard/<course_id>', methods=['GET'])
@require_auth
def get_leaderboard(course_id):
    """Get course leaderboard"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        if limit < 1 or limit > 100:
            return error_response('Limit must be between 1 and 100', 400)
        
        service = GamificationService(current_app.db)
        
        # Update leaderboard first
        service.update_leaderboard(course_id)
        
        # Get leaderboard
        leaderboard = service.get_leaderboard(course_id, limit)
        leaderboard_data = [entry.to_dict() for entry in leaderboard]
        
        return success_response({
            'leaderboard': leaderboard_data,
            'total': len(leaderboard_data)
        }, 'Leaderboard retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/leaderboard/<course_id>/my-rank', methods=['GET'])
@require_auth
def get_my_rank(course_id):
    """Get current student's rank on leaderboard"""
    try:
        student_id = get_current_user()
        
        service = GamificationService(current_app.db)
        rank_entry = service.get_student_rank(student_id, course_id)
        
        return success_response({'rank': rank_entry.to_dict()}, 'Student rank retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/streak/<course_id>', methods=['GET'])
@require_auth
def get_my_streak(course_id):
    """Get current student's streak in a course"""
    try:
        student_id = get_current_user()
        
        service = GamificationService(current_app.db)
        streak = service.get_streak(student_id, course_id)
        
        return success_response({'streak': streak.to_dict()}, 'Streak retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)
