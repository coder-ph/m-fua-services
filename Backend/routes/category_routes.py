from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError

from models.category import ServiceCategory
from schemas.service_schema import ServiceCategorySchema
from extensions.extensions import db
from utils.decorators import admin_required, validate_schema

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@category_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@validate_schema(ServiceCategorySchema())
def create_category():
    """Create a new service category (admin only)"""
    data = request.get_json()
    
    category = ServiceCategory(
        name=data['name'],
        description=data.get('description'),
        icon=data.get('icon'),
        parent_id=data.get('parent_id')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return category.to_dict(), 201
    except IntegrityError:
        db.session.rollback()
        return {'message': 'Category with this name already exists'}, 400

@category_bp.route('', methods=['GET'])
def list_categories():
    """List all active categories"""
    categories = ServiceCategory.query.filter_by(is_active=True).all()
    return {'categories': [c.to_dict() for c in categories]}

@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get category details"""
    category = ServiceCategory.query.get_or_404(category_id)
    if not category.is_active:
        return {'message': 'Category not found'}, 404
    return category.to_dict()

@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
@validate_schema(ServiceCategorySchema())
def update_category(category_id):
    """Update a category (admin only)"""
    category = ServiceCategory.query.get_or_404(category_id)
    data = request.get_json()
    
    # Update fields
    for field in ['name', 'description', 'icon', 'parent_id']:
        if field in data:
            setattr(category, field, data[field])
    
    try:
        db.session.commit()
        return category.to_dict()
    except IntegrityError:
        db.session.rollback()
        return {'message': 'Category with this name already exists'}, 400

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(category_id):
    """Deactivate a category (admin only)"""
    category = ServiceCategory.query.get_or_404(category_id)
    
    # Check if category has active services
    if category.services.filter_by(is_active=True).count() > 0:
        return {'message': 'Cannot delete category with active services'}, 400
    
    # Soft delete
    category.is_active = False
    db.session.commit()
    
    return {'message': 'Category deactivated successfully'}

@category_bp.route('/<int:category_id>/subcategories', methods=['POST'])
@jwt_required()
@admin_required
@validate_schema(ServiceCategorySchema())
def create_subcategory(category_id):
    """Create a subcategory (admin only)"""
    parent = ServiceCategory.query.get_or_404(category_id)
    data = request.get_json()
    
    subcategory = ServiceCategory(
        name=data['name'],
        description=data.get('description'),
        icon=data.get('icon'),
        parent_id=parent.id
    )
    
    try:
        db.session.add(subcategory)
        db.session.commit()
        return subcategory.to_dict(), 201
    except IntegrityError:
        db.session.rollback()
        return {'message': 'Subcategory with this name already exists'}, 400
