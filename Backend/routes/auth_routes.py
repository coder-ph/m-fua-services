from flask import Blueprint, request, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash
from datetime import timedelta

from models.user import User, UserRole
from schemas.auth_schema import (
    RegisterSchema, LoginSchema, RefreshTokenSchema,
    ForgotPasswordSchema, ResetPasswordSchema, ChangePasswordSchema, UserUpdateSchema
)
from services.auth_service import AuthService
from extensions.extensions import db, limiter
from utils.decorators import validate_schema, role_required
from utils.email import send_password_reset_email

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("10 per minute")
@validate_schema(RegisterSchema())
def register():
    """
    Register a new user account
    ---
    tags:
      - Authentication
    description: Create a new user account with the provided details
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/RegisterRequest'
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            refresh_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            user:
              $ref: '#/definitions/User'
      400:
        description: Bad request (e.g., email already registered)
        schema:
          $ref: '#/definitions/Error'
    """
    data = request.get_json()
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return {'message': 'Email already registered'}, 400
    
    # Create new user
    user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        role=UserRole[data['role'].upper()]
    )
    
    # Add optional fields if provided
    for field in ['address', 'city', 'country', 'company_name', 'bio']:
        if field in data:
            setattr(user, field, data[field])
    
    db.session.add(user)
    db.session.commit()
    
    # Generate tokens
    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }, 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
@validate_schema(LoginSchema())
def login():
    """
    User login
    ---
    tags:
      - Authentication
    description: Authenticate user and get access and refresh tokens
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
              example: user@example.com
            password:
              type: string
              format: password
              example: SecurePass123!
    responses:
      200:
        description: Successfully logged in
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            refresh_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            user:
              $ref: '#/definitions/User'
      401:
        description: Invalid credentials
        schema:
          $ref: '#/definitions/Error'
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return {'message': 'Invalid credentials'}, 401
    
    if not user.is_active:
        return {'message': 'Account is deactivated'}, 403
    
    # Create tokens
    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    description: Get a new access token using a valid refresh token
    responses:
      200:
        description: New access token generated
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      401:
        description: Invalid or expired refresh token
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id, fresh=False)
    return {'access_token': new_token}

@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit("5 per hour")
@validate_schema(ForgotPasswordSchema())
def forgot_password():
    """
    Request password reset
    ---
    tags:
      - Authentication
    description: Request a password reset link to be sent to the user's email
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              format: email
              example: user@example.com
    responses:
      200:
        description: If the email is registered, a reset link will be sent
        schema:
          type: object
          properties:
            message:
              type: string
              example: "If your email is registered, you will receive a password reset link"
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user:
        reset_token = AuthService.generate_reset_token(user.id)
        send_password_reset_email(user, reset_token)
    
    # Always return success to prevent email enumeration
    return {'message': 'If your email is registered, you will receive a password reset link'}

@auth_bp.route('/reset-password', methods=['POST'])
@validate_schema(ResetPasswordSchema())
def reset_password():
    """
    Reset password
    ---
    tags:
      - Authentication
    description: Reset user password using a valid reset token
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - token
            - new_password
          properties:
            token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            new_password:
              type: string
              format: password
              minLength: 8
              example: "NewSecurePass123!"
    responses:
      200:
        description: Password successfully reset
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Password has been reset successfully"
      400:
        description: Invalid or expired token
        schema:
          $ref: '#/definitions/Error'
      404:
        description: User not found
        schema:
          $ref: '#/definitions/Error'
    """
    data = request.get_json()
    user_id = AuthService.verify_reset_token(data['token'])
    
    if not user_id:
        return {'message': 'Invalid or expired token'}, 400
    
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found'}, 404
    
    user.set_password(data['new_password'])
    db.session.commit()
    
    return {'message': 'Password has been reset successfully'}

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@validate_schema(ChangePasswordSchema())
def change_password():
    """
    Change password
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    description: Change the current user's password
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - current_password
            - new_password
          properties:
            current_password:
              type: string
              format: password
              example: "OldSecurePass123!"
            new_password:
              type: string
              format: password
              minLength: 8
              example: "NewSecurePass123!"
    responses:
      200:
        description: Password successfully changed
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Password has been changed successfully"
      400:
        description: Current password is incorrect
        schema:
          $ref: '#/definitions/Error'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    user = User.query.get(current_user_id)
    if not user.check_password(data['current_password']):
        return {'message': 'Current password is incorrect'}, 400
    
    user.set_password(data['new_password'])
    db.session.commit()
    
    return {'message': 'Password updated successfully'}

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    description: Get the current user's profile information
    responses:
      200:
        description: User profile information
        schema:
          $ref: '#/definitions/User'
    """
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    return user.to_dict()

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
@validate_schema(UserUpdateSchema())
def update_profile():
    """
    Update current user profile
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    description: Update the current user's profile information
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
              example: "John"
            last_name:
              type: string
              example: "Doe"
            phone:
              type: string
              example: "+1234567890"
            address:
              type: string
              example: "123 Main St"
            city:
              type: string
              example: "New York"
            country:
              type: string
              example: "USA"
            company_name:
              type: string
              example: "ACME Corp"
            bio:
              type: string
              example: "A short bio about the user"
    responses:
      200:
        description: User profile updated successfully
        schema:
          $ref: '#/definitions/User'
    """
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    data = request.get_json()
    
    # Update user fields
    for field in ['first_name', 'last_name', 'phone', 'address', 
                 'city', 'country', 'company_name', 'bio']:
        if field in data:
            setattr(user, field, data[field])
    
    db.session.commit()
    return user.to_dict()

@auth_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@role_required(UserRole.ADMIN)
def list_users():
    """
    List all users (admin only)
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    description: Get a list of all users (only accessible by admins)
    responses:
      200:
        description: List of users
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                $ref: '#/definitions/User'
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}

@auth_bp.route('/admin/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
@role_required(UserRole.ADMIN)
def toggle_user_status(user_id):
    """
    Toggle user active status (admin only)
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    description: Toggle the active status of a user (only accessible by admins)
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
          example: 1
    responses:
      200:
        description: User status updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User activated/deactivated successfully"
    """
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return {'message': f"User {'activated' if user.is_active else 'deactivated'} successfully"}
