import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from app import create_app
from models.user import User, UserProfile, UserRole
from models.service import Service, ServiceStatus, ServiceImage, ServiceOffer, ServiceMessage
from models.category import ServiceCategory
from models.rating import Rating
from models.notification import Notification
from extensions.extensions import db

def create_sample_users():
    """Create sample users for testing"""
    # Create admin user
    admin = User(
        email='admin@example.com',
        password=generate_password_hash('admin123'),
        first_name='Admin',
        last_name='User',
        phone='+1234567890',
        role=UserRole.ADMIN,
        is_active=True
    )
    db.session.add(admin)
    
    # Create client users
    client1 = User(
        email='client1@example.com',
        password=generate_password_hash('client123'),
        first_name='John',
        last_name='Doe',
        phone='+1234567891',
        role=UserRole.CLIENT,
        is_active=True
    )
    db.session.add(client1)
    
    client2 = User(
        email='client2@example.com',
        password=generate_password_hash('client123'),
        first_name='Jane',
        last_name='Smith',
        phone='+1234567892',
        role=UserRole.CLIENT,
        is_active=True
    )
    db.session.add(client2)
    
    # Create provider users
    provider1 = User(
        email='provider1@example.com',
        password=generate_password_hash('provider123'),
        first_name='Mike',
        last_name='Johnson',
        phone='+1234567893',
        role=UserRole.PROVIDER,
        is_active=True
    )
    db.session.add(provider1)
    
    provider2 = User(
        email='provider2@example.com',
        password=generate_password_hash('provider123'),
        first_name='Sarah',
        last_name='Williams',
        phone='+1234567894',
        role=UserRole.PROVIDER,
        is_active=True
    )
    db.session.add(provider2)
    
    db.session.commit()
    
    # Create user profiles
    admin_profile = UserProfile(
        user_id=admin.id,
        bio='System Administrator',
        company_name='M-FUA Admin'
    )
    db.session.add(admin_profile)
    
    client1_profile = UserProfile(
        user_id=client1.id,
        bio='Looking for reliable service providers',
        address='123 Main St',
        city='Eldoret',
        country='Kenya'
    )
    db.session.add(client1_profile)
    
    provider1_profile = UserProfile(
        user_id=provider1.id,
        bio='Professional service provider with 5+ years of experience',
        company_name='Mike\'s Services',
        address='456 Service Rd',
        city='Eldoret',
        country='Kenya',
        service_radius=25,
        business_hours={
            'monday': {'open': '08:00', 'close': '17:00'},
            'tuesday': {'open': '08:00', 'close': '17:00'},
            'wednesday': {'open': '08:00', 'close': '17:00'},
            'thursday': {'open': '08:00', 'close': '17:00'},
            'friday': {'open': '08:00', 'close': '17:00'},
            'saturday': {'open': '09:00', 'close': '13:00'},
            'sunday': {'open': None, 'close': None}
        }
    )
    db.session.add(provider1_profile)
    
    db.session.commit()
    
    return {
        'admin': admin,
        'client1': client1,
        'client2': client2,
        'provider1': provider1,
        'provider2': provider2
    }

def create_sample_categories():
    """Create sample service categories"""
    categories = [
        {'name': 'Home Services', 'description': 'Services for your home'},
        {'name': 'Professional Services', 'description': 'Professional and business services'},
        {'name': 'Personal Care', 'description': 'Personal care and wellness services'},
        {'name': 'Events', 'description': 'Event planning and services'},
    ]
    
    subcategories = {
        'Home Services': [
            'Cleaning', 'Plumbing', 'Electrical', 'Carpentry', 'Painting', 'Gardening'
        ],
        'Professional Services': [
            'IT Support', 'Graphic Design', 'Writing & Translation', 'Legal Services', 'Accounting'
        ],
        'Personal Care': [
            'Hair Styling', 'Massage Therapy', 'Personal Training', 'Makeup Artistry'
        ],
        'Events': [
            'Photography', 'Catering', 'Decorations', 'Entertainment'
        ]
    }
    
    created_categories = {}
    
    # Create main categories
    for cat_data in categories:
        category = ServiceCategory(
            name=cat_data['name'],
            description=cat_data['description'],
            is_active=True
        )
        db.session.add(category)
        db.session.flush()  # Get the ID without committing
        created_categories[cat_data['name']] = category
    
    db.session.commit()
    
    # Create subcategories
    for parent_name, subcat_names in subcategories.items():
        parent = created_categories.get(parent_name)
        if parent:
            for subcat_name in subcat_names:
                subcategory = ServiceCategory(
                    name=subcat_name,
                    parent_id=parent.id,
                    is_active=True
                )
                db.session.add(subcategory)
    
    db.session.commit()
    return created_categories

def create_sample_services(users, categories):
    """Create sample services"""
    client = users['client1']
    provider = users['provider1']
    
    # Get some categories
    home_services = categories['Home Services']
    professional_services = categories['Professional Services']
    
    # Create services
    service1 = Service(
        title='House Cleaning Service',
        description='Need a thorough cleaning for my 3-bedroom apartment. Includes living room, kitchen, and bathrooms.',
        status=ServiceStatus.PENDING,
        budget=5000.00,
        deadline=datetime.utcnow() + timedelta(days=7),
        client_id=client.id,
        category_id=ServiceCategory.query.filter_by(name='Cleaning', parent_id=home_services.id).first().id
    )
    db.session.add(service1)
    
    service2 = Service(
        title='Website Development',
        description='Looking for a developer to create a business website with 5 pages and contact form.',
        status=ServiceStatus.ASSIGNED,
        budget=15000.00,
        deadline=datetime.utcnow() + timedelta(days=14),
        client_id=client.id,
        provider_id=provider.id,
        category_id=ServiceCategory.query.filter_by(name='IT Support', parent_id=professional_services.id).first().id,
        assigned_at=datetime.utcnow() - timedelta(days=1)
    )
    db.session.add(service2)
    
    service3 = Service(
        title='Plumbing Repair',
        description='Leaking kitchen faucet needs to be fixed or replaced.',
        status=ServiceStatus.IN_PROGRESS,
        budget=3000.00,
        deadline=datetime.utcnow() + timedelta(days=2),
        client_id=users['client2'].id,
        provider_id=provider.id,
        category_id=ServiceCategory.query.filter_by(name='Plumbing', parent_id=home_services.id).first().id,
        assigned_at=datetime.utcnow() - timedelta(days=2),
        started_at=datetime.utcnow() - timedelta(hours=2)
    )
    db.session.add(service3)
    
    db.session.commit()
    
    # Add some images to services
    image1 = ServiceImage(
        service_id=service1.id,
        image_url='https://example.com/images/cleaning1.jpg',
        is_primary=True
    )
    db.session.add(image1)
    
    # Create some offers
    offer1 = ServiceOffer(
        service_id=service1.id,
        provider_id=provider.id,
        amount=4500.00,
        message='I can do this cleaning job for you. I have 5 years of experience in house cleaning.'
    )
    db.session.add(offer1)
    
    # Create some messages
    message1 = ServiceMessage(
        service_id=service2.id,
        sender_id=provider.id,
        message='Hi! I\'ve started working on your website. Do you have any specific color scheme in mind?',
        is_read=True
    )
    db.session.add(message1)
    
    message2 = ServiceMessage(
        service_id=service2.id,
        sender_id=client.id,
        message='Yes, I was thinking of a blue and white color scheme. What do you think?',
        is_read=True
    )
    db.session.add(message2)
    
    db.session.commit()
    
    return {
        'service1': service1,
        'service2': service2,
        'service3': service3
    }

def create_sample_ratings(users, services):
    """Create sample ratings"""
    client = users['client1']
    provider = users['provider1']
    service = services['service2']
    
    rating = Rating(
        service_id=service.id,
        reviewer_id=client.id,
        provider_id=provider.id,
        rating=5,
        comment='Excellent work! The website looks amazing and was delivered on time.',
        created_at=datetime.utcnow()
    )
    db.session.add(rating)
    db.session.commit()

def seed_database():
    """Main function to seed the database"""
    print("Starting database seeding...")
    
    # Create all database tables
    db.create_all()
    
    # Clear existing data
    print("Clearing existing data...")
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Clear table {table}')
        db.session.execute(table.delete())
    db.session.commit()
    
    # Create sample data
    print("Creating sample users...")
    users = create_sample_users()
    
    print("Creating sample categories...")
    categories = create_sample_categories()
    
    print("Creating sample services...")
    services = create_sample_services(users, categories)
    
    print("Creating sample ratings...")
    create_sample_ratings(users, services)
    
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()
