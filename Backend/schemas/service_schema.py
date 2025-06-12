from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, timedelta
import re

class ServiceCategorySchema(Schema):
    """Schema for service category"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(required=False, allow_none=True)
    icon = fields.Str(required=False, allow_none=True)
    is_active = fields.Bool(dump_only=True)
    parent_id = fields.Int(required=False, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Include subcategories when serializing
    subcategories = fields.Nested('self', many=True, exclude=('subcategories',))
    
    class Meta:
        fields = ('id', 'name', 'description', 'icon', 'is_active', 'parent_id', 
                 'created_at', 'updated_at', 'subcategories')
        ordered = True


class ServiceImageSchema(Schema):
    """Schema for service images"""
    id = fields.Int(dump_only=True)
    image_url = fields.Str(required=True)
    thumbnail_url = fields.Str(required=False, allow_none=True)
    is_primary = fields.Boolean(load_default=False)
    created_at = fields.DateTime(dump_only=True)
    
    class Meta:
        fields = ('id', 'image_url', 'thumbnail_url', 'is_primary', 'created_at')
        ordered = True


class ServiceOfferSchema(Schema):
    """Schema for service offers"""
    id = fields.Int(dump_only=True)
    provider_id = fields.Int(dump_only=True)
    amount = fields.Decimal(required=True, places=2, as_string=True)
    message = fields.Str(required=False, allow_none=True)
    status = fields.Str(dump_only=True)  # pending, accepted, rejected
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested provider details
    provider = fields.Nested('UserProfileSchema', only=(
        'id', 'first_name', 'last_name', 'company_name', 'profile_picture', 'rating_average'
    ), dump_only=True)
    
    class Meta:
        fields = ('id', 'provider_id', 'amount', 'message', 'status', 
                 'created_at', 'updated_at', 'provider')
        ordered = True


class ServiceMessageSchema(Schema):
    """Schema for service messages"""
    id = fields.Int(dump_only=True)
    message = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    is_read = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Sender information
    sender_id = fields.Int(dump_only=True)
    sender = fields.Nested('UserProfileSchema', only=(
        'id', 'first_name', 'last_name', 'profile_picture', 'company_name'
    ), dump_only=True)
    
    class Meta:
        fields = ('id', 'message', 'is_read', 'created_at', 'sender_id', 'sender')
        ordered = True


class ServiceCreateSchema(Schema):
    """Schema for creating a new service"""
    title = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=10, max=5000))
    category_id = fields.Int(required=True)
    budget = fields.Decimal(required=True, places=2, as_string=True)
    deadline = fields.DateTime(required=True)
    location = fields.Str(required=True)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    
    @validates('budget')
    def validate_budget(self, value):
        if value <= 0:
            raise ValidationError('Budget must be greater than 0')
    
    @validates('deadline')
    def validate_deadline(self, value):
        if value < datetime.utcnow() + timedelta(hours=1):
            raise ValidationError('Deadline must be at least 1 hour from now')


class ServiceUpdateSchema(Schema):
    """Schema for updating a service"""
    title = fields.Str(validate=validate.Length(min=5, max=200), required=False)
    description = fields.Str(validate=validate.Length(min=10, max=5000), required=False)
    status = fields.Str(validate=validate.OneOf([
        'pending', 'assigned', 'in_progress', 'completed', 'cancelled', 'rejected', 'expired'
    ]), required=False)
    budget = fields.Decimal(places=2, as_string=True, required=False)
    deadline = fields.DateTime(required=False)
    location = fields.Str(required=False)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    
    @validates('budget')
    def validate_budget(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Budget must be greater than 0')
    
    @validates('deadline')
    def validate_deadline(self, value):
        if value is not None and value < datetime.utcnow() + timedelta(hours=1):
            raise ValidationError('Deadline must be at least 1 hour from now')


class ServiceSchema(Schema):
    """Schema for service response"""
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    budget = fields.Decimal(as_string=True)
    deadline = fields.DateTime()
    location = fields.Str()
    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    assigned_at = fields.DateTime(allow_none=True)
    started_at = fields.DateTime(allow_none=True)
    completed_at = fields.DateTime(allow_none=True)
    
    # Relationships
    client_id = fields.Int(dump_only=True)
    provider_id = fields.Int(allow_none=True)
    category_id = fields.Int()
    
    # Nested objects
    client = fields.Nested('UserProfileSchema', only=(
        'id', 'first_name', 'last_name', 'profile_picture'
    ), dump_only=True)
    
    provider = fields.Nested('UserProfileSchema', only=(
        'id', 'first_name', 'last_name', 'company_name', 'profile_picture', 'rating_average'
    ), dump_only=True)
    
    category = fields.Nested(ServiceCategorySchema, only=(
        'id', 'name', 'description', 'icon'
    ), dump_only=True)
    
    images = fields.Nested(ServiceImageSchema, many=True, dump_only=True)
    offers = fields.Nested(ServiceOfferSchema, many=True, dump_only=True)
    messages = fields.Nested(ServiceMessageSchema, many=True, dump_only=True)
    
    # Statistics
    messages_count = fields.Int(dump_only=True)
    offers_count = fields.Int(dump_only=True)
    
    class Meta:
        fields = (
            'id', 'title', 'description', 'status', 'budget', 'deadline',
            'location', 'latitude', 'longitude', 'created_at', 'updated_at',
            'assigned_at', 'started_at', 'completed_at', 'client_id', 'provider_id',
            'category_id', 'client', 'provider', 'category', 'images', 'offers',
            'messages', 'messages_count', 'offers_count'
        )
        ordered = True


class ServiceFilterSchema(Schema):
    """Schema for filtering services"""
    status = fields.Str(validate=validate.OneOf([
            'all', 'pending', 'assigned', 'in_progress', 'completed', 'cancelled', 'rejected', 'expired'
        ]), load_default='all')
    category_id = fields.Int(required=False)
    min_budget = fields.Decimal(places=2, as_string=True, required=False)
    max_budget = fields.Decimal(places=2, as_string=True, required=False)
    location = fields.Str(required=False)
    latitude = fields.Float(required=False)
    longitude = fields.Float(required=False)
    radius = fields.Int(required=False)  # in kilometers
    sort_by = fields.Str(validate=validate.OneOf([
            'newest', 'oldest', 'budget_high', 'budget_low', 'deadline_soonest'
        ]), load_default='newest')
    page = fields.Int(validate=validate.Range(min=1), load_default=1)
    per_page = fields.Int(validate=validate.Range(min=1, max=100), load_default=20)
    
    @validates('max_budget')
    def validate_budget_range(self, value, **kwargs):
        if 'min_budget' in self.context and value is not None and self.context['min_budget'] is not None:
            if value < self.context['min_budget']:
                raise ValidationError('max_budget must be greater than or equal to min_budget')
    
    @validates('radius')
    def validate_radius(self, value, **kwargs):
        if value is not None and (value < 1 or value > 100):
            raise ValidationError('Radius must be between 1 and 100 kilometers')


class ServiceAssignmentSchema(Schema):
    """Schema for assigning a provider to a service"""
    provider_id = fields.Int(required=True)
    message = fields.Str(required=False, allow_none=True)


class ServiceStatusUpdateSchema(Schema):
    """Schema for updating service status"""
    status = fields.Str(required=True, validate=validate.OneOf([
        'in_progress', 'completed', 'cancelled', 'rejected'
    ]))
    notes = fields.Str(required=False, allow_none=True)
