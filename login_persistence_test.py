#!/usr/bin/env python3
"""
CRITICAL: User Registration & Login Persistence Testing - Render Backend
Specific test for the user's reported issue:
- Can create new account (signup works)
- Can log out
- CANNOT log back in (401 error)
- Suggests accounts are NOT being saved to database
"""

import requests
import json
import time
import uuid
from datetime import datetime

BACKEND_URL = "https://baby-steps-demo-api.onrender.com"

def test_user_reported_issue():
    """Test the exact scenario reported by the user"""
    print("🔍 TESTING USER REPORTED ISSUE: Login Persistence Problem")
    print("=" * 80)
    
    session = requests.Session()
    
    # Step 1: Test demo account first (should work if database is initialized)
    print("\n1️⃣ TESTING DEMO ACCOUNT (demo@babysteps.com / demo123)")
    print("This should work if database initialization is correct...")
    
    try:
        demo_response = session.post(
            f"{BACKEND_URL}/api/auth/login",
            headers={"Content-Type": "application/json"},
            json={"email": "demo@babysteps.com", "password": "demo123"},
            timeout=30
        )
        
        print(f"Demo login status: {demo_response.status_code}")
        if demo_response.status_code == 200:
            demo_data = demo_response.json()
            print("✅ Demo account login SUCCESSFUL")
            print(f"Token received: {demo_data.get('access_token', 'None')[:20]}...")
        else:
            print("❌ Demo account login FAILED")
            print(f"Response: {demo_response.text}")
            
    except Exception as e:
        print(f"❌ Demo account error: {str(e)}")
    
    # Step 2: Create a new unique user
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser2025_{unique_id}@test.com"
    test_password = "testpass123"
    test_name = f"Test User 2025 {unique_id}"
    
    print(f"\n2️⃣ CREATING NEW USER: {test_email}")
    
    try:
        register_response = session.post(
            f"{BACKEND_URL}/api/auth/register",
            headers={"Content-Type": "application/json"},
            json={
                "name": test_name,
                "email": test_email,
                "password": test_password
            },
            timeout=30
        )
        
        print(f"Registration status: {register_response.status_code}")
        if register_response.status_code in [200, 201]:
            register_data = register_response.json()
            print("✅ User registration SUCCESSFUL")
            print(f"Response: {json.dumps(register_data, indent=2)}")
        else:
            print("❌ User registration FAILED")
            print(f"Response: {register_response.text}")
            return
            
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return
    
    # Step 3: IMMEDIATE login attempt (critical test)
    print(f"\n3️⃣ IMMEDIATE LOGIN TEST (This is where the issue should appear)")
    print("If database persistence is broken, this will fail with 401...")
    
    time.sleep(2)  # Brief pause to ensure database write completes
    
    try:
        login_response = session.post(
            f"{BACKEND_URL}/api/auth/login",
            headers={"Content-Type": "application/json"},
            json={
                "email": test_email,
                "password": test_password
            },
            timeout=30
        )
        
        print(f"Login status: {login_response.status_code}")
        if login_response.status_code == 200:
            login_data = login_response.json()
            print("✅ IMMEDIATE LOGIN SUCCESSFUL - Database persistence is WORKING!")
            print(f"Token received: {login_data.get('access_token', 'None')[:20]}...")
            
            # Step 4: Test protected endpoint to verify token works
            token = login_data.get('access_token')
            if token:
                print(f"\n4️⃣ TESTING PROTECTED ENDPOINT ACCESS")
                babies_response = session.get(
                    f"{BACKEND_URL}/api/babies",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=30
                )
                
                print(f"Protected endpoint status: {babies_response.status_code}")
                if babies_response.status_code == 200:
                    print("✅ Protected endpoint access SUCCESSFUL")
                    babies_data = babies_response.json()
                    print(f"Found {len(babies_data)} baby profiles")
                else:
                    print("❌ Protected endpoint access FAILED")
                    print(f"Response: {babies_response.text}")
            
        elif login_response.status_code == 401:
            print("❌ CRITICAL ISSUE CONFIRMED: 401 Unauthorized")
            print("🚨 This confirms the user's report - accounts are NOT being saved to database!")
            print(f"Response: {login_response.text}")
            
            # Additional debugging
            print(f"\n🔍 DEBUGGING INFO:")
            print(f"Registration was successful but login failed immediately")
            print(f"This suggests database persistence issues or user lookup problems")
            
        else:
            print(f"❌ Unexpected login failure: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
    
    # Step 5: Try login again after a longer delay
    print(f"\n5️⃣ RETRY LOGIN AFTER DELAY (Testing if it's a timing issue)")
    time.sleep(5)
    
    try:
        retry_response = session.post(
            f"{BACKEND_URL}/api/auth/login",
            headers={"Content-Type": "application/json"},
            json={
                "email": test_email,
                "password": test_password
            },
            timeout=30
        )
        
        print(f"Retry login status: {retry_response.status_code}")
        if retry_response.status_code == 200:
            print("✅ Retry login SUCCESSFUL - May have been a timing issue")
        else:
            print("❌ Retry login also FAILED - Confirms persistence issue")
            print(f"Response: {retry_response.text}")
            
    except Exception as e:
        print(f"❌ Retry login error: {str(e)}")

def test_multiple_users():
    """Test with multiple users to see if it's consistent"""
    print("\n" + "=" * 80)
    print("🔍 TESTING MULTIPLE USERS FOR CONSISTENCY")
    print("=" * 80)
    
    session = requests.Session()
    
    for i in range(3):
        print(f"\n👤 USER {i+1}/3")
        unique_id = str(uuid.uuid4())[:8]
        test_email = f"multitest_{i}_{unique_id}@test.com"
        test_password = "testpass123"
        test_name = f"Multi Test User {i+1}"
        
        # Register
        try:
            register_response = session.post(
                f"{BACKEND_URL}/api/auth/register",
                headers={"Content-Type": "application/json"},
                json={
                    "name": test_name,
                    "email": test_email,
                    "password": test_password
                },
                timeout=30
            )
            
            if register_response.status_code in [200, 201]:
                print(f"✅ User {i+1} registration successful")
                
                # Immediate login
                time.sleep(1)
                login_response = session.post(
                    f"{BACKEND_URL}/api/auth/login",
                    headers={"Content-Type": "application/json"},
                    json={
                        "email": test_email,
                        "password": test_password
                    },
                    timeout=30
                )
                
                if login_response.status_code == 200:
                    print(f"✅ User {i+1} immediate login successful")
                else:
                    print(f"❌ User {i+1} immediate login failed: {login_response.status_code}")
                    
            else:
                print(f"❌ User {i+1} registration failed: {register_response.status_code}")
                
        except Exception as e:
            print(f"❌ User {i+1} error: {str(e)}")

if __name__ == "__main__":
    print("🚀 STARTING LOGIN PERSISTENCE INVESTIGATION")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    test_user_reported_issue()
    test_multiple_users()
    
    print("\n" + "=" * 80)
    print("📋 INVESTIGATION COMPLETE")
    print("=" * 80)