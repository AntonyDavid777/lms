#!/usr/bin/env python
"""
Flask application entry point
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass  # dotenv not available, use environment variables instead

from app.factory import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"Starting TechTots LMS API on {host}:{port}")
    print(f"Documentation available at http://{host}:{port}/api/v1/docs (when Swagger is configured)")
    
    app.run(host=host, port=port, debug=debug)
