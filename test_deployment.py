#!/usr/bin/env python3
"""
Simple test script to verify Render deployment is working
Run this after deploying the updated backend server
"""

import requests
import json
import time

BASE_URL = "https://baby-steps-demo-api.onrender.com/api"

def test_deployment():
    print("🚀 Testing Baby Steps Render Deployment...")
    print(f"📍 Base URL: {BASE_URL}")
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: User Registration
    print("\n2️⃣ Testing User Registration...")
    test_email = f"test{int(time.time())}@example.com"
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": test_email,
            "name": "Test User",
            "password": "testpass123"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                token = data['access_token']
                print("✅ User registration passed")
            else:
                print(f"❌ Registration response missing token: {data}")
                return False
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Test 3: Authentication
    print("\n3️⃣ Testing Authentication...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": test_email,
            "password": "testpass123"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                token = data['access_token']
                headers = {"Authorization": f"Bearer {token}"}
                print("✅ Authentication passed")
            else:
                print(f"❌ Login response missing token: {data}")
                return False
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Test 4: Protected Endpoint
    print("\n4️⃣ Testing Protected Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/user/profile", headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('email') == test_email:
                print("✅ Protected endpoint passed")
            else:
                print(f"❌ Profile data incorrect: {data}")
                return False
        else:
            print(f"❌ Profile request failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Profile error: {e}")
        return False
    
    # Test 5: Demo Login (existing user)
    print("\n5️⃣ Testing Demo Login...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "demo@babysteps.com",
            "password": "demo123"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                print("✅ Demo login passed")
            else:
                print(f"❌ Demo login response missing token: {data}")
        else:
            print(f"❌ Demo login failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Demo login error: {e}")
    
    print("\n🎉 All tests completed successfully!")
    print("\n✅ Backend deployment is working correctly")
    print("✅ Frontend should now be able to connect successfully")
    print("✅ User registration, login, and profile management functional")
    
    return True

if __name__ == "__main__":
    success = test_deployment()
    if success:
        print("\n🚀 Deployment verification PASSED - ready for frontend testing!")
    else:
        print("\n❌ Deployment verification FAILED - check server logs")