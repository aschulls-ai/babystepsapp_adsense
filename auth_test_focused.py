#!/usr/bin/env python3
"""
Focused Authentication Test for Baby Steps - Email Verification Optional
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://babysteps-app-2.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_auth_flow():
    """Test the complete authentication flow"""
    session = requests.Session()
    session.timeout = 30
    
    print("🚀 Testing Baby Steps Authentication - Email Verification Optional")
    print("=" * 70)
    
    # Test credentials
    new_user_email = "newuser@test.com"
    new_user_password = "TestPass123"
    existing_user_email = "test@babysteps.com"
    existing_user_password = "TestPassword123"
    
    results = []
    
    # 1. Health check
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            results.append("✅ Health Check: API is healthy")
        else:
            results.append(f"❌ Health Check: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Health Check: Error - {str(e)}")
    
    # 2. Register new user
    try:
        user_data = {
            "email": new_user_email,
            "name": "New Test User",
            "password": new_user_password
        }
        response = session.post(f"{API_BASE}/auth/register", json=user_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('email_verified') == False:
                results.append("✅ New User Registration: User registered with email_verified=False")
            else:
                results.append("❌ New User Registration: email_verified should be False")
        elif response.status_code == 400 and "already registered" in response.text:
            results.append("✅ New User Registration: User already exists (acceptable)")
        else:
            results.append(f"❌ New User Registration: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ New User Registration: Error - {str(e)}")
    
    # 3. Login immediately without verification
    try:
        login_data = {
            "email": new_user_email,
            "password": new_user_password
        }
        response = session.post(f"{API_BASE}/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data and data.get('token_type') == 'bearer':
                auth_token = data['access_token']
                session.headers.update({'Authorization': f"Bearer {auth_token}"})
                results.append("✅ Immediate Login: SUCCESS - Can login without email verification")
            else:
                results.append("❌ Immediate Login: Invalid response format")
        else:
            results.append(f"❌ Immediate Login: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Immediate Login: Error - {str(e)}")
    
    # 4. Test protected endpoint access
    try:
        response = session.get(f"{API_BASE}/babies", timeout=10)
        if response.status_code == 200:
            results.append("✅ Protected Endpoints: Can access with token from unverified user")
        else:
            results.append(f"❌ Protected Endpoints: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Protected Endpoints: Error - {str(e)}")
    
    # 5. Test existing user login
    try:
        login_data = {
            "email": existing_user_email,
            "password": existing_user_password
        }
        response = session.post(f"{API_BASE}/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                results.append("✅ Existing User Login: SUCCESS")
            else:
                results.append("❌ Existing User Login: Invalid response")
        else:
            results.append(f"❌ Existing User Login: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Existing User Login: Error - {str(e)}")
    
    # 6. Test email verification still exists
    try:
        email_data = {"email": new_user_email}
        response = session.post(f"{API_BASE}/auth/resend-verification", json=email_data, timeout=10)
        if response.status_code == 200:
            results.append("✅ Email Verification: Functionality still exists")
        else:
            results.append(f"❌ Email Verification: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Email Verification: Error - {str(e)}")
    
    # Print results
    print("\n📊 TEST RESULTS:")
    print("=" * 70)
    for result in results:
        print(result)
    
    # Summary
    failed_tests = [r for r in results if r.startswith("❌")]
    passed_tests = [r for r in results if r.startswith("✅")]
    
    print(f"\n🎯 SUMMARY:")
    print("=" * 70)
    print(f"✅ Passed: {len(passed_tests)}")
    print(f"❌ Failed: {len(failed_tests)}")
    
    if len(failed_tests) == 0:
        print("\n🎉 SUCCESS: Email verification is now optional for login!")
        print("✅ Users can access the app immediately after registration")
        print("✅ Email verification functionality still exists")
        print("✅ All authentication tests passed")
    else:
        print("\n⚠️ Some tests failed:")
        for failed in failed_tests:
            print(f"   {failed}")

if __name__ == "__main__":
    test_auth_flow()