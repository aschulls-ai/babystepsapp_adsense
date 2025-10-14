#!/usr/bin/env python3
"""
USER PROFILE ENDPOINT TESTING
Testing the new user profile endpoints as specified in review request:
1. GET /api/user/profile - Get current user profile
2. PUT /api/user/profile - Update user profile

Test Scenarios:
1. Get User Profile - Login as demo@babysteps.com / demo123 and GET profile
2. Update Name - PUT with name and current_password
3. Update Email - PUT with email and current_password, verify new token
4. Update Password - PUT with current_password and new_password, test old/new login

Backend: https://infant-care-app-2.preview.emergentagent.com
Test Account: demo@babysteps.com / demo123
"""

import requests
import json
import time
from datetime import datetime, timezone
import uuid

class UserProfileTester:
    def __init__(self):
        self.base_url = "https://infant-care-app-2.preview.emergentagent.com"
        self.token = None
        self.test_results = []
        self.total_tests = 8
        self.passed_tests = 0
        self.failed_tests = 0
        self.original_email = "demo@babysteps.com"
        self.original_password = "demo123"
        self.original_name = "Demo User"
        
    def log_test(self, test_name, success, details="", response_time=0):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "response_time": f"{response_time:.2f}s"
        }
        self.test_results.append(result)
        
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
        print(f"{status} - {test_name} ({response_time:.2f}s)")
        if details:
            print(f"    Details: {details}")
    
    def make_request(self, method, endpoint, data=None, headers=None):
        """Make HTTP request with timing"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response_time = time.time() - start_time
            return response, response_time
            
        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            return None, response_time
        except Exception as e:
            response_time = time.time() - start_time
            print(f"Request error: {str(e)}")
            return None, response_time
    
    def get_auth_headers(self):
        """Get authorization headers"""
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}
    
    def test_1_login_demo_account(self):
        """Test 1: Login with Demo Account (demo@babysteps.com / demo123)"""
        data = {
            "email": self.original_email,
            "password": self.original_password
        }
        
        response, response_time = self.make_request("POST", "/api/auth/login", data)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                self.token = result.get("access_token")
                if self.token:
                    self.log_test("1. Login Demo Account", True, 
                                f"JWT token received: {self.token[:20]}...", response_time)
                    return True
                else:
                    self.log_test("1. Login Demo Account", False, 
                                "No access_token in response", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("1. Login Demo Account", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("1. Login Demo Account", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_2_get_user_profile(self):
        """Test 2: GET /api/user/profile - Get current user profile"""
        response, response_time = self.make_request("GET", "/api/user/profile", 
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                profile = response.json()
                expected_fields = ["id", "email", "name"]
                
                # Check if all expected fields are present
                missing_fields = [field for field in expected_fields if field not in profile]
                if missing_fields:
                    self.log_test("2. Get User Profile", False, 
                                f"Missing fields: {missing_fields}", response_time)
                    return False
                
                # Verify demo account details
                if profile["email"] == self.original_email and profile["name"] == self.original_name:
                    self.log_test("2. Get User Profile", True, 
                                f"Profile retrieved: {profile['email']}, {profile['name']}", response_time)
                    return True
                else:
                    self.log_test("2. Get User Profile", False, 
                                f"Unexpected profile data: {profile}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2. Get User Profile", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("2. Get User Profile", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_3_update_name(self):
        """Test 3: PUT /api/user/profile - Update name"""
        new_name = "New Demo Name"
        data = {
            "name": new_name,
            "current_password": self.original_password
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                if result.get("message") and "updated successfully" in result["message"]:
                    # Verify the name was updated by getting profile again
                    profile_response, profile_time = self.make_request("GET", "/api/user/profile", 
                                                                     headers=self.get_auth_headers())
                    
                    if profile_response and profile_response.status_code == 200:
                        profile = profile_response.json()
                        if profile.get("name") == new_name:
                            self.log_test("3. Update Name", True, 
                                        f"Name updated to: {new_name}", response_time + profile_time)
                            return True
                        else:
                            self.log_test("3. Update Name", False, 
                                        f"Name not updated correctly: {profile.get('name')}", response_time + profile_time)
                            return False
                    else:
                        self.log_test("3. Update Name", False, 
                                    "Could not verify name update", response_time)
                        return False
                else:
                    self.log_test("3. Update Name", False, 
                                f"Unexpected response: {result}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("3. Update Name", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("3. Update Name", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_4_update_email(self):
        """Test 4: PUT /api/user/profile - Update email"""
        new_email = "updated@test.com"
        data = {
            "email": new_email,
            "current_password": self.original_password
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                if result.get("message") and "updated successfully" in result["message"]:
                    # Check if new token was provided
                    new_token = result.get("token")
                    if new_token:
                        # Update our token and verify it works
                        old_token = self.token
                        self.token = new_token
                        
                        # Test new token by getting profile
                        profile_response, profile_time = self.make_request("GET", "/api/user/profile", 
                                                                         headers=self.get_auth_headers())
                        
                        if profile_response and profile_response.status_code == 200:
                            profile = profile_response.json()
                            if profile.get("email") == new_email:
                                self.log_test("4. Update Email", True, 
                                            f"Email updated to: {new_email}, new token works", response_time + profile_time)
                                return True
                            else:
                                self.log_test("4. Update Email", False, 
                                            f"Email not updated correctly: {profile.get('email')}", response_time + profile_time)
                                return False
                        else:
                            self.log_test("4. Update Email", False, 
                                        "New token doesn't work", response_time)
                            return False
                    else:
                        self.log_test("4. Update Email", False, 
                                    "No new token provided for email change", response_time)
                        return False
                else:
                    self.log_test("4. Update Email", False, 
                                f"Unexpected response: {result}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4. Update Email", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("4. Update Email", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_5_update_password(self):
        """Test 5: PUT /api/user/profile - Update password"""
        new_password = "newpass456"
        data = {
            "current_password": self.original_password,
            "new_password": new_password
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                if result.get("message") and "updated successfully" in result["message"]:
                    self.log_test("5. Update Password", True, 
                                "Password updated successfully", response_time)
                    # Store new password for next test
                    self.current_password = new_password
                    return True
                else:
                    self.log_test("5. Update Password", False, 
                                f"Unexpected response: {result}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("5. Update Password", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("5. Update Password", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_6_login_old_password_fails(self):
        """Test 6: Try login with old password - should fail"""
        data = {
            "email": "updated@test.com",  # Use updated email
            "password": self.original_password  # Old password
        }
        
        response, response_time = self.make_request("POST", "/api/auth/login", data)
        
        # Should fail with 401
        if response and response.status_code == 401:
            self.log_test("6. Login Old Password Fails", True, 
                        "Old password correctly rejected", response_time)
            return True
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("6. Login Old Password Fails", False, 
                        f"Expected 401, got HTTP {status}", response_time)
            return False
    
    def test_7_login_new_password_works(self):
        """Test 7: Try login with new password - should work"""
        data = {
            "email": "updated@test.com",  # Use updated email
            "password": getattr(self, 'current_password', 'newpass456')  # New password
        }
        
        response, response_time = self.make_request("POST", "/api/auth/login", data)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                new_token = result.get("access_token")
                if new_token:
                    self.log_test("7. Login New Password Works", True, 
                                f"New password login successful: {new_token[:20]}...", response_time)
                    self.token = new_token  # Update token for final test
                    return True
                else:
                    self.log_test("7. Login New Password Works", False, 
                                "No access_token in response", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("7. Login New Password Works", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("7. Login New Password Works", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_8_final_profile_verification(self):
        """Test 8: Final profile verification with all updates"""
        response, response_time = self.make_request("GET", "/api/user/profile", 
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                profile = response.json()
                expected_email = "updated@test.com"
                expected_name = "New Demo Name"
                
                if profile.get("email") == expected_email and profile.get("name") == expected_name:
                    self.log_test("8. Final Profile Verification", True, 
                                f"All updates verified: {profile['email']}, {profile['name']}", response_time)
                    return True
                else:
                    self.log_test("8. Final Profile Verification", False, 
                                f"Profile not as expected: {profile}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("8. Final Profile Verification", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("8. Final Profile Verification", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def run_all_tests(self):
        """Run all user profile tests in sequence"""
        print("🚀 USER PROFILE ENDPOINT TESTING")
        print(f"Backend: {self.base_url}")
        print(f"Test Account: {self.original_email} / {self.original_password}")
        print(f"Total Tests: {self.total_tests}")
        print("=" * 80)
        
        # Test 1: Login
        print("\n📋 PHASE 1: Authentication")
        if not self.test_1_login_demo_account():
            print("❌ Cannot proceed without authentication")
            return self.generate_report()
        
        # Test 2: Get Profile
        print("\n📋 PHASE 2: Get User Profile")
        self.test_2_get_user_profile()
        
        # Test 3: Update Name
        print("\n📋 PHASE 3: Update Name")
        self.test_3_update_name()
        
        # Test 4: Update Email
        print("\n📋 PHASE 4: Update Email")
        self.test_4_update_email()
        
        # Test 5: Update Password
        print("\n📋 PHASE 5: Update Password")
        self.test_5_update_password()
        
        # Test 6: Old Password Fails
        print("\n📋 PHASE 6: Old Password Verification")
        self.test_6_login_old_password_fails()
        
        # Test 7: New Password Works
        print("\n📋 PHASE 7: New Password Verification")
        self.test_7_login_new_password_works()
        
        # Test 8: Final Verification
        print("\n📋 PHASE 8: Final Profile Verification")
        self.test_8_final_profile_verification()
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 USER PROFILE ENDPOINT TEST RESULTS")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Tests Failed: {self.failed_tests}/{self.total_tests}")
        
        # Success Criteria Check
        print("\n🎯 SUCCESS CRITERIA:")
        criteria_met = []
        
        # Check GET /api/user/profile
        get_profile_test = next((r for r in self.test_results if "Get User Profile" in r["test"]), None)
        if get_profile_test and "✅" in get_profile_test["status"]:
            criteria_met.append("✅ GET /api/user/profile working")
        else:
            criteria_met.append("❌ GET /api/user/profile failed")
        
        # Check PUT /api/user/profile for name update
        update_name_test = next((r for r in self.test_results if "Update Name" in r["test"]), None)
        if update_name_test and "✅" in update_name_test["status"]:
            criteria_met.append("✅ PUT /api/user/profile (name update) working")
        else:
            criteria_met.append("❌ PUT /api/user/profile (name update) failed")
        
        # Check PUT /api/user/profile for email update
        update_email_test = next((r for r in self.test_results if "Update Email" in r["test"]), None)
        if update_email_test and "✅" in update_email_test["status"]:
            criteria_met.append("✅ PUT /api/user/profile (email update) working")
        else:
            criteria_met.append("❌ PUT /api/user/profile (email update) failed")
        
        # Check PUT /api/user/profile for password update
        update_password_test = next((r for r in self.test_results if "Update Password" in r["test"]), None)
        if update_password_test and "✅" in update_password_test["status"]:
            criteria_met.append("✅ PUT /api/user/profile (password update) working")
        else:
            criteria_met.append("❌ PUT /api/user/profile (password update) failed")
        
        # Check password verification
        old_password_test = next((r for r in self.test_results if "Old Password Fails" in r["test"]), None)
        new_password_test = next((r for r in self.test_results if "New Password Works" in r["test"]), None)
        if (old_password_test and "✅" in old_password_test["status"] and 
            new_password_test and "✅" in new_password_test["status"]):
            criteria_met.append("✅ Password change verification working")
        else:
            criteria_met.append("❌ Password change verification failed")
        
        for criterion in criteria_met:
            print(criterion)
        
        # Performance Metrics
        response_times = [float(r["response_time"].replace("s", "")) for r in self.test_results if r["response_time"] != "0.00s"]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"Average Response Time: {avg_response_time:.2f}s")
            print(f"Fastest Response: {min(response_times):.2f}s")
            print(f"Slowest Response: {max(response_times):.2f}s")
        
        # Detailed Test Results
        print(f"\n📋 DETAILED TEST RESULTS:")
        for result in self.test_results:
            print(f"{result['status']} - {result['test']} ({result['response_time']})")
            if result['details']:
                print(f"    {result['details']}")
        
        # Final Assessment
        print(f"\n🏆 FINAL ASSESSMENT:")
        if success_rate >= 90:
            print("🎉 EXCELLENT - User profile endpoints are working perfectly")
        elif success_rate >= 75:
            print("✅ GOOD - User profile endpoints are mostly functional with minor issues")
        elif success_rate >= 50:
            print("⚠️ FAIR - User profile endpoints have significant issues requiring attention")
        else:
            print("❌ POOR - User profile endpoints have critical issues preventing normal operation")
        
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success_rate": success_rate,
            "test_results": self.test_results,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0
        }

if __name__ == "__main__":
    tester = UserProfileTester()
    results = tester.run_all_tests()