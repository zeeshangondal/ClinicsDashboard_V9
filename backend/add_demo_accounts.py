#!/usr/bin/env python3
"""
Script to add demo accounts to the deployed database
"""
import requests
import json

# The deployed application URL
BASE_URL = "https://3dhkilcjwzz5.manus.space"

def create_demo_accounts():
    """Add demo accounts via API calls"""
    
    # First, let's check if we can access the health endpoint
    try:
        health_response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        print(f"Health check: {health_response.status_code}")
        if health_response.status_code == 200:
            print("✅ Backend is accessible")
        else:
            print("❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"❌ Cannot reach backend: {e}")
        return False
    
    # Try to login with super admin to create demo data
    try:
        login_data = {
            "clinic_name": "Craft AI",
            "username": "craft_admin", 
            "password": "CraftAI2024!"
        }
        
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            headers={"Content-Type": "application/json"},
            json=login_data,
            timeout=10
        )
        
        print(f"Super admin login attempt: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        
        if login_response.status_code == 200:
            auth_data = login_response.json()
            access_token = auth_data.get('access_token')
            
            if access_token:
                print("✅ Super admin login successful")
                
                # Now create demo clinic and user via admin API
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                
                # Create demo clinic
                clinic_data = {
                    "name": "Demo Clinic",
                    "subscription_plan": "basic",
                    "admin_email": "demo@example.com",
                    "admin_name": "Demo User",
                    "admin_password": "demo"
                }
                
                clinic_response = requests.post(
                    f"{BASE_URL}/api/admin/clinics",
                    headers=headers,
                    json=clinic_data,
                    timeout=10
                )
                
                print(f"Create clinic response: {clinic_response.status_code}")
                print(f"Clinic response: {clinic_response.text}")
                
                if clinic_response.status_code in [200, 201]:
                    clinic_info = clinic_response.json()
                    clinic_id = clinic_info.get('id')
                    
                    # Create demo user
                    user_data = {
                        "clinic_id": clinic_id,
                        "username": "demo",
                        "email": "demo@example.com",
                        "password": "demo",
                        "role": "admin",
                        "first_name": "Demo",
                        "last_name": "User",
                        "is_active": True
                    }
                    
                    user_response = requests.post(
                        f"{BASE_URL}/api/admin/users",
                        headers=headers,
                        json=user_data,
                        timeout=10
                    )
                    
                    print(f"Create user response: {user_response.status_code}")
                    print(f"User response: {user_response.text}")
                    
                    if user_response.status_code in [200, 201]:
                        print("✅ Demo accounts created successfully!")
                        return True
                    else:
                        print("❌ Failed to create demo user")
                        return False
                else:
                    print("❌ Failed to create demo clinic")
                    return False
            else:
                print("❌ No access token received")
                return False
        else:
            print("❌ Super admin login failed")
            return False
            
    except Exception as e:
        print(f"❌ Error creating demo accounts: {e}")
        return False

if __name__ == "__main__":
    success = create_demo_accounts()
    if success:
        print("\n🎉 Demo accounts are ready!")
        print("You can now login with:")
        print("  Clinic: Demo Clinic")
        print("  Username: demo")
        print("  Password: demo")
    else:
        print("\n❌ Failed to create demo accounts")

