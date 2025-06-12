#!/usr/bin/env python3
"""
Run the MFUA development server.

This script provides a convenient way to run the development server with
hot-reload enabled. It's not suitable for production use.
"""
import os
import sys
import click
from app import create_app
from extensions.extensions import db, migrate  # Import db and migrate from extensions

# Set the default configuration
debug = os.environ.get('FLASK_DEBUG', '1') != '0'
os.environ['FLASK_ENV'] = 'development' if debug else 'production'

app = create_app()
# Database and migrations are initialized in create_app() via init_extensions()

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    click.echo('Initializing the database...')
    # Create database tables
    db.create_all()
    click.echo('Database initialized.')

@app.cli.command("seed-db")
def seed_db():
    """Seed the database with initial data."""
    from models.user import User
    from models.category import ServiceCategory
    
    click.echo('Seeding the database...')
    
    # Create admin user if not exists
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password=User.hash_password('admin123'),
            role='admin',
            is_active=True,
            is_verified=True
        )
        db.session.add(admin)
        click.echo('Created admin user: admin@example.com / admin123')
    
    # Create some sample categories
    categories = [
        ('Laundry', 'Professional laundry services'),
        ('Dry Cleaning', 'Dry cleaning services for all fabrics'),
        ('Ironing', 'Professional ironing services'),
        ('Home Cleaning', 'Complete home cleaning services'),
        ('Appliance Repair', 'Repair services for home appliances'),
        ('Plumbing', 'Plumbing and pipe repair services'),
        ('Electrical', 'Electrical repair and installation'),
        ('Carpentry', 'Furniture and woodwork services'),
        ('Moving', 'Home and office moving services'),
        ('Gardening', 'Garden maintenance and landscaping')
    ]
    
    for name, description in categories:
        if not ServiceCategory.query.filter_by(name=name).first():
            category = ServiceCategory(name=name, description=description)
            db.session.add(category)
    
    db.session.commit()
    click.echo('Database seeded with initial data.')

if __name__ == '__main__':
    # Run the development server
    app.run(host='0.0.0.0', port=5000, debug=debug)
