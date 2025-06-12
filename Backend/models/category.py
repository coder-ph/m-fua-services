from datetime import datetime
from extensions.extensions import db

class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Self-referential relationship for subcategories
    parent = db.relationship('ServiceCategory', remote_side=[id], backref='subcategories')
    
    # Relationships
    services = db.relationship('Service', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'is_active': self.is_active,
            'parent_id': self.parent_id,
            'has_children': len(self.subcategories) > 0 if self.subcategories else False,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_all_categories(cls, include_inactive=False):
        """Get all categories, optionally including inactive ones"""
        query = cls.query
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.all()
    
    @classmethod
    def get_root_categories(cls, include_inactive=False):
        """Get all root categories (categories without a parent)"""
        query = cls.query.filter_by(parent_id=None)
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.all()
    
    def get_ancestors(self):
        """Get all ancestors of this category"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def get_descendants(self, include_self=False):
        """Get all descendants of this category"""
        descendants = []
        
        def _get_children(category):
            for child in category.subcategories:
                descendants.append(child)
                _get_children(child)
        
        if include_self:
            descendants.append(self)
        
        _get_children(self)
        return descendants
