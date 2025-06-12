from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import or_
from datetime import datetime, timedelta

from models.service import Service, ServiceStatus, ServiceImage, ServiceOffer, ServiceMessage
from models.user import UserRole
from schemas.service_schema import (
    ServiceCreateSchema, ServiceUpdateSchema, ServiceFilterSchema,
    ServiceStatusUpdateSchema, ServiceAssignmentSchema, ServiceOfferSchema,
    ServiceMessageSchema
)
from extensions.extensions import db
from utils.decorators import validate_schema, role_required, provider_required, admin_required

service_bp = Blueprint('services', __name__, url_prefix='/api/services')

@service_bp.route('', methods=['POST'])
@jwt_required()
@validate_schema(ServiceCreateSchema())
def create_service():
    """
    Create a new service request
    ---
    tags:
      - Services
    security:
      - Bearer: []
    description: Create a new service request (for clients)
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
            - category_id
            - budget
            - deadline
            - location
          properties:
            title:
              type: string
              example: "House Cleaning"
            description:
              type: string
              example: "Need cleaning for a 3-bedroom house"
            category_id:
              type: integer
              example: 1
            budget:
              type: number
              format: float
              example: 5000
            deadline:
              type: string
              format: date-time
              example: "2025-06-30T18:00:00"
            location:
              type: string
              example: "Nairobi, Kenya"
            latitude:
              type: number
              format: float
              example: -1.2921
            longitude:
              type: number
              format: float
              example: 36.8219
    responses:
      201:
        description: Service created successfully
        schema:
          $ref: '#/definitions/Service'
      400:
        description: Invalid input
        schema:
          $ref: '#/definitions/Error'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Create service
    service = Service(
        title=data['title'],
        description=data['description'],
        category_id=data['category_id'],
        budget=float(data['budget']),
        deadline=datetime.fromisoformat(data['deadline']),
        location=data['location'],
        client_id=current_user_id,
        status=ServiceStatus.PENDING
    )
    
    # Add optional location data
    if 'latitude' in data and 'longitude' in data:
        service.latitude = float(data['latitude'])
        service.longitude = float(data['longitude'])
    
    db.session.add(service)
    db.session.commit()
    
    return service.to_dict(), 201

@service_bp.route('', methods=['GET'])
@jwt_required()
def list_services():
    """
    List services with optional filtering
    ---
    tags:
      - Services
    security:
      - Bearer: []
    description: |
      List services with optional filtering and pagination.
      Clients see their own services, providers see assigned and available services.
    parameters:
      - $ref: '#/parameters/page'
      - $ref: '#/parameters/per_page'
      - name: status
        in: query
        type: string
        enum: [pending, assigned, in_progress, completed, cancelled, rejected, expired]
        description: Filter by service status
      - name: category_id
        in: query
        type: integer
        description: Filter by category ID
    responses:
      200:
        description: List of services
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                $ref: '#/definitions/Service'
            total:
              type: integer
              example: 100
            pages:
              type: integer
              example: 10
            page:
              type: integer
              example: 1
            per_page:
              type: integer
              example: 10
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    # Parse query parameters
    status = request.args.get('status')
    category_id = request.args.get('category_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Base query
    query = Service.query
    
    # Filter by user role
    if claims.get('role') == 'CLIENT':
        query = query.filter(Service.client_id == current_user_id)
    elif claims.get('role') == 'PROVIDER':
        # Providers see their assigned services and available services
        query = query.filter(
            or_(
                Service.provider_id == current_user_id,
                Service.status == ServiceStatus.PENDING
            )
        )
    
    # Apply filters
    if status:
        query = query.filter(Service.status == ServiceStatus[status.upper()])
    if category_id:
        query = query.filter(Service.category_id == category_id)
    
    # Pagination
    pagination = query.order_by(Service.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return {
        'items': [service.to_dict() for service in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page
    }

@service_bp.route('/<int:service_id>', methods=['GET'])
@jwt_required()
def get_service(service_id):
    """
    Get service details
    ---
    tags:
      - Services
    security:
      - Bearer: []
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service to retrieve
    responses:
      200:
        description: Service details
        schema:
          $ref: '#/definitions/Service'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
      403:
        description: Forbidden - Not authorized to view this service
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Service not found
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    service = Service.query.get_or_404(service_id)
    
    # Check permissions
    if claims.get('role') == 'CLIENT' and service.client_id != current_user_id:
        return {'message': 'Not authorized to view this service'}, 403
    if claims.get('role') == 'PROVIDER' and service.provider_id != current_user_id and service.status != ServiceStatus.PENDING:
        return {'message': 'Not authorized to view this service'}, 403
    
    return service.to_dict()

@service_bp.route('/<int:service_id>', methods=['PUT'])
@jwt_required()
@validate_schema(ServiceUpdateSchema())
def update_service(service_id):
    """
    Update service details
    ---
    tags:
      - Services
    security:
      - Bearer: []
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service to update
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Updated Service Title"
            description:
              type: string
              example: "Updated service description"
            budget:
              type: number
              format: float
              example: 6000
            deadline:
              type: string
              format: date-time
              example: "2025-07-15T18:00:00"
            location:
              type: string
              example: "Updated Location, City"
            latitude:
              type: number
              format: float
              example: -1.3000
            longitude:
              type: number
              format: float
              example: 36.8000
    responses:
      200:
        description: Service updated successfully
        schema:
          $ref: '#/definitions/Service'
      400:
        description: Invalid input
        schema:
          $ref: '#/definitions/Error'
      403:
        description: Forbidden - Not authorized to update this service
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Service not found
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    service = Service.query.get_or_404(service_id)
    
    # Only client or admin can update
    if service.client_id != current_user_id and get_jwt().get('role') != 'ADMIN':
        return {'message': 'Not authorized to update this service'}, 403
    
    data = request.get_json()
    
    # Update fields
    for field in ['title', 'description', 'budget', 'deadline', 'location', 'status']:
        if field in data:
            setattr(service, field, data[field])
    
    if 'latitude' in data and 'longitude' in data:
        service.latitude = float(data['latitude'])
        service.longitude = float(data['longitude'])
    
    db.session.commit()
    return service.to_dict()

@service_bp.route('/<int:service_id>/assign', methods=['POST'])
@jwt_required()
@validate_schema(ServiceAssignmentSchema())
@provider_required
def assign_self(service_id):
    """
    Assign self to a service (provider only)
    ---
    tags:
      - Services
    security:
      - Bearer: []
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service to be assigned
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            message:
              type: string
              example: "I've been assigned to this service"
    responses:
      200:
        description: Successfully assigned to service
        schema:
          $ref: '#/definitions/Service'
      400:
        description: Service is not available for assignment
        schema:
          $ref: '#/definitions/Error'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
      403:
        description: Forbidden - Only providers can assign themselves to services
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Service not found
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    
    # Check if service is available
    if service.status != ServiceStatus.PENDING:
        return {'message': 'Service is not available for assignment'}, 400
    
    # Assign provider
    service.provider_id = current_user_id
    service.status = ServiceStatus.ASSIGNED
    service.assigned_at = datetime.utcnow()
    
    # Add assignment message
    message = ServiceMessage(
        service_id=service.id,
        sender_id=current_user_id,
        message=data.get('message', 'I\'ve been assigned to this service')
    )
    
    db.session.add(message)
    db.session.commit()
    
    # TODO: Send notification to client
    
    return service.to_dict()

@service_bp.route('/<int:service_id>/status', methods=['PUT'])
@jwt_required()
@validate_schema(ServiceStatusUpdateSchema())
def update_status(service_id):
    """
    Update service status
    ---
    tags:
      - Services
    security:
      - Bearer: []
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service to update
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum: [pending, assigned, in_progress, completed, cancelled, rejected, expired]
              example: "in_progress"
    responses:
      200:
        description: Service status updated successfully
        schema:
          $ref: '#/definitions/Service'
      400:
        description: Invalid status update
        schema:
          $ref: '#/definitions/Error'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
      403:
        description: Forbidden - Not authorized to update this service
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Service not found
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    
    # Check permissions
    if claims.get('role') == 'CLIENT' and service.client_id != current_user_id:
        return {'message': 'Not authorized to update this service'}, 403
    if claims.get('role') == 'PROVIDER' and service.provider_id != current_user_id:
        return {'message': 'Not authorized to update this service'}, 403
    
    # Update status
    new_status = ServiceStatus[data['status'].upper()]
    service.status = new_status
    
    # Update timestamps
    now = datetime.utcnow()
    if new_status == ServiceStatus.IN_PROGRESS:
        service.started_at = now
    elif new_status == ServiceStatus.COMPLETED:
        service.completed_at = now
    
    # Add status update message
    message = ServiceMessage(
        service_id=service.id,
        sender_id=current_user_id,
        message=f"Status updated to {data['status']}"
    )
    if 'notes' in data:
        message.message += f": {data['notes']}"
    
    db.session.add(message)
    db.session.commit()
    
    # TODO: Send notification to the other party
    
    return service.to_dict()

@service_bp.route('/<int:service_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(service_id):
    """
    Get messages for a service
    ---
    tags:
      - Services
    security:
      - Bearer: []
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service
    responses:
      200:
        description: List of service messages
        schema:
          type: array
          items:
            $ref: '#/definitions/ServiceMessage'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
      403:
        description: Forbidden - Not authorized to view messages for this service
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Service not found
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    service = Service.query.get_or_404(service_id)
    
    # Check permissions
    if service.client_id != current_user_id and service.provider_id != current_user_id and get_jwt().get('role') != 'ADMIN':
        return {'message': 'Not authorized to view these messages'}, 403
    
    messages = ServiceMessage.query.filter_by(service_id=service_id)\
        .order_by(ServiceMessage.created_at.asc())\
        .all()
    
    return {'messages': [msg.to_dict() for msg in messages]}

@service_bp.route('/<int:service_id>/messages', methods=['POST'])
@jwt_required()
@validate_schema(ServiceMessageSchema())
def send_message(service_id):
    """
    Send a message for a service
    ---
    tags:
      - Services
    security:
      - Bearer: []
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - message
          properties:
            message:
              type: string
              example: "Hello, I have a question about this service"
    responses:
      201:
        description: Message sent successfully
        schema:
          $ref: '#/definitions/ServiceMessage'
      400:
        description: Invalid input
        schema:
          $ref: '#/definitions/Error'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
      403:
        description: Forbidden - Not authorized to send messages for this service
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Service not found
        schema:
          $ref: '#/definitions/Error'
    """
    current_user_id = get_jwt_identity()
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    
    # Check permissions - only client, provider, or admin can message
    if service.client_id != current_user_id and service.provider_id != current_user_id and get_jwt().get('role') != 'ADMIN':
        return {'message': 'Not authorized to send messages for this service'}, 403
    
    # Create message
    message = ServiceMessage(
        service_id=service.id,
        sender_id=current_user_id,
        message=data['message']
    )
    
    db.session.add(message)
    db.session.commit()
    
    # TODO: Send notification to the other party
    
    return message.to_dict(), 201
