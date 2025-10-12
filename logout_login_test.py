#!/usr/bin/env python3
"""
CRITICAL TEST: Registration -> Logout -> Login Back In
Testing the exact user scenario:
1. Register new account ✅ (works)
2. Log out ✅ (works) 
3. Try to log back in ❌ (fails with 401)
"""

import requests
import json
import time
import uuid
from datetime import datetime

BACKEND_URL = "https://baby-steps-demo-api.onrender.com"

def test_logout_login_cycle():
    """Test the complete cycle: register -> logout -> login"""
    print("🔄 TESTING COMPLETE LOGOUT/LOGIN CYCLE")
    print("=" * 80)
    
    # Create 3 test users and test the logout/login cycle for each
    test_users = []
    
    for i in range(3):
        print(f"\n👤 USER {i+1}/3 - COMPLETE CYCLE TEST")
        print("-" * 50)
        
        # Generate unique user
        unique_id = str(uuid.uuid4())[:8]
        user_data = {
            "email": f"logouttest_{i}_{unique_id}@test.com",
            "password": "testpass123",
            "name": f"Logout Test User {i+1}"
        }
        
        session = requests.Session()
        
        # Step 1: Register
        print(f"1️⃣ REGISTERING: {user_data['email']}")
        try:
            register_response = session.post(
                f"{BACKEND_URL}/api/auth/register",
                headers={"Content-Type": "application/json"},
                json=user_data,
                timeout=30
            )
            
            print(f"   Registration status: {register_response.status_code}")
            if register_response.status_code in [200, 201]:
                register_data = register_response.json()
                print("   ✅ Registration successful")
                
                # Check if auto-login token is provided
                auto_token = register_data.get("access_token")
                if auto_token:
                    print(f"   📝 Auto-login token received: {auto_token[:20]}...")
                else:
                    print("   📝 No auto-login token (normal for some implementations)")
                
            else:
                print(f"   ❌ Registration failed: {register_response.text}")
                continue
                
        except Exception as e:
            print(f"   ❌ Registration error: {str(e)}")
            continue
        
        # Step 2: Initial Login (to get a token)
        print(f"\n2️⃣ INITIAL LOGIN: {user_data['email']}")
        try:
            login_response = session.post(
                f"{BACKEND_URL}/api/auth/login",
                headers={"Content-Type": "application/json"},
                json={
                    "email": user_data["email"],
                    "password": user_data["password"]
                },
                timeout=30
            )
            
            print(f"   Initial login status: {login_response.status_code}")
            if login_response.status_code == 200:
                login_data = login_response.json()
                token = login_data.get("access_token")
                print(f"   ✅ Initial login successful")
                print(f"   📝 Token received: {token[:20]}...")
                
                # Store user info for later testing
                test_users.append({
                    "email": user_data["email"],
                    "password": user_data["password"],
                    "name": user_data["name"],
                    "token": token
                })
                
            else:
                print(f"   ❌ Initial login failed: {login_response.text}")
                continue
                
        except Exception as e:
            print(f"   ❌ Initial login error: {str(e)}")
            continue
        
        # Step 3: Test protected endpoint with token
        print(f"\n3️⃣ TESTING PROTECTED ENDPOINT ACCESS")
        try:
            babies_response = session.get(
                f"{BACKEND_URL}/api/babies",
                headers={"Authorization": f"Bearer {token}"},
                timeout=30
            )
            
            print(f"   Protected endpoint status: {babies_response.status_code}")
            if babies_response.status_code == 200:
                print("   ✅ Protected endpoint accessible with token")
            else:
                print(f"   ❌ Protected endpoint failed: {babies_response.text}")
                
        except Exception as e:
            print(f"   ❌ Protected endpoint error: {str(e)}")
        
        # Step 4: Simulate logout (clear session/token)
        print(f"\n4️⃣ SIMULATING LOGOUT")
        # In a real app, logout would invalidate the token server-side
        # For this test, we'll just clear our local token and session
        session.headers.clear()
        print("   ✅ Logged out (cleared local session and token)")
        
        # Step 5: CRITICAL TEST - Try to log back in
        print(f"\n5️⃣ CRITICAL TEST: LOGGING BACK IN")
        print("   This is where the user reports 401 errors...")
        
        # Use a fresh session to simulate a new browser/app session
        fresh_session = requests.Session()
        
        try:
            relogin_response = fresh_session.post(
                f"{BACKEND_URL}/api/auth/login",
                headers={"Content-Type": "application/json"},
                json={
                    "email": user_data["email"],
                    "password": user_data["password"]
                },
                timeout=30
            )
            
            print(f"   Re-login status: {relogin_response.status_code}")
            
            if relogin_response.status_code == 200:
                relogin_data = relogin_response.json()
                new_token = relogin_data.get("access_token")
                print("   ✅ RE-LOGIN SUCCESSFUL!")
                print(f"   📝 New token received: {new_token[:20]}...")
                
                # Test protected endpoint with new token
                babies_test = fresh_session.get(
                    f"{BACKEND_URL}/api/babies",
                    headers={"Authorization": f"Bearer {new_token}"},
                    timeout=30
                )
                
                if babies_test.status_code == 200:
                    print("   ✅ Protected endpoint works with new token")
                else:
                    print(f"   ⚠️  Protected endpoint issue: {babies_test.status_code}")
                
            elif relogin_response.status_code == 401:
                print("   ❌ CRITICAL ISSUE CONFIRMED: 401 UNAUTHORIZED")
                print("   🚨 USER'S REPORT IS ACCURATE - Cannot log back in!")
                print(f"   Response: {relogin_response.text}")
                
                # Additional debugging
                print(f"\n   🔍 DEBUGGING INFO:")
                print(f"   - User was just created and logged in successfully")
                print(f"   - Now getting 401 when trying to log back in")
                print(f"   - This confirms database persistence or lookup issues")
                
            else:
                print(f"   ❌ Unexpected re-login failure: {relogin_response.status_code}")
                print(f"   Response: {relogin_response.text}")
                
        except Exception as e:
            print(f"   ❌ Re-login error: {str(e)}")
        
        print(f"\n   📊 USER {i+1} SUMMARY:")
        print(f"   - Registration: ✅")
        print(f"   - Initial Login: ✅") 
        print(f"   - Re-login after logout: {'✅' if relogin_response.status_code == 200 else '❌'}")
        
        time.sleep(2)  # Brief pause between users
    
    return test_users

def test_existing_users_relogin(test_users):
    """Test re-login for all created users after some time"""
    if not test_users:
        print("\n❌ No test users available for re-login testing")
        return
    
    print(f"\n" + "=" * 80)
    print("🔄 TESTING RE-LOGIN FOR ALL CREATED USERS")
    print("=" * 80)
    
    for i, user in enumerate(test_users):
        print(f"\n👤 RE-LOGIN TEST {i+1}/{len(test_users)}: {user['email']}")
        print("-" * 50)
        
        fresh_session = requests.Session()
        
        try:
            relogin_response = fresh_session.post(
                f"{BACKEND_URL}/api/auth/login",
                headers={"Content-Type": "application/json"},
                json={
                    "email": user["email"],
                    "password": user["password"]
                },
                timeout=30
            )
            
            print(f"Status: {relogin_response.status_code}")
            
            if relogin_response.status_code == 200:
                print("✅ Re-login successful")
                token = relogin_response.json().get("access_token")
                print(f"Token: {token[:20]}...")
            elif relogin_response.status_code == 401:
                print("❌ 401 UNAUTHORIZED - User cannot log back in!")
                print(f"Response: {relogin_response.text}")
            else:
                print(f"❌ Unexpected status: {relogin_response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 STARTING LOGOUT/LOGIN CYCLE TESTING")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("\nThis test will:")
    print("1. Register 3 new users")
    print("2. Log each user in initially") 
    print("3. Simulate logout")
    print("4. Try to log back in (where user reports 401 errors)")
    
    # Test the complete cycle
    created_users = test_logout_login_cycle()
    
    # Wait a bit and test re-login again
    print(f"\n⏰ Waiting 10 seconds before final re-login tests...")
    time.sleep(10)
    
    test_existing_users_relogin(created_users)
    
    print("\n" + "=" * 80)
    print("📋 LOGOUT/LOGIN CYCLE TESTING COMPLETE")
    print("=" * 80)