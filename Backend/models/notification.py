from datetime import datetime
from enum import Enum
from extensions.extensions import db

class NotificationType(Enum):
    """Types of notifications"""
    # Service related
    SERVICE_REQUESTED = 'service_requested'
    SERVICE_ACCEPTED = 'service_accepted'
    SERVICE_REJECTED = 'service_rejected'
    SERVICE_COMPLETED = 'service_completed'
    SERVICE_CANCELLED = 'service_cancelled'
    
    # Rating related
    NEW_RATING = 'new_rating'
    RATING_RESPONSE = 'rating_response'
    
    # Message related
    NEW_MESSAGE = 'new_message'
    
    # System
    SYSTEM_ALERT = 'system_alert'
    PROMOTION = 'promotion'


class NotificationPreference(db.Model):
    """User's notification preferences"""
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Email preferences
    email_enabled = db.Column(db.Boolean, default=True)
    email_frequency = db.Column(db.String(20), default='immediate')  # immediate, daily, weekly
    
    # Push notification preferences
    push_enabled = db.Column(db.Boolean, default=True)
    
    # Notification type preferences
    service_updates = db.Column(db.Boolean, default=True)
    new_messages = db.Column(db.Boolean, default=True)
    rating_updates = db.Column(db.Boolean, default=True)
    promotions = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notification_preferences', uselist=False))
    
    def to_dict(self):
        return {
            'email_enabled': self.email_enabled,
            'email_frequency': self.email_frequency,
            'push_enabled': self.push_enabled,
            'service_updates': self.service_updates,
            'new_messages': self.new_messages,
            'rating_updates': self.rating_updates,
            'promotions': self.promotions
        }


class Notification(db.Model):
    """User notification"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Notification details
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.Enum(NotificationType), nullable=False)
    
    # Related entity (e.g., service_id, message_id)
    related_entity_type = db.Column(db.String(50))  # e.g., 'service', 'message', 'rating'
    related_entity_id = db.Column(db.Integer)  # ID of the related entity
    
    # Read status
    read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type.value,
            'related_entity_type': self.related_entity_type,
            'related_entity_id': self.related_entity_id,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }


class PushSubscription(db.Model):
    """Push notification subscriptions for web push"""
    __tablename__ = 'push_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Push subscription data (Web Push API)
    endpoint = db.Column(db.Text, nullable=False)
    auth = db.Column(db.String(100), nullable=False)
    p256dh = db.Column(db.String(100), nullable=False)
    
    # Device info
    user_agent = db.Column(db.Text, nullable=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('push_subscriptions', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'endpoint': self.endpoint,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_agent': self.user_agent,
            'is_active': self.is_active
        }
