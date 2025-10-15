#!/usr/bin/env python3
"""
QUICK USER PROFILE VERIFICATION TEST
Verify the user profile endpoints are working correctly
"""

import requests
import json

def test_user_profile_endpoints():
    base_url = "https://growithbaby.preview.emergentagent.com"
    
    print("🔍 QUICK USER PROFILE ENDPOINT VERIFICATION")
    print("=" * 50)
    
    # Step 1: Login
    print("1. Testing login...")
    login_data = {"email": "demo@babysteps.com", "password": "demo123"}
    response = requests.post(f"{base_url}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login successful")
        
        # Step 2: Get Profile
        print("2. Testing GET /api/user/profile...")
        response = requests.get(f"{base_url}/api/user/profile", headers=headers)
        
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ GET profile successful: {profile}")
            
            # Step 3: Update Name
            print("3. Testing PUT /api/user/profile (name update)...")
            update_data = {
                "name": "Test Updated Name",
                "current_password": "demo123"
            }
            response = requests.put(f"{base_url}/api/user/profile", json=update_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Name update successful: {result.get('message')}")
                
                # Verify name update
                response = requests.get(f"{base_url}/api/user/profile", headers=headers)
                if response.status_code == 200:
                    updated_profile = response.json()
                    if updated_profile.get("name") == "Test Updated Name":
                        print("✅ Name update verified")
                    else:
                        print(f"❌ Name not updated correctly: {updated_profile.get('name')}")
                
            else:
                print(f"❌ Name update failed: HTTP {response.status_code}")
                print(f"Response: {response.text}")
        else:
            print(f"❌ GET profile failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
    else:
        print(f"❌ Login failed: HTTP {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_user_profile_endpoints()