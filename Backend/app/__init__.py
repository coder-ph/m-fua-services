from flask import Flask
from flask_cors import CORS
from config.config import config
from extensions.extensions import db, init_extensions
import os
from .swagger_config import SWAGGER_TEMPLATE

def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register blueprints
    register_blueprints(app)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Add shell context
    @app.shell_context_processor
    def make_shell_context():
        from models.user import User, UserProfile
        from models.service import Service, ServiceStatus, ServiceImage, ServiceOffer, ServiceMessage
        from models.rating import Rating
        from models.category import ServiceCategory
        
        return {
            'db': db,
            'User': User,
            'UserProfile': UserProfile,
            'Service': Service,
            'ServiceStatus': ServiceStatus,
            'ServiceImage': ServiceImage,
            'ServiceOffer': ServiceOffer,
            'ServiceMessage': ServiceMessage,
            'Rating': Rating,
            'ServiceCategory': ServiceCategory
        }
    
    return app

def register_blueprints(app):
    """Register Flask blueprints"""
    # Import blueprints here to avoid circular imports
    from routes.auth_routes import auth_bp
    from routes.service_routes import service_bp
    from routes.category_routes import category_bp
    from routes.rating_routes import rating_bp
    from routes.notification_routes import notification_bp
    from routes.quote_routes import quote_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(service_bp, url_prefix='/api/services')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(rating_bp, url_prefix='/api/ratings')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(quote_bp, url_prefix='/api/quotes')

def register_error_handlers(app):
    """Register error handlers."""
    from werkzeug.exceptions import HTTPException
    from flask import jsonify
    
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """Handle HTTP exceptions."""
        return jsonify({
            'error': {
                'code': error.code,
                'message': error.description,
                'type': error.name
            }
        }), error.code
