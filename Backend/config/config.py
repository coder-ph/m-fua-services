import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # App settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    
    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # CORS
    ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # File uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    
    # Redis (for rate limiting and caching)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    
    # API
    API_PREFIX = '/api/v1'
    
    # Security
    PASSWORD_RESET_EXPIRE_HOURS = 24
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data-dev.sqlite')
    
    # Enable SQL query logging in development
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    # Disable rate limiting in development by default
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'false').lower() == 'true'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'
    WTF_CSRF_ENABLED = False
    
    # Use in-memory SQLite for faster tests
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
    # Disable CSRF tokens in the Forms for testing
    WTF_CSRF_ENABLED = False
    
    # Disable rate limiting in tests
    RATELIMIT_ENABLED = False
    
    # Disable background tasks during testing
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/mfua'
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)
        
        # Log to file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = logging.handlers.RotatingFileHandler(
            'logs/mfua.log', maxBytes=10485760, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('MFUA startup')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
