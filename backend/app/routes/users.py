from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response, paginated_response
from app.utils.auth import require_auth, require_role, get_current_user
from app.services.user_service import UserService
from app.models.user import UserRole
from app.utils.errors import ValidationError, NotFoundError
from bson import ObjectId

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
@require_role(UserRole.ADMIN.value)
def list_users():
    """List all users (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        role = request.args.get('role')
        is_active = request.args.get('is_active', type=lambda x: x.lower() == 'true')
        search = request.args.get('search')
        
        # Validate pagination
        if page < 1:
            return error_response('Page must be >= 1', 400)
        if page_size < 1 or page_size > current_app.config['MAX_PAGE_SIZE']:
            return error_response(f'Page size must be between 1 and {current_app.config["MAX_PAGE_SIZE"]}', 400)
        
        service = UserService(current_app.db)
        
        if search:
            users, total = service.search_users(search, page, page_size)
        else:
            users, total = service.list_users(page, page_size, role, is_active if is_active is not None else None)
        
        users_data = [user.to_dict() for user in users]
        
        return paginated_response(users_data, total, page, page_size, 'Users retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """Get user details"""
    try:
        current_user_id = get_current_user()
        
        # Users can only view their own profile or admins can view anyone
        user_data = g.user_data
        if user_id != current_user_id and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to view this user', 403)
        
        service = UserService(current_app.db)
        user = service.get_user_by_id(user_id)
        
        return success_response({'user': user.to_dict()}, 'User retrieved successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    """Update user information"""
    try:
        current_user_id = get_current_user()
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        # Users can only update their own profile or admins can update anyone
        user_data = g.user_data
        if user_id != current_user_id and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('You do not have permission to update this user', 403)
        
        service = UserService(current_app.db)
        
        # Validate role change (only admins can change roles)
        if 'role' in data and user_data.get('role') != UserRole.ADMIN.value:
            return error_response('Only administrators can change user roles', 403)
        
        updated_user = service.update_user(user_id, **data)
        
        return success_response({'user': updated_user.to_dict()}, 'User updated successfully')
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<user_id>', methods=['DELETE'])
@require_role(UserRole.ADMIN.value)
def delete_user(user_id):
    """Delete (deactivate) user"""
    try:
        service = UserService(current_app.db)
        service.delete_user(user_id)
        
        return success_response(None, 'User deactivated successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<user_id>/change-password', methods=['POST'])
@require_auth
def change_password(user_id):
    """Change user password"""
    try:
        current_user_id = get_current_user()
        
        # Users can only change their own password
        if user_id != current_user_id:
            return error_response('You can only change your own password', 403)
        
        data = request.get_json()
        
        if not data or not all(k in data for k in ['old_password', 'new_password']):
            return error_response('Missing required fields: old_password, new_password', 400)
        
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        # Validate new password
        if len(new_password) < 8:
            return error_response('New password must be at least 8 characters', 400)
        if old_password == new_password:
            return error_response('New password cannot be the same as old password', 400)
        
        service = UserService(current_app.db)
        service.change_password(user_id, old_password, new_password)
        
        return success_response(None, 'Password changed successfully')
    
    except (ValidationError, NotFoundError) as e:
        status_code = 400 if isinstance(e, ValidationError) else 404
        return error_response(str(e), status_code)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<user_id>/deactivate', methods=['POST'])
@require_role(UserRole.ADMIN.value)
def deactivate_user(user_id):
    """Deactivate user account (admin only)"""
    try:
        service = UserService(current_app.db)
        service.deactivate_user(user_id)
        
        return success_response(None, 'User deactivated successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<user_id>/activate', methods=['POST'])
@require_role(UserRole.ADMIN.value)
def activate_user(user_id):
    """Reactivate user account (admin only)"""
    try:
        service = UserService(current_app.db)
        service.activate_user(user_id)
        
        return success_response(None, 'User reactivated successfully')
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/<user_id>/courses', methods=['GET'])
@require_auth
def get_user_courses(user_id):
    """Get all courses enrolled by a user"""
    try:
        current_user_id = get_current_user()
        user_data = g.user_data
        
        # Users can only view their own courses or admins/teachers can view anyone's
        if user_id != current_user_id and user_data.get('role') not in [UserRole.ADMIN.value, UserRole.TEACHER.value]:
            return error_response('You do not have permission to view these courses', 403)
        
        service = UserService(current_app.db)
        courses = service.get_user_courses(user_id)
        
        return success_response({'courses': courses, 'total': len(courses)}, 'User courses retrieved successfully')
    
    except Exception as e:
        return error_response(str(e), 500)
