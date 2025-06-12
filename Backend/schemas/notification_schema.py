from marshmallow import Schema, fields, validate, ValidationError, validates
from datetime import datetime

class NotificationSchema(Schema):
    """Base schema for notifications"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    message = fields.Str(dump_only=True)
    notification_type = fields.Str(dump_only=True)
    is_read = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Contextual data (varies by notification type)
    data = fields.Dict(dump_only=True)
    
    class Meta:
        fields = ('id', 'user_id', 'title', 'message', 'notification_type', 
                 'is_read', 'created_at', 'data')
        ordered = True


class NotificationListSchema(Schema):
    """Schema for listing notifications with pagination"""
    items = fields.Nested(NotificationSchema, many=True)
    total = fields.Int()
    page = fields.Int()
    per_page = fields.Int()
    total_pages = fields.Int()
    
    class Meta:
        fields = ('items', 'total', 'page', 'per_page', 'total_pages')
        ordered = True


class NotificationUpdateSchema(Schema):
    """Schema for updating notification status"""
    is_read = fields.Bool(required=False)
    
    @validates('is_read')
    def validate_is_read(self, value):
        if value is None:
            raise ValidationError('is_read cannot be null')


class NotificationFilterSchema(Schema):
    """Schema for filtering notifications"""
    is_read = fields.Bool(required=False)
    notification_type = fields.Str(required=False)
    start_date = fields.DateTime(required=False)
    end_date = fields.DateTime(required=False)
    page = fields.Int(validate=validate.Range(min=1), load_default=1)
    per_page = fields.Int(validate=validate.Range(min=1, max=100), load_default=20)
    
    @validates('end_date')
    def validate_date_range(self, value, **kwargs):
        if 'start_date' in self.context and value is not None and self.context['start_date'] is not None:
            if value < self.context['start_date']:
                raise ValidationError('end_date must be after start_date')


class PushNotificationSubscriptionSchema(Schema):
    """Schema for push notification subscription"""
    endpoint = fields.Str(required=True)
    keys = fields.Dict(keys=fields.Str(), values=fields.Str(), required=True)
    
    @validates('keys')
    def validate_keys(self, value):
        required_keys = {'p256dh', 'auth'}
        if not required_keys.issubset(value.keys()):
            raise ValidationError(f'Missing required keys: {required_keys - set(value.keys())}')


class NotificationPreferenceSchema(Schema):
    """Schema for user notification preferences"""
    email_enabled = fields.Bool(load_default=True)
    push_enabled = fields.Bool(load_default=True)
    sms_enabled = fields.Bool(load_default=True)
    
    # Notification type specific preferences
    service_updates = fields.Bool(load_default=True)
    messages = fields.Bool(load_default=True)
    offers = fields.Bool(load_default=True)
    promotions = fields.Bool(load_default=True)
    account_updates = fields.Bool(load_default=True)
    
    # Quiet hours (times when notifications should be silenced)
    quiet_hours_enabled = fields.Bool(load_default=False)
    quiet_hours_start = fields.Time(load_default=None, allow_none=True)
    quiet_hours_end = fields.Time(load_default=None, allow_none=True)
    
    @validates('quiet_hours_start')
    def validate_quiet_hours_start(self, value, **kwargs):
        if self.context.get('quiet_hours_enabled') and value is None:
            raise ValidationError('quiet_hours_start is required when quiet_hours_enabled is true')
    
    @validates('quiet_hours_end')
    def validate_quiet_hours_end(self, value, **kwargs):
        if self.context.get('quiet_hours_enabled') and value is None:
            raise ValidationError('quiet_hours_end is required when quiet_hours_enabled is true')
    
    @validates('quiet_hours_end')
    def validate_quiet_hours_range(self, value, **kwargs):
        if (self.context.get('quiet_hours_enabled') and 
            'quiet_hours_start' in self.context and 
            value is not None and 
            self.context['quiet_hours_start'] is not None):
            
            if value == self.context['quiet_hours_start']:
                raise ValidationError('quiet_hours_end cannot be the same as quiet_hours_start')


class EmailNotificationSchema(Schema):
    """Schema for sending email notifications"""
    to = fields.Email(required=True)
    subject = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    template = fields.Str(required=True)
    context = fields.Dict(load_default=dict)
    
    @validates('template')
    def validate_template(self, value):
        allowed_templates = {
            'welcome', 'password_reset', 'password_changed', 
            'service_assigned', 'service_status_update', 'new_message'
        }
        if value not in allowed_templates:
            raise ValidationError(f'Invalid template. Must be one of: {", ".join(allowed_templates)}')


class SmsNotificationSchema(Schema):
    """Schema for sending SMS notifications"""
    to = fields.Str(required=True, validate=validate.Regexp(r'^\+?[1-9]\d{1,14}$'))
    message = fields.Str(required=True, validate=validate.Length(max=160))
    
    @validates('to')
    def validate_phone(self, value):
        # E.164 format validation
        if not value.startswith('+'):
            raise ValidationError('Phone number must be in E.164 format (e.g., +1234567890)')


class PushNotificationSchema(Schema):
    """Schema for sending push notifications"""
    user_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(max=100))
    body = fields.Str(required=False, validate=validate.Length(max=200))
    data = fields.Dict(required=False)
    icon = fields.Url(required=False)
    badge = fields.Url(required=False)
    actions = fields.List(
        fields.Dict(keys=fields.Str(), values=fields.Str()),
        required=False
    )
    
    @validates('actions')
    def validate_actions(self, value):
        if value and len(value) > 2:
            raise ValidationError('Maximum of 2 actions allowed per notification')


__all__ = [
    'NotificationSchema',
    'NotificationListSchema',
    'NotificationUpdateSchema',
    'NotificationFilterSchema',
    'PushNotificationSubscriptionSchema',
    'NotificationPreferenceSchema',
    'EmailNotificationSchema',
    'SmsNotificationSchema',
    'PushNotificationSchema'
]
