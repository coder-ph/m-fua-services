from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, timedelta

class RatingBaseSchema(Schema):
    """Base schema for rating operations"""
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=False, allow_none=True, validate=validate.Length(max=1000))
    is_anonymous = fields.Bool(load_default=False)


class RatingCreateSchema(RatingBaseSchema):
    """Schema for creating a new rating"""
    service_id = fields.Int(required=True)

    @validates('service_id')
    def validate_service_id(self, value):
        from models.service import Service, ServiceStatus
        service = Service.query.get(value)
        if not service:
            raise ValidationError('Service not found')
        if service.status != ServiceStatus.COMPLETED:
            raise ValidationError('Cannot rate a service that is not completed')


class RatingUpdateSchema(RatingBaseSchema):
    """Schema for updating an existing rating"""
    rating = fields.Int(required=False, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=False, allow_none=True, validate=validate.Length(max=1000))
    is_anonymous = fields.Bool(required=False)


class RatingResponseSchema(Schema):
    """Schema for responding to a rating"""
    response = fields.Str(required=True, validate=validate.Length(min=1, max=1000))


class RatingSchema(RatingBaseSchema):
    """Schema for rating response"""
    id = fields.Int(dump_only=True)
    reviewer_id = fields.Int(dump_only=True)
    provider_id = fields.Int(dump_only=True)
    service_id = fields.Int(dump_only=True)
    provider_response = fields.Str(dump_only=True)
    responded_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested fields
    reviewer = fields.Dict(dump_only=True)  # Will be populated by to_dict()
    provider = fields.Dict(dump_only=True)  # Will be populated by to_dict()
    service = fields.Dict(dump_only=True)   # Will be populated by to_dict()
    
    class Meta:
        fields = (
            'id', 'rating', 'comment', 'is_anonymous', 'reviewer_id', 
            'provider_id', 'service_id', 'provider_response', 'responded_at',
            'created_at', 'updated_at', 'reviewer', 'provider', 'service'
        )
        ordered = True
