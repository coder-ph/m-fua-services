from marshmallow import Schema, fields, validate, validates, ValidationError
from models.user import User, UserRole
import re

class LoginSchema(Schema):
    """Schema for user login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    remember_me = fields.Bool(load_default=False)

class RegisterSchema(Schema):
    """Schema for user registration"""
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, 
        load_only=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters long")
    )
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    phone = fields.Str(required=True)
    role = fields.Str(required=True, validate=validate.OneOf([role.value for role in UserRole]))
    
    @validates('phone')
    def validate_phone(self, value):
        """Validate phone number format"""
        # Simple phone number validation - adjust regex as needed
        if not re.match(r'^\+?[1-9]\d{9,14}$', value):
            raise ValidationError("Invalid phone number format. Please use format: +1234567890")

class RefreshTokenSchema(Schema):
    """Schema for token refresh"""
    refresh_token = fields.Str(required=True)

class ForgotPasswordSchema(Schema):
    """Schema for forgot password request"""
    email = fields.Email(required=True)

class ResetPasswordSchema(Schema):
    """Schema for password reset"""
    token = fields.Str(required=True)
    new_password = fields.Str(
        required=True, 
        load_only=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters long")
    )

class ChangePasswordSchema(Schema):
    """Schema for changing password"""
    current_password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(
        required=True, 
        load_only=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters long")
    )

class AuthResponseSchema(Schema):
    """Schema for authentication response"""
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Dict()
    message = fields.Str()

class UserProfileSchema(Schema):
    """Schema for user profile"""
    bio = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)
    profile_picture = fields.Str(allow_none=True)
    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)
    company_name = fields.Str(allow_none=True)
    service_radius = fields.Int(allow_none=True)
    business_hours = fields.Dict(allow_none=True)
    website = fields.Url(allow_none=True)
    facebook = fields.Str(allow_none=True)
    twitter = fields.Str(allow_none=True)
    instagram = fields.Str(allow_none=True)

class UserUpdateSchema(Schema):
    """Schema for updating user information"""
    first_name = fields.Str(validate=validate.Length(min=2, max=50))
    last_name = fields.Str(validate=validate.Length(min=2, max=50))
    phone = fields.Str()
    profile = fields.Nested(UserProfileSchema, allow_none=True)
    
    @validates('phone')
    def validate_phone(self, value):
        if not re.match(r'^\+?[1-9]\d{9,14}$', value):
            raise ValidationError("Invalid phone number format. Please use format: +1234567890")
