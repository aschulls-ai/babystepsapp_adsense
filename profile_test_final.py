#!/usr/bin/env python3
"""
FINAL USER PROFILE ENDPOINT TEST
Testing with a fresh test user account
"""

import requests
import json
import time

def test_user_profile_complete():
    base_url = "https://babysteps-tracker.preview.emergentagent.com"
    
    print("🚀 COMPREHENSIVE USER PROFILE ENDPOINT TEST")
    print("=" * 60)
    
    # Test credentials
    test_email = "profiletest@example.com"
    test_password = "testpass123"
    test_name = "Profile Test User"
    
    # Step 1: Register new user
    print("1. Registering new test user...")
    register_data = {
        "email": test_email,
        "name": test_name,
        "password": test_password
    }
    response = requests.post(f"{base_url}/api/auth/register", json=register_data)
    
    if response.status_code == 200:
        print("✅ Registration successful")
        
        # Step 2: Login
        print("2. Testing login...")
        login_data = {"email": test_email, "password": test_password}
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login successful")
            
            # Step 3: GET /api/user/profile
            print("3. Testing GET /api/user/profile...")
            response = requests.get(f"{base_url}/api/user/profile", headers=headers)
            
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ GET profile successful")
                print(f"   Profile: ID={profile.get('id')}, Email={profile.get('email')}, Name={profile.get('name')}")
                
                # Verify expected fields
                expected_fields = ["id", "email", "name"]
                missing_fields = [field for field in expected_fields if field not in profile]
                if missing_fields:
                    print(f"❌ Missing fields: {missing_fields}")
                    return False
                
                if profile.get("email") != test_email or profile.get("name") != test_name:
                    print(f"❌ Profile data mismatch")
                    return False
                
                # Step 4: PUT /api/user/profile - Update Name
                print("4. Testing PUT /api/user/profile (name update)...")
                new_name = "Updated Test Name"
                update_data = {
                    "name": new_name,
                    "current_password": test_password
                }
                response = requests.put(f"{base_url}/api/user/profile", json=update_data, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Name update successful: {result.get('message')}")
                    
                    # Verify name update
                    response = requests.get(f"{base_url}/api/user/profile", headers=headers)
                    if response.status_code == 200:
                        updated_profile = response.json()
                        if updated_profile.get("name") == new_name:
                            print("✅ Name update verified")
                        else:
                            print(f"❌ Name not updated correctly: {updated_profile.get('name')}")
                            return False
                    
                    # Step 5: PUT /api/user/profile - Update Email
                    print("5. Testing PUT /api/user/profile (email update)...")
                    new_email = "updated.profile@example.com"
                    update_data = {
                        "email": new_email,
                        "current_password": test_password
                    }
                    response = requests.put(f"{base_url}/api/user/profile", json=update_data, headers=headers)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ Email update successful: {result.get('message')}")
                        
                        # Check if new token was provided
                        new_token = result.get("token")
                        if new_token:
                            print("✅ New token provided for email change")
                            headers = {"Authorization": f"Bearer {new_token}"}
                            
                            # Verify email update with new token
                            response = requests.get(f"{base_url}/api/user/profile", headers=headers)
                            if response.status_code == 200:
                                updated_profile = response.json()
                                if updated_profile.get("email") == new_email:
                                    print("✅ Email update verified")
                                else:
                                    print(f"❌ Email not updated correctly: {updated_profile.get('email')}")
                                    return False
                            
                            # Step 6: PUT /api/user/profile - Update Password
                            print("6. Testing PUT /api/user/profile (password update)...")
                            new_password = "newpassword456"
                            update_data = {
                                "current_password": test_password,
                                "new_password": new_password
                            }
                            response = requests.put(f"{base_url}/api/user/profile", json=update_data, headers=headers)
                            
                            if response.status_code == 200:
                                result = response.json()
                                print(f"✅ Password update successful: {result.get('message')}")
                                
                                # Step 7: Test old password fails
                                print("7. Testing old password rejection...")
                                login_data = {"email": new_email, "password": test_password}
                                response = requests.post(f"{base_url}/api/auth/login", json=login_data)
                                
                                if response.status_code == 401:
                                    print("✅ Old password correctly rejected")
                                else:
                                    print(f"❌ Old password should be rejected, got HTTP {response.status_code}")
                                
                                # Step 8: Test new password works
                                print("8. Testing new password login...")
                                login_data = {"email": new_email, "password": new_password}
                                response = requests.post(f"{base_url}/api/auth/login", json=login_data)
                                
                                if response.status_code == 200:
                                    final_token = response.json().get("access_token")
                                    print("✅ New password login successful")
                                    
                                    # Step 9: Final verification
                                    print("9. Final profile verification...")
                                    headers = {"Authorization": f"Bearer {final_token}"}
                                    response = requests.get(f"{base_url}/api/user/profile", headers=headers)
                                    
                                    if response.status_code == 200:
                                        final_profile = response.json()
                                        if (final_profile.get("email") == new_email and 
                                            final_profile.get("name") == new_name):
                                            print("✅ Final verification successful")
                                            print(f"   Final Profile: Email={final_profile.get('email')}, Name={final_profile.get('name')}")
                                            
                                            print("\n🎉 ALL USER PROFILE ENDPOINT TESTS PASSED!")
                                            print("✅ GET /api/user/profile - Working")
                                            print("✅ PUT /api/user/profile (name) - Working")
                                            print("✅ PUT /api/user/profile (email) - Working")
                                            print("✅ PUT /api/user/profile (password) - Working")
                                            print("✅ Password verification - Working")
                                            return True
                                        else:
                                            print(f"❌ Final profile verification failed: {final_profile}")
                                    else:
                                        print(f"❌ Final profile check failed: HTTP {response.status_code}")
                                else:
                                    print(f"❌ New password login failed: HTTP {response.status_code}")
                            else:
                                print(f"❌ Password update failed: HTTP {response.status_code}")
                                print(f"Response: {response.text}")
                        else:
                            print("❌ No new token provided for email change")
                    else:
                        print(f"❌ Email update failed: HTTP {response.status_code}")
                        print(f"Response: {response.text}")
                else:
                    print(f"❌ Name update failed: HTTP {response.status_code}")
                    print(f"Response: {response.text}")
            else:
                print(f"❌ GET profile failed: HTTP {response.status_code}")
                print(f"Response: {response.text}")
        else:
            print(f"❌ Login failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
    else:
        print(f"❌ Registration failed: HTTP {response.status_code}")
        print(f"Response: {response.text}")
    
    return False

if __name__ == "__main__":
    success = test_user_profile_complete()
    if not success:
        print("\n❌ SOME TESTS FAILED - Check the output above for details")
        exit(1)
    else:
        print("\n✅ ALL TESTS PASSED SUCCESSFULLY")