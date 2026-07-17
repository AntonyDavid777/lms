from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import config
from app.utils.database import DatabaseConnection, init_indexes
from app.utils.errors import handle_exception
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Application factory function"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}},
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    )
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register error handlers
    handle_exception(app)
    
    # Initialize database connection
    try:
        db = DatabaseConnection.connect(
            app.config['MONGODB_URI'],
            app.config['DATABASE_NAME']
        )
        init_indexes(db)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Store database reference in app
    app.db = db
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix=app.config['API_PREFIX'])
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'TechTots LMS API'}, 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return {
            'service': 'TechTots LMS API',
            'version': app.config['API_VERSION'],
            'docs': f"{app.config['API_PREFIX']}/docs"
        }, 200
    
    logger.info(f"Flask app created with config: {config_name}")
    
    return app
