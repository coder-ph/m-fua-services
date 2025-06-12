from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from celery import Celery
from flasgger import Swagger, LazyString, LazyJSONEncoder
import logging
import json

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
migrate = Migrate()
celery = Celery()

# Initialize Swagger with default config
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/",
    "swagger": "2.0"  # Explicitly set Swagger version
}

# Import the template after defining the config
from app.swagger_config import SWAGGER_TEMPLATE

# Initialize Swagger with the template
swagger = Swagger(template=SWAGGER_TEMPLATE, config=swagger_config)

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def init_extensions(app):
    """Initialize all Flask extensions"""
    # Set the custom JSON encoder for Swagger
    app.json_encoder = LazyJSONEncoder
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config.get('CELERY_CONFIG', {}))
    
    # Configure Swagger
    app.config['SWAGGER'] = {
        'title': 'M-FUA Services Platform API',
        'uiversion': 3,
        'specs': swagger_config['specs'],
        'static_url_path': swagger_config['static_url_path'],
        'specs_route': swagger_config['specs_route']
    }
    
    # Initialize Swagger with the app
    swagger.init_app(app)
    
    # Initialize rate limiter
    limiter.init_app(app)
    
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    
    # Configure JWT error handlers
    @jwt.unauthorized_loader
    def handle_unauthorized_error(error):
        return {'message': 'Missing or invalid token'}, 401
    
    @jwt.invalid_token_loader
    def handle_invalid_token_error(error):
        return {'message': 'Invalid token'}, 401
    
    @jwt.expired_token_loader
    def handle_expired_token_error(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 401
    
    @jwt.revoked_token_loader
    def handle_revoked_token_error():
        return {'message': 'Token has been revoked'}, 401
    
    # Try to import tasks if the module exists
    try:
        # Try absolute import first
        from tasks import tasks  # noqa
        logging.info("Successfully imported Celery tasks")
    except ImportError:
        try:
            # Fallback to relative import
            from ..tasks import tasks  # noqa
            logging.info("Successfully imported Celery tasks using relative import")
        except ImportError as e:
            logging.warning(f"Could not import tasks: {str(e)}. Running without Celery tasks.")
    except Exception as e:
        logging.error(f"Error importing tasks: {str(e)}. Running without Celery tasks.")
    
    return app
