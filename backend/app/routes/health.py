from flask import Blueprint

bp = Blueprint('health', __name__, url_prefix='/health')


@bp.route('', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'TechTots LMS API'}, 200
