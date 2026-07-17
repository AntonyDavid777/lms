from flask import Blueprint, request, g, current_app
from app.utils.responses import success_response, error_response
from app.utils.errors import ValidationError, AuthenticationError, NotFoundError, ConflictError
from app.utils.auth import require_auth, get_current_user
from app.models.user import User, UserRole
from bson import ObjectId
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    if not any(c.isupper() for c in password):
        return False, 'Password must contain at least one uppercase letter'
    if not any(c.isdigit() for c in password):
        return False, 'Password must contain at least one digit'
    return True, 'Password is valid'


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['email', 'password', 'name']):
            return error_response('Missing required fields: email, password, name', 400)
        
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        role = data.get('role', UserRole.STUDENT.value)
        
        # Validate email
        if not validate_email(email):
            return error_response('Invalid email format', 400)
        
        # Validate password
        is_valid, msg = validate_password(password)
        if not is_valid:
            return error_response(msg, 400)
        
        # Validate name
        if len(name) < 2:
            return error_response('Name must be at least 2 characters long', 400)
        
        # Check if role is valid
        valid_roles = [r.value for r in UserRole]
        if role not in valid_roles:
            return error_response(f'Invalid role. Must be one of: {", ".join(valid_roles)}', 400)
        
        # Check if email already exists
        db = current_app.db
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            return error_response('Email already registered', 409)
        
        # Create new user
        user = User(
            email=email,
            password=password,
            name=name,
            role=role
        )
        
        # Insert user into database
        result = db.users.insert_one(user.to_dict(include_password=True))
        
        # Generate tokens
        from app.utils.auth import generate_tokens
        tokens = generate_tokens(
            user._id,
            {'role': role, 'email': email, 'name': name}
        )
        
        return success_response({
            'user': user.to_dict(),
            **tokens
        }, 'User registered successfully', 201), 201
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/login', methods=['POST'])
def login():
    """Login user with email and password"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return error_response('Missing required fields: email, password', 400)
        
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        db = current_app.db
        user_doc = db.users.find_one({'email': email})
        
        if not user_doc:
            return error_response('Invalid email or password', 401)
        
        user = User.from_mongo_dict(user_doc)
        
        if not user.verify_password(password):
            return error_response('Invalid email or password', 401)
        
        if not user.is_active:
            return error_response('User account is inactive', 403)
        
        # Generate tokens
        from app.utils.auth import generate_tokens
        tokens = generate_tokens(
            user._id,
            {'role': user.role, 'email': user.email, 'name': user.name}
        )
        
        return success_response({
            'user': user.to_dict(),
            **tokens
        }, 'Login successful')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/me', methods=['GET'])
@require_auth
def get_current_user_info():
    """Get current authenticated user information"""
    try:
        user_id = get_current_user()
        db = current_app.db
        
        user_doc = db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user_doc:
            return error_response('User not found', 404)
        
        user = User.from_mongo_dict(user_doc)
        
        return success_response({
            'user': user.to_dict()
        }, 'User information retrieved')
    
    except Exception as e:
        return error_response(str(e), 500)


@bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    try:
        data = request.get_json()
        
        if not data or 'refresh_token' not in data:
            return error_response('Missing refresh_token', 400)
        
        from app.utils.auth import verify_token, generate_tokens
        
        refresh_token = data.get('refresh_token')
        payload = verify_token(refresh_token, token_type='refresh')
        
        user_id = payload.get('user_id')
        db = current_app.db
        
        user_doc = db.users.find_one({'_id': ObjectId(user_id)})
        if not user_doc:
            return error_response('User not found', 404)
        
        user = User.from_mongo_dict(user_doc)
        
        tokens = generate_tokens(
            user._id,
            {'role': user.role, 'email': user.email, 'name': user.name}
        )
        
        return success_response(tokens, 'Token refreshed successfully')
    
    except Exception as e:
        return error_response(str(e), 500)
