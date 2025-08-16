#!/usr/bin/env python3
"""
Script to set up demo clinic and user data in the deployed database
"""
import requests
import json

# First, try to login as super admin to create demo data
def setup_demo_data():
    base_url = "https://zmhqivcvdxyx.manus.space"
    
    # Try to login as super admin
    login_data = {
        "clinic_name": "Craft AI",
        "username": "craft_admin", 
        "password": "CraftAI2024!"
    }
    
    print("Attempting to login as super admin...")
    response = requests.post(f"{base_url}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        print("✅ Super admin login successful")
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        # Create demo clinic via admin API
        clinic_data = {
            "name": "Demo Clinic",
            "admin_email": "demo@example.com",
            "admin_name": "Demo Admin",
            "subscription_status": "active",
            "subscription_plan": "basic",
            "is_active": True
        }
        
        print("Creating demo clinic...")
        clinic_response = requests.post(f"{base_url}/api/admin/clinics", json=clinic_data, headers=headers)
        
        if clinic_response.status_code == 201:
            clinic_id = clinic_response.json()["clinic"]["id"]
            print(f"✅ Demo clinic created with ID: {clinic_id}")
            
            # Create demo user
            user_data = {
                "clinic_id": clinic_id,
                "username": "demo",
                "email": "demo@example.com",
                "password": "demo",
                "role": "admin",
                "first_name": "Demo",
                "last_name": "User"
            }
            
            print("Creating demo user...")
            user_response = requests.post(f"{base_url}/api/admin/users", json=user_data, headers=headers)
            
            if user_response.status_code == 201:
                print("✅ Demo user created successfully")
                print("Demo setup complete!")
                return True
            else:
                print(f"❌ Failed to create demo user: {user_response.text}")
        else:
            print(f"❌ Failed to create demo clinic: {clinic_response.text}")
    else:
        print(f"❌ Super admin login failed: {response.text}")
    
    return False

if __name__ == "__main__":
    setup_demo_data()

