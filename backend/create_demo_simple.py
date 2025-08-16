#!/usr/bin/env python3
"""
Simple script to create demo clinic and user data directly
"""
import requests
import json

def create_demo_data():
    base_url = "https://zmhqivcvdxyx.manus.space"
    
    # Login as super admin
    login_response = requests.post(f"{base_url}/api/auth/login", json={
        "clinic_name": "Craft AI",
        "username": "craft_admin", 
        "password": "CraftAI2024!"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Super admin login failed: {login_response.text}")
        return False
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Try to create clinic with minimal data
    clinic_data = {
        "name": "Demo Clinic"
    }
    
    print("Creating demo clinic...")
    clinic_response = requests.post(f"{base_url}/api/admin/clinics", json=clinic_data, headers=headers)
    print(f"Clinic creation response: {clinic_response.status_code} - {clinic_response.text}")
    
    # If clinic creation fails, try a different approach - create user directly
    print("\nTrying to create demo user directly...")
    user_data = {
        "username": "demo",
        "email": "demo@example.com", 
        "password": "demo",
        "clinic_name": "Demo Clinic"
    }
    
    user_response = requests.post(f"{base_url}/api/admin/users", json=user_data, headers=headers)
    print(f"User creation response: {user_response.status_code} - {user_response.text}")
    
    # Test login with demo credentials
    print("\nTesting demo login...")
    demo_login = requests.post(f"{base_url}/api/auth/login", json={
        "clinic_name": "Demo Clinic",
        "username": "demo",
        "password": "demo"
    })
    print(f"Demo login response: {demo_login.status_code} - {demo_login.text[:200]}...")
    
    return demo_login.status_code == 200

if __name__ == "__main__":
    create_demo_data()

