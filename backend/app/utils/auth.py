import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, g
from config.config import Config
from app.utils.errors import AuthenticationError, AuthorizationError
import logging

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_tokens(user_id: str, user_data: dict = None):
    """Generate JWT access and refresh tokens"""
    now = datetime.utcnow()
    
    # Access token
    access_token_payload = {
        'user_id': str(user_id),
        'type': 'access',
        'iat': now,
        'exp': now + Config.JWT_ACCESS_TOKEN_EXPIRES,
    }
    if user_data:
        access_token_payload.update(user_data)
    
    access_token = jwt.encode(
        access_token_payload,
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    # Refresh token
    refresh_token_payload = {
        'user_id': str(user_id),
        'type': 'refresh',
        'iat': now,
        'exp': now + Config.JWT_REFRESH_TOKEN_EXPIRES,
    }
    
    refresh_token = jwt.encode(
        refresh_token_payload,
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
    }


def verify_token(token: str, token_type: str = 'access'):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=['HS256']
        )
        
        if payload.get('type') != token_type:
            raise AuthenticationError('Invalid token type')
        
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationError('Invalid token')


def get_token_from_request():
    """Extract JWT token from request headers"""
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header:
        raise AuthenticationError('Missing authorization header')
    
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise AuthenticationError('Invalid authorization scheme')
        return token
    except ValueError:
        raise AuthenticationError('Invalid authorization header format')


def require_auth(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = get_token_from_request()
            payload = verify_token(token, token_type='access')
            g.user_id = payload.get('user_id')
            g.user_data = payload
        except AuthenticationError as e:
            return {'success': False, 'error': str(e)}, 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(*allowed_roles):
    """Decorator to require specific user roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = get_token_from_request()
                payload = verify_token(token, token_type='access')
                g.user_id = payload.get('user_id')
                g.user_data = payload
                
                user_role = payload.get('role')
                if user_role not in allowed_roles:
                    raise AuthorizationError(f'This action requires one of: {", ".join(allowed_roles)}')
                
            except (AuthenticationError, AuthorizationError) as e:
                status_code = 401 if isinstance(e, AuthenticationError) else 403
                return {'success': False, 'error': str(e)}, status_code
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def get_current_user():
    """Get current authenticated user from g object"""
    return getattr(g, 'user_id', None)


def get_user_data():
    """Get current user data from g object"""
    return getattr(g, 'user_data', {})
