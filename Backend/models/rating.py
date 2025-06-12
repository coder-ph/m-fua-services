from datetime import datetime
from extensions.extensions import db

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    
    # Response from the provider
    provider_response = db.Column(db.Text, nullable=True)
    responded_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    service = db.relationship('Service', backref=db.backref('ratings', lazy=True))
    
    __table_args__ = (
        db.UniqueConstraint('reviewer_id', 'service_id', name='_reviewer_service_uc'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'reviewer': None if self.is_anonymous else self.reviewer.to_dict(),
            'provider': self.provider.to_dict(),
            'service_id': self.service_id,
            'rating': self.rating,
            'comment': self.comment,
            'is_anonymous': self.is_anonymous,
            'provider_response': self.provider_response,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_average_rating(cls, provider_id):
        """Calculate average rating for a provider"""
        from sqlalchemy import func
        result = db.session.query(
            func.avg(cls.rating).label('average'),
            func.count(cls.id).label('count')
        ).filter_by(provider_id=provider_id).first()
        
        return {
            'average': float(result[0]) if result[0] else 0,
            'count': result[1]
        }
    
    @classmethod
    def get_ratings_summary(cls, provider_id):
        """Get rating distribution (count of each star rating)"""
        from sqlalchemy import func
        
        # Get count for each rating value (1-5)
        distribution = dict(db.session.query(
            cls.rating,
            func.count(cls.id)
        ).filter_by(provider_id=provider_id).group_by(cls.rating).all())
        
        # Ensure all ratings 1-5 are in the result with 0 if no ratings
        rating_summary = {str(i): distribution.get(i, 0) for i in range(1, 6)}
        
        # Add average and total count
        avg_rating = cls.get_average_rating(provider_id)
        rating_summary.update({
            'average': avg_rating['average'],
            'total': avg_rating['count']
        })
        
        return rating_summary
    
    def add_provider_response(self, response_text):
        """Add a response from the provider"""
        self.provider_response = response_text
        self.responded_at = datetime.utcnow()
        return self
