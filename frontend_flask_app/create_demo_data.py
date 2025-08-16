#!/usr/bin/env python3
"""
Script to create demo data within Flask app context
"""
from src.main import app
from src.models.clinic import Clinic
from src.models.user import User
from src.models.user import db

def create_demo_data():
    with app.app_context():
        try:
            # Check if demo clinic already exists
            existing_clinic = Clinic.query.filter_by(name='Demo Clinic').first()
            if existing_clinic:
                print("Demo Clinic already exists")
                clinic = existing_clinic
            else:
                # Create demo clinic
                clinic = Clinic(
                    name='Demo Clinic',
                    is_active=True,
                    subscription_status='active',
                    subscription_plan='basic'
                )
                db.session.add(clinic)
                db.session.commit()
                print(f'✅ Demo Clinic created with ID: {clinic.id}')
            
            # Check if demo user already exists
            existing_user = User.query.filter_by(username='demo', clinic_id=clinic.id).first()
            if existing_user:
                print("Demo user already exists")
            else:
                # Create demo user
                user = User.create_user(
                    clinic_id=clinic.id,
                    username='demo',
                    email='demo@example.com',
                    password='demo',
                    role='admin',
                    first_name='Demo',
                    last_name='User'
                )
                print(f'✅ Demo user created with ID: {user.id}')
            
            print('✅ Demo setup complete!')
            return True
            
        except Exception as e:
            print(f'❌ Error creating demo data: {e}')
            db.session.rollback()
            return False

if __name__ == "__main__":
    create_demo_data()

