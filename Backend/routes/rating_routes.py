from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_

from models.rating import Rating
from models.service import Service, ServiceStatus
from models.user import UserRole
from schemas.rating_schema import (
    RatingCreateSchema, RatingUpdateSchema, RatingResponseSchema
)
from extensions.extensions import db
from utils.decorators import validate_schema, role_required

rating_bp = Blueprint('ratings', __name__, url_prefix='/api/ratings')

@rating_bp.route('', methods=['POST'])
@jwt_required()
@validate_schema(RatingCreateSchema())
def create_rating():
    """Create a new rating and review"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get the service and verify the user has completed it
    service = Service.query.filter_by(
        id=data['service_id'],
        client_id=current_user_id,
        status=ServiceStatus.COMPLETED
    ).first_or_404()
    
    # Check if rating already exists
    existing_rating = Rating.query.filter_by(
        service_id=service.id,
        reviewer_id=current_user_id
    ).first()
    
    if existing_rating:
        return {'message': 'You have already rated this service'}, 400
    
    # Create the rating
    rating = Rating(
        service_id=service.id,
        provider_id=service.provider_id,
        reviewer_id=current_user_id,
        rating=data['rating'],
        comment=data.get('comment'),
        is_anonymous=data.get('is_anonymous', False)
    )
    
    db.session.add(rating)
    db.session.commit()
    
    return rating.to_dict(), 201

@rating_bp.route('/provider/<int:provider_id>', methods=['GET'])
def get_provider_ratings(provider_id):
    """Get all ratings for a provider"""
    # Check if provider exists and is active
    provider = db.session.query(User).filter_by(
        id=provider_id,
        role=UserRole.PROVIDER,
        is_active=True
    ).first_or_404()
    
    # Get query parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    min_rating = request.args.get('min_rating', type=int)
    
    # Build query
    query = Rating.query.filter_by(provider_id=provider_id)
    
    if min_rating is not None:
        query = query.filter(Rating.rating >= min_rating)
    
    # Paginate results
    pagination = query.order_by(Rating.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get rating summary
    summary = {
        'average_rating': provider.average_rating,
        'total_ratings': provider.rating_count,
        'rating_distribution': provider.rating_distribution
    }
    
    return {
        'summary': summary,
        'ratings': [r.to_dict() for r in pagination.items],
        'pagination': {
            'total': pagination.total,
            'pages': pagination.pages,
            'page': page,
            'per_page': per_page
        }
    }

@rating_bp.route('/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    """Get rating details"""
    rating = Rating.query.get_or_404(rating_id)
    return rating.to_dict()

@rating_bp.route('/<int:rating_id>', methods=['PUT'])
@jwt_required()
@validate_schema(RatingUpdateSchema())
def update_rating(rating_id):
    """Update a rating"""
    current_user_id = get_jwt_identity()
    rating = Rating.query.get_or_404(rating_id)
    
    # Check if the current user is the reviewer
    if rating.reviewer_id != current_user_id:
        return {'message': 'Not authorized to update this rating'}, 403
    
    data = request.get_json()
    
    # Update fields
    if 'rating' in data:
        rating.rating = data['rating']
    if 'comment' in data:
        rating.comment = data['comment']
    if 'is_anonymous' in data:
        rating.is_anonymous = data['is_anonymous']
    
    db.session.commit()
    return rating.to_dict()

@rating_bp.route('/<int:rating_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(rating_id):
    """Delete a rating"""
    current_user_id = get_jwt_identity()
    rating = Rating.query.get_or_404(rating_id)
    
    # Check if the current user is the reviewer or an admin
    if rating.reviewer_id != current_user_id and get_jwt().get('role') != 'ADMIN':
        return {'message': 'Not authorized to delete this rating'}, 403
    
    db.session.delete(rating)
    db.session.commit()
    return {'message': 'Rating deleted successfully'}

@rating_bp.route('/<int:rating_id>/report', methods=['POST'])
@jwt_required()
def report_rating(rating_id):
    """Report an inappropriate rating"""
    current_user_id = get_jwt_identity()
    rating = Rating.query.get_or_404(rating_id)
    
    # Prevent reporting your own rating
    if rating.reviewer_id == current_user_id:
        return {'message': 'Cannot report your own rating'}, 400
    
    # Increment report count
    rating.report_count += 1
    db.session.commit()
    
    # TODO: Notify admin if report count exceeds threshold
    
    return {'message': 'Rating reported successfully'}

@rating_bp.route('/<int:rating_id>/response', methods=['POST'])
@jwt_required()
@role_required(UserRole.PROVIDER)
@validate_schema(RatingResponseSchema())
def respond_to_rating(rating_id):
    """Respond to a rating (provider only)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get the rating
    rating = Rating.query.get_or_404(rating_id)
    
    # Verify the current user is the provider being rated
    if rating.provider_id != current_user_id:
        return {'message': 'Not authorized to respond to this rating'}, 403
    
    # Update the rating with the response
    rating.provider_response = data['response']
    rating.responded_at = db.func.now()
    
    db.session.commit()
    
    return rating.to_dict(), 200

@rating_bp.route('/response/<int:rating_id>', methods=['PUT'])
@jwt_required()
@role_required(UserRole.PROVIDER)
@validate_schema(RatingResponseSchema())
def update_rating_response(rating_id):
    """Update a rating response (provider only)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get the rating
    rating = Rating.query.filter_by(
        id=rating_id,
        provider_id=current_user_id
    ).first_or_404()
    
    # Update the response
    rating.provider_response = data['response']
    rating.responded_at = db.func.now()
    
    db.session.commit()
    
    return rating.to_dict()

@rating_bp.route('/response/<int:rating_id>', methods=['DELETE'])
@jwt_required()
@role_required(UserRole.PROVIDER)
def delete_rating_response(rating_id):
    """Delete a rating response (provider only)"""
    current_user_id = get_jwt_identity()
    
    # Get the rating
    rating = Rating.query.filter_by(
        id=rating_id,
        provider_id=current_user_id
    ).first_or_404()
    
    # Remove the response
    rating.provider_response = None
    rating.responded_at = None
    
    db.session.commit()
    
    return {'message': 'Response deleted successfully'}
