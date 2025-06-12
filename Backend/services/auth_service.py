from flask import current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from sqlalchemy.exc import IntegrityError

from models.user import User, UserProfile, UserRole
from extensions.extensions import db, mail
from utils.email import send_email

class AuthService:
    """Service for handling authentication and user management"""
    
    @staticmethod
    def create_user(email, password, first_name, last_name, phone, role=UserRole.CLIENT, **kwargs):
        """Create a new user"""
        try:
            user = User(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role=role if isinstance(role, UserRole) else UserRole(role)
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Send welcome email
            AuthService._send_welcome_email(user)
            
            return user
            
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating user: {str(e)}")
            raise ValueError("Email or phone number already exists")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error creating user: {str(e)}")
            raise
    
    @staticmethod
    def create_user_profile(profile_data):
        """Create or update user profile"""
        try:
            profile = UserProfile.query.filter_by(user_id=profile_data['user_id']).first()
            
            if profile:
                # Update existing profile
                for key, value in profile_data.items():
                    if hasattr(profile, key):
                        setattr(profile, key, value)
            else:
                # Create new profile
                profile = UserProfile(**profile_data)
                db.session.add(profile)
            
            db.session.commit()
            return profile
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating/updating profile: {str(e)}")
            raise
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate a user with email and password"""
        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            if not user.is_active:
                raise ValueError("Account is deactivated. Please contact support.")
            return user
            
        return None
    
    @staticmethod
    def generate_auth_tokens(user):
        """Generate access and refresh tokens for a user"""
        from flask_jwt_extended import create_access_token, create_refresh_token
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'role': user.role.value,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
    
    @staticmethod
    def initiate_password_reset(email):
        """Initiate password reset process"""
        user = User.query.filter_by(email=email).first()
        if not user:
            # Don't reveal that the email doesn't exist
            return True
            
        # Generate reset token
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        reset_token = serializer.dumps(user.email, salt='password-reset-salt')
        
        # Send password reset email
        reset_url = f"{current_app.config.get('FRONTEND_URL', '')}/reset-password?token={reset_token}"
        
        send_email(
            subject="Password Reset Request",
            recipients=[user.email],
            template='email/reset_password.html',
            user=user,
            reset_url=reset_url
        )
        
        return True
    
    @staticmethod
    def reset_password(token, new_password):
        """Reset user password using token"""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        
        try:
            email = serializer.loads(
                token,
                salt='password-reset-salt',
                max_age=3600  # Token expires in 1 hour
            )
            
            user = User.query.filter_by(email=email).first()
            if not user:
                raise ValueError("Invalid token")
                
            user.password = new_password
            db.session.commit()
            
            # Send confirmation email
            send_email(
                subject="Password Changed Successfully",
                recipients=[user.email],
                template='email/password_changed.html',
                user=user
            )
            
            return True
            
        except SignatureExpired:
            raise ValueError("Password reset token has expired")
        except (BadSignature, Exception) as e:
            current_app.logger.error(f"Password reset error: {str(e)}")
            raise ValueError("Invalid or expired token")
    
    @staticmethod
    def change_password(user, current_password, new_password):
        """Change user password"""
        if not user.verify_password(current_password):
            raise ValueError("Current password is incorrect")
            
        user.password = new_password
        db.session.commit()
        
        # Send notification email
        send_email(
            subject="Your Password Was Changed",
            recipients=[user.email],
            template='email/password_changed.html',
            user=user
        )
        
        return True
    
    @staticmethod
    def _send_welcome_email(user):
        """Send welcome email to new user"""
        send_email(
            subject="Welcome to Laundry & Services Platform",
            recipients=[user.email],
            template='email/welcome.html',
            user=user,
            login_url=f"{current_app.config.get('FRONTEND_URL', '')}/login"
        )
    
    @staticmethod
    def update_user_profile(user_id, profile_data):
        """Update user profile information"""
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
                
            # Update user fields
            if 'first_name' in profile_data:
                user.first_name = profile_data.pop('first_name')
            if 'last_name' in profile_data:
                user.last_name = profile_data.pop('last_name')
            if 'phone' in profile_data:
                user.phone = profile_data.pop('phone')
            
            # Update or create profile
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if profile:
                for key, value in profile_data.items():
                    if hasattr(profile, key):
                        setattr(profile, key, value)
            else:
                profile = UserProfile(user_id=user_id, **profile_data)
                db.session.add(profile)
            
            db.session.commit()
            return user
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating profile: {str(e)}")
            raise
