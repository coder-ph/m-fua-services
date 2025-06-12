from datetime import datetime
from enum import Enum
from extensions.extensions import db

class ServiceStatus(Enum):
    PENDING = 'pending'      # Service posted, waiting for provider
    ASSIGNED = 'assigned'    # Provider assigned, work not started
    IN_PROGRESS = 'in_progress'  # Provider has started the work
    COMPLETED = 'completed'  # Service completed successfully
    CANCELLED = 'cancelled'  # Service was cancelled
    REJECTED = 'rejected'    # Service was rejected by provider
    EXPIRED = 'expired'      # Service expired without assignment

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(ServiceStatus), default=ServiceStatus.PENDING, nullable=False)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Relationships
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_at = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    images = db.relationship('ServiceImage', backref='service', lazy=True, cascade='all, delete-orphan')
    offers = db.relationship('ServiceOffer', backref='service', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('ServiceMessage', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_details=False):
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'budget': float(self.budget) if self.budget else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'location': self.location,
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            } if self.latitude and self.longitude else None,
            'client': self.client.to_dict() if self.client else None,
            'provider': self.provider.to_dict() if self.provider else None,
            'category': self.category.to_dict() if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_details:
            result.update({
                'images': [img.to_dict() for img in self.images],
                'offers': [offer.to_dict() for offer in self.offers],
                'messages': [msg.to_dict() for msg in self.messages],
                'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
                'started_at': self.started_at.isoformat() if self.started_at else None,
                'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            })
        
        return result
    
    def assign_provider(self, provider_id):
        """Assign a provider to this service"""
        if self.status != ServiceStatus.PENDING:
            raise ValueError("Only pending services can be assigned")
            
        self.provider_id = provider_id
        self.status = ServiceStatus.ASSIGNED
        self.assigned_at = datetime.utcnow()
    
    def start_service(self):
        """Mark service as in progress"""
        if self.status != ServiceStatus.ASSIGNED:
            raise ValueError("Only assigned services can be started")
            
        self.status = ServiceStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()
    
    def complete_service(self):
        """Mark service as completed"""
        if self.status != ServiceStatus.IN_PROGRESS:
            raise ValueError("Only in-progress services can be completed")
            
        self.status = ServiceStatus.COMPLETED
        self.completed_at = datetime.utcnow()
    
    def cancel_service(self, reason=None):
        """Cancel the service"""
        if self.status in [ServiceStatus.COMPLETED, ServiceStatus.CANCELLED, ServiceStatus.REJECTED, ServiceStatus.EXPIRED]:
            raise ValueError(f"Cannot cancel service in {self.status} state")
            
        self.status = ServiceStatus.CANCELLED
        self.updated_at = datetime.utcnow()
    
    def reject_service(self, reason=None):
        """Reject the service (by provider)"""
        if self.status != ServiceStatus.ASSIGNED:
            raise ValueError("Only assigned services can be rejected")
            
        self.status = ServiceStatus.REJECTED
        prev_provider = self.provider_id
        self.provider_id = None
        self.updated_at = datetime.utcnow()
        return prev_provider  # Return the previous provider ID for notifications
    
    def expire_service(self):
        """Mark service as expired"""
        if self.status != ServiceStatus.PENDING:
            raise ValueError("Only pending services can be expired")
            
        self.status = ServiceStatus.EXPIRED
        self.updated_at = datetime.utcnow()


class ServiceImage(db.Model):
    __tablename__ = 'service_images'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'thumbnail_url': self.thumbnail_url,
            'is_primary': self.is_primary,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ServiceOffer(db.Model):
    __tablename__ = 'service_offers'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    provider = db.relationship('User', backref='offers')
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'provider': self.provider.to_dict() if self.provider else None,
            'amount': float(self.amount) if self.amount else None,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ServiceMessage(db.Model):
    __tablename__ = 'service_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', backref='messages_sent')
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'sender': self.sender.to_dict() if self.sender else None,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
