#!/usr/bin/env python3
"""
Direct database setup for deployed application
"""
import sys
import os
sys.path.insert(0, '/home/ubuntu/craft-ai-backend')

from src.main import app
from src.models.user import User, db
from src.models.clinic import Clinic

def setup_demo_accounts():
    """Setup demo accounts directly in database"""
    with app.app_context():
        try:
            # Check if Demo Clinic exists
            demo_clinic = Clinic.query.filter_by(name='Demo Clinic').first()
            if not demo_clinic:
                # Create Demo Clinic
                demo_clinic = Clinic(
                    name='Demo Clinic',
                    is_active=True,
                    subscription_status='active',
                    subscription_plan='basic'
                )
                db.session.add(demo_clinic)
                db.session.commit()
                print(f"✅ Created Demo Clinic with ID: {demo_clinic.id}")
            else:
                print(f"✅ Demo Clinic already exists with ID: {demo_clinic.id}")
            
            # Check if demo user exists
            demo_user = User.query.filter_by(username='demo', clinic_id=demo_clinic.id).first()
            if not demo_user:
                # Create demo user
                demo_user = User.create_user(
                    clinic_id=demo_clinic.id,
                    username='demo',
                    email='demo@example.com',
                    password='demo',
                    role='admin',
                    first_name='Demo',
                    last_name='User'
                )
                print(f"✅ Created demo user with ID: {demo_user.id}")
            else:
                print(f"✅ Demo user already exists with ID: {demo_user.id}")
            
            # Verify super admin exists
            super_admin = User.query.filter_by(username='craft_admin', role='super_admin').first()
            if super_admin:
                print(f"✅ Super admin exists with ID: {super_admin.id}")
            else:
                print("❌ Super admin not found")
            
            print("\n🎉 Demo accounts setup complete!")
            print("Login credentials:")
            print("  Demo User: Demo Clinic / demo / demo")
            print("  Super Admin: craft_admin / CraftAI2024!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up demo accounts: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    setup_demo_accounts()

