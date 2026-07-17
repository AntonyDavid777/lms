from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import route modules
from app.routes import health, auth, users, courses, lessons, assessments, progress, gamification, analytics

# Register individual routes
def register_routes():
    """Register all API routes"""
    # Health routes
    api_bp.register_blueprint(health.bp)
    # Auth routes
    api_bp.register_blueprint(auth.bp)
    # User routes
    api_bp.register_blueprint(users.bp)
    # Course routes
    api_bp.register_blueprint(courses.bp)
    # Lesson routes
    api_bp.register_blueprint(lessons.bp)
    # Assessment routes
    api_bp.register_blueprint(assessments.bp)
    # Progress routes
    api_bp.register_blueprint(progress.bp)
    # Gamification routes
    api_bp.register_blueprint(gamification.bp)
    # Analytics routes
    api_bp.register_blueprint(analytics.bp)

# Register routes
register_routes()
