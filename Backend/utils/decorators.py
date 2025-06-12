from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from models.user import UserRole

def validate_schema(schema_cls):
    """
    Validate request data against a Marshmallow schema.
    Returns 400 with validation errors if validation fails.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            schema = schema_cls()
            errors = schema.validate(data)
            if errors:
                return jsonify({
                    'message': 'Validation error',
                    'errors': errors
                }), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(required_role):
    """
    Require a specific role to access a route.
    Returns 403 if user doesn't have the required role.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') != required_role.name and claims.get('role') != 'ADMIN':
                return jsonify({
                    'message': 'Insufficient permissions'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def provider_required(f):
    """Require the user to be a service provider"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') not in ['PROVIDER', 'ADMIN']:
            return jsonify({
                'message': 'Service provider account required'
            }), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Require the user to be an admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'ADMIN':
            return jsonify({
                'message': 'Admin privileges required'
            }), 403
        return f(*args, **kwargs)
    return decorated_function
