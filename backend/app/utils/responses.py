from flask import jsonify
from datetime import datetime
import json


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects"""
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def success_response(data=None, message='Success', status_code=200):
    """Format success response"""
    response = {
        'success': True,
        'message': message,
        'status_code': status_code,
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def paginated_response(items, total, page, page_size, message='Success', status_code=200):
    """Format paginated response"""
    response = {
        'success': True,
        'message': message,
        'status_code': status_code,
        'data': items,
        'pagination': {
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size,
        }
    }
    return jsonify(response), status_code


def error_response(message, status_code=400, errors=None):
    """Format error response"""
    response = {
        'success': False,
        'error': message,
        'status_code': status_code,
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code
