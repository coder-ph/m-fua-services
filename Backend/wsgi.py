"""
WSGI config for MFUA project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from app import create_app

# Set the default configuration if not set
os.environ.setdefault('FLASK_ENV', 'production')

# Create the Flask application
application = create_app()

if __name__ == "__main__":
    # This is only used when running the application directly
    # In production, a WSGI server like Gunicorn will be used
    application.run(host='0.0.0.0', port=5000)
