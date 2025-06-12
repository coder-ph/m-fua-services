from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models.notification import Notification, NotificationType, NotificationPreference, PushSubscription
from schemas.notification_schema import (
    NotificationSchema, NotificationUpdateSchema,
    NotificationPreferenceSchema, PushNotificationSubscriptionSchema
)
from extensions.extensions import db
from utils.decorators import validate_schema

notification_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notification_bp.route('', methods=['GET'])
@jwt_required()
def list_notifications():
    """Get user's notifications"""
    current_user_id = get_jwt_identity()
    
    # Query parameters
    read = request.args.get('read')
    notification_type = request.args.get('type')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    query = Notification.query.filter_by(user_id=current_user_id)
    
    # Apply filters
    if read is not None:
        query = query.filter(Notification.read == (read.lower() == 'true'))
    if notification_type:
        query = query.filter(Notification.type == NotificationType[notification_type.upper()])
    
    # Pagination
    pagination = query.order_by(Notification.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return {
        'items': [n.to_dict() for n in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page
    }

@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def unread_count():
    """Get count of unread notifications"""
    current_user_id = get_jwt_identity()
    count = Notification.query.filter_by(
        user_id=current_user_id,
        read=False
    ).count()
    return {'unread_count': count}

@notification_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    """Get notification details"""
    current_user_id = get_jwt_identity()
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=current_user_id
    ).first_or_404()
    
    # Mark as read when retrieved
    if not notification.read:
        notification.read = True
        notification.read_at = datetime.utcnow()
        db.session.commit()
    
    return notification.to_dict()

@notification_bp.route('/<int:notification_id>', methods=['PUT'])
@jwt_required()
@validate_schema(NotificationUpdateSchema())
def update_notification(notification_id):
    """Update notification (mark as read/unread)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=current_user_id
    ).first_or_404()
    
    if 'read' in data:
        notification.read = data['read']
        notification.read_at = datetime.utcnow() if data['read'] else None
    
    db.session.commit()
    return notification.to_dict()

@notification_bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_all_read():
    """Mark all notifications as read"""
    current_user_id = get_jwt_identity()
    now = datetime.utcnow()
    
    updated = Notification.query.filter_by(
        user_id=current_user_id,
        read=False
    ).update({
        'read': True,
        'read_at': now
    }, synchronize_session=False)
    
    db.session.commit()
    return {'message': f'Marked {updated} notifications as read'}

@notification_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """Get user's notification preferences"""
    current_user_id = get_jwt_identity()
    preferences = NotificationPreference.query.filter_by(user_id=current_user_id).all()
    return {'preferences': [p.to_dict() for p in preferences]}

@notification_bp.route('/preferences', methods=['PUT'])
@jwt_required()
@validate_schema(NotificationPreferenceSchema())
def update_preferences():
    """Update notification preferences"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Update or create each preference
    for pref_data in data['preferences']:
        pref = NotificationPreference.query.filter_by(
            user_id=current_user_id,
            notification_type=NotificationType[pref_data['notification_type']]
        ).first()
        
        if not pref:
            pref = NotificationPreference(
                user_id=current_user_id,
                notification_type=NotificationType[pref_data['notification_type']]
            )
            db.session.add(pref)
        
        # Update channels
        for channel in ['email', 'push', 'sms']:
            if channel in pref_data:
                setattr(pref, f'receive_{channel}', pref_data[channel])
    
    db.session.commit()
    
    # Return updated preferences
    preferences = NotificationPreference.query.filter_by(user_id=current_user_id).all()
    return {'preferences': [p.to_dict() for p in preferences]}

@notification_bp.route('/push/subscribe', methods=['POST'])
@jwt_required()
@validate_schema(PushNotificationSubscriptionSchema())
def subscribe_push():
    """Subscribe to push notifications"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if subscription already exists
    subscription = PushSubscription.query.filter_by(
        user_id=current_user_id,
        endpoint=data['endpoint']
    ).first()
    
    if not subscription:
        subscription = PushSubscription(
            user_id=current_user_id,
            endpoint=data['endpoint'],
            keys=data['keys'],
            auth_secret=data.get('auth'),
            p256dh_key=data.get('p256dh')
        )
        db.session.add(subscription)
    else:
        # Update existing subscription
        subscription.keys = data['keys']
        if 'auth' in data:
            subscription.auth_secret = data['auth']
        if 'p256dh' in data:
            subscription.p256dh_key = data['p256dh']
    
    db.session.commit()
    return {'message': 'Push subscription updated'}, 200

@notification_bp.route('/push/unsubscribe', methods=['POST'])
@jwt_required()
@validate_schema(PushNotificationSubscriptionSchema(only=('endpoint',)))
def unsubscribe_push():
    """Unsubscribe from push notifications"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Delete the subscription
    deleted = PushSubscription.query.filter_by(
        user_id=current_user_id,
        endpoint=data['endpoint']
    ).delete()
    
    db.session.commit()
    
    if deleted:
        return {'message': 'Push subscription removed'}, 200
    return {'message': 'No subscription found'}, 404
