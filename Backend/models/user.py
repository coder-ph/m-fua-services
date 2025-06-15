from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions.extensions import db
from enum import Enum

class UserRole(Enum):
    CLIENT = 'client'
    PROVIDER = 'provider'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CLIENT)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services_posted = db.relationship('Service', backref='client', lazy=True, foreign_keys='Service.client_id')
    services_assigned = db.relationship('Service', backref='provider', lazy=True, foreign_keys='Service.provider_id')
    ratings_given = db.relationship('Rating', backref='reviewer', lazy=True, foreign_keys='Rating.reviewer_id')
    ratings_received = db.relationship('Rating', backref='provider', lazy=True, foreign_keys='Rating.provider_id')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_client(self):
        return self.role == UserRole.CLIENT
    
    def is_provider(self):
        return self.role == UserRole.PROVIDER
    
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # For service providers
    company_name = db.Column(db.String(100), nullable=True)
    business_hours = db.Column(db.JSON, nullable=True)  # Store as {'monday': {'open': '09:00', 'close': '17:00'}, ...}
    service_radius = db.Column(db.Integer, default=10)  # in kilometers
    
    # Social media links
    website = db.Column(db.String(255), nullable=True)
    facebook = db.Column(db.String(255), nullable=True)
    twitter = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bio': self.bio,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'profile_picture': self.profile_picture,
            'company_name': self.company_name,
            'service_radius': self.service_radius,
            'business_hours': self.business_hours,
            'social_media': {
                'website': self.website,
                'facebook': self.facebook,
                'twitter': self.twitter,
                'instagram': self.instagram
            },
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            } if self.latitude and self.longitude else None
        }
