from flask import jsonify
import logging

logger = logging.getLogger(__name__)


class APIException(Exception):
    """Base exception for API errors"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
    
    def to_dict(self):
        rv = {
            'success': False,
            'error': self.message,
            'status_code': self.status_code,
        }
        rv.update(self.payload)
        return rv


class ValidationError(APIException):
    """Validation error"""
    def __init__(self, message, payload=None):
        super().__init__(message, 400, payload)


class AuthenticationError(APIException):
    """Authentication error"""
    def __init__(self, message='Unauthorized'):
        super().__init__(message, 401)


class AuthorizationError(APIException):
    """Authorization error"""
    def __init__(self, message='Forbidden'):
        super().__init__(message, 403)


class NotFoundError(APIException):
    """Resource not found error"""
    def __init__(self, message='Resource not found'):
        super().__init__(message, 404)


class ConflictError(APIException):
    """Conflict error"""
    def __init__(self, message='Resource conflict'):
        super().__init__(message, 409)


class InternalServerError(APIException):
    """Internal server error"""
    def __init__(self, message='Internal server error'):
        super().__init__(message, 500)


def format_error_response(status_code, message, additional_data=None):
    """Format error response"""
    response = {
        'success': False,
        'error': message,
        'status_code': status_code,
    }
    if additional_data:
        response.update(additional_data)
    return jsonify(response), status_code


def handle_exception(app):
    """Register exception handlers with Flask app"""
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = error.to_dict()
        return jsonify(response), error.status_code
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        return format_error_response(400, 'Bad request')
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        return format_error_response(401, 'Unauthorized')
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        return format_error_response(403, 'Forbidden')
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return format_error_response(404, 'Resource not found')
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        logger.error(f"Internal server error: {error}")
        return format_error_response(500, 'Internal server error')
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return format_error_response(500, 'Internal server error')
