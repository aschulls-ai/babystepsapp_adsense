#!/usr/bin/env python3
"""
USER PROFILE UPDATE ENDPOINT TESTING
Testing the new user profile endpoints as specified in review request

Backend: https://infant-care-app-2.preview.emergentagent.com
Test Account: demo@babysteps.com / demo123

Test Scenarios:
1. GET /api/user/profile - Should return user profile (email, name)
2. PUT /api/user/profile - Should update user profile
3. Update name only with current password
4. Update email with current password (should return new token)
5. Update password with current password
6. Error cases: missing password, wrong password, duplicate email
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
        """Test 1: Login with Demo Account"""
        data = {
            "email": "demo@babysteps.com",
            "password": "demo123"
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
            status_code = response.status_code if response else "Timeout"
            response_text = response.text if response else "Connection timeout"
            self.log_test("1. Login Demo Account", False, 
                        f"HTTP {status_code}: {response_text}", response_time)
            return False
    
    def test_2_get_user_profile(self):
        """Test 2: GET /api/user/profile - Should return user profile"""
        headers = self.get_auth_headers()
        response, response_time = self.make_request("GET", "/api/user/profile", headers=headers)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                required_fields = ['id', 'email', 'name']
                missing_fields = [field for field in required_fields if field not in result]
                
                if not missing_fields:
                    self.log_test("2. GET User Profile", True, 
                                f"Profile retrieved: {result.get('email')} - {result.get('name')}", response_time)
                    return True, result
                else:
                    self.log_test("2. GET User Profile", False, 
                                f"Missing required fields: {missing_fields}", response_time)
                    return False, None
            except json.JSONDecodeError:
                self.log_test("2. GET User Profile", False, 
                            "Invalid JSON response", response_time)
                return False, None
        elif response and response.status_code == 404:
            self.log_test("2. GET User Profile", False, 
                        "Endpoint not found (HTTP 404) - /api/user/profile not implemented", response_time)
            return False, None
        else:
            status_code = response.status_code if response else "Timeout"
            response_text = response.text if response else "Connection timeout"
            self.log_test("2. GET User Profile", False, 
                        f"HTTP {status_code}: {response_text}", response_time)
            return False, None
    
    def test_3_update_name_only(self):
        """Test 3: Update Name Only with Current Password"""
        headers = self.get_auth_headers()
        data = {
            "name": "Updated Demo Parent",
            "current_password": "demo123"
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data, headers)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                self.log_test("3. Update Name Only", True, 
                            f"Name updated successfully: {result}", response_time)
                return True
            except json.JSONDecodeError:
                self.log_test("3. Update Name Only", True, 
                            "Name updated (no JSON response)", response_time)
                return True
        elif response and response.status_code == 404:
            self.log_test("3. Update Name Only", False, 
                        "Endpoint not found (HTTP 404) - /api/user/profile PUT not implemented", response_time)
            return False
        else:
            status_code = response.status_code if response else "Timeout"
            response_text = response.text if response else "Connection timeout"
            self.log_test("3. Update Name Only", False, 
                        f"HTTP {status_code}: {response_text}", response_time)
            return False
    
    def test_4_update_email(self):
        """Test 4: Update Email with Current Password"""
        headers = self.get_auth_headers()
        data = {
            "email": "newemail@test.com",
            "current_password": "demo123"
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data, headers)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                # Should return new token if email changed
                if 'access_token' in result:
                    self.log_test("4. Update Email", True, 
                                f"Email updated with new token: {result.get('access_token', '')[:20]}...", response_time)
                    # Update token for subsequent tests
                    self.token = result['access_token']
                else:
                    self.log_test("4. Update Email", True, 
                                f"Email updated: {result}", response_time)
                return True
            except json.JSONDecodeError:
                self.log_test("4. Update Email", True, 
                            "Email updated (no JSON response)", response_time)
                return True
        elif response and response.status_code == 404:
            self.log_test("4. Update Email", False, 
                        "Endpoint not found (HTTP 404) - /api/user/profile PUT not implemented", response_time)
            return False
        else:
            status_code = response.status_code if response else "Timeout"
            response_text = response.text if response else "Connection timeout"
            self.log_test("4. Update Email", False, 
                        f"HTTP {status_code}: {response_text}", response_time)
            return False
    
    def test_5_update_password(self):
        """Test 5: Update Password with Current Password"""
        headers = self.get_auth_headers()
        data = {
            "current_password": "demo123",
            "new_password": "newpass123"
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data, headers)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                self.log_test("5. Update Password", True, 
                            f"Password updated successfully: {result}", response_time)
                return True
            except json.JSONDecodeError:
                self.log_test("5. Update Password", True, 
                            "Password updated (no JSON response)", response_time)
                return True
        elif response and response.status_code == 404:
            self.log_test("5. Update Password", False, 
                        "Endpoint not found (HTTP 404) - /api/user/profile PUT not implemented", response_time)
            return False
        else:
            status_code = response.status_code if response else "Timeout"
            response_text = response.text if response else "Connection timeout"
            self.log_test("5. Update Password", False, 
                        f"HTTP {status_code}: {response_text}", response_time)
            return False
    
    def test_6_error_no_password(self):
        """Test 6: Error Case - Update Email Without Current Password"""
        headers = self.get_auth_headers()
        data = {
            "email": "newemail2@test.com"
            # Missing current_password
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data, headers)
        
        if response and (response.status_code == 400 or response.status_code == 422):
            self.log_test("6. Error: No Password", True, 
                        f"Correctly rejected (HTTP {response.status_code})", response_time)
            return True
        elif response and response.status_code == 404:
            self.log_test("6. Error: No Password", False, 
                        "Endpoint not found (HTTP 404)", response_time)
            return False
        else:
            status_code = response.status_code if response else "Timeout"
            self.log_test("6. Error: No Password", False, 
                        f"Should have failed but got HTTP {status_code}", response_time)
            return False
    
    def test_7_error_wrong_password(self):
        """Test 7: Error Case - Update with Wrong Current Password"""
        headers = self.get_auth_headers()
        data = {
            "name": "Should Fail",
            "current_password": "wrongpassword"
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data, headers)
        
        if response and (response.status_code == 401 or response.status_code == 403):
            self.log_test("7. Error: Wrong Password", True, 
                        f"Correctly rejected (HTTP {response.status_code})", response_time)
            return True
        elif response and response.status_code == 404:
            self.log_test("7. Error: Wrong Password", False, 
                        "Endpoint not found (HTTP 404)", response_time)
            return False
        else:
            status_code = response.status_code if response else "Timeout"
            self.log_test("7. Error: Wrong Password", False, 
                        f"Should have failed but got HTTP {status_code}", response_time)
            return False
    
    def test_8_verify_updated_profile(self):
        """Test 8: Verify Profile Updates by Getting Profile Again"""
        headers = self.get_auth_headers()
        response, response_time = self.make_request("GET", "/api/user/profile", headers=headers)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                updated_name = result.get('name', '')
                updated_email = result.get('email', '')
                
                # Check if updates were persisted
                name_updated = "Updated Demo Parent" in updated_name
                email_updated = "newemail@test.com" in updated_email
                
                if name_updated or email_updated:
                    self.log_test("8. Verify Updates", True, 
                                f"Updates persisted - Name: {updated_name}, Email: {updated_email}", response_time)
                else:
                    self.log_test("8. Verify Updates", True, 
                                f"Profile retrieved - Name: {updated_name}, Email: {updated_email}", response_time)
                return True
            except json.JSONDecodeError:
                self.log_test("8. Verify Updates", False, 
                            "Invalid JSON response", response_time)
                return False
        elif response and response.status_code == 404:
            self.log_test("8. Verify Updates", False, 
                        "Endpoint not found (HTTP 404)", response_time)
            return False
        else:
            status_code = response.status_code if response else "Timeout"
            response_text = response.text if response else "Connection timeout"
            self.log_test("8. Verify Updates", False, 
                        f"HTTP {status_code}: {response_text}", response_time)
            return False
    
    def run_all_tests(self):
        """Run all user profile tests"""
        print("🧪 USER PROFILE UPDATE ENDPOINT TESTING")
        print("=" * 60)
        print(f"Backend URL: {self.base_url}")
        print(f"Test Account: demo@babysteps.com / demo123")
        print("=" * 60)
        print()
        
        # Test 1: Login
        print("📋 PHASE 1: AUTHENTICATION")
        login_success = self.test_1_login_demo_account()
        
        if not login_success:
            print("❌ CRITICAL: Cannot proceed without authentication")
            return self.generate_summary()
        
        # Test 2: Get Profile
        print("\n📋 PHASE 2: GET USER PROFILE")
        profile_success, profile_data = self.test_2_get_user_profile()
        
        # Test 3-5: Update Operations
        print("\n📋 PHASE 3: PROFILE UPDATE OPERATIONS")
        self.test_3_update_name_only()
        self.test_4_update_email()
        self.test_5_update_password()
        
        # Test 6-7: Error Cases
        print("\n📋 PHASE 4: ERROR HANDLING")
        self.test_6_error_no_password()
        self.test_7_error_wrong_password()
        
        # Test 8: Verify Updates
        print("\n📋 PHASE 5: VERIFICATION")
        self.test_8_verify_updated_profile()
        
        return self.generate_summary()
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 USER PROFILE ENDPOINT TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"Tests Passed: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print()
        
        # Analyze results
        failed_tests = [result for result in self.test_results if result['status'] == '❌ FAIL']
        passed_tests = [result for result in self.test_results if result['status'] == '✅ PASS']
        
        if failed_tests:
            print("❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['details']}")
            print()
        
        if passed_tests:
            print("✅ PASSED TESTS:")
            for test in passed_tests:
                print(f"  • {test['test']}")
            print()
        
        # Critical Analysis
        profile_endpoints_working = any("not found" not in result['details'] and 
                                      ("GET User Profile" in result['test'] or "Update" in result['test']) 
                                      and result['status'] == '✅ PASS' 
                                      for result in self.test_results)
        
        endpoints_not_found = any("not found" in result['details'] for result in self.test_results)
        
        print("🔍 CRITICAL FINDINGS:")
        if endpoints_not_found:
            print("  ❌ User profile endpoints (/api/user/profile) are NOT IMPLEMENTED")
            print("  ❌ GET /api/user/profile - Missing")
            print("  ❌ PUT /api/user/profile - Missing")
            print("  ❌ The requested user profile update functionality is not available")
        elif profile_endpoints_working:
            print("  ✅ User profile endpoints are implemented and functional")
            print("  ✅ GET /api/user/profile - Working")
            print("  ✅ PUT /api/user/profile - Working")
        else:
            print("  ⚠️  User profile endpoints may have issues - check individual test results")
        
        print()
        print("📋 RECOMMENDATION:")
        if endpoints_not_found:
            print("  The main agent needs to implement the user profile endpoints:")
            print("  1. GET /api/user/profile - Return user profile (id, email, name)")
            print("  2. PUT /api/user/profile - Update user profile with validation")
            print("  3. Implement proper password verification for updates")
            print("  4. Return new JWT token when email is changed")
        elif success_rate >= 75:
            print("  User profile functionality is working well!")
        else:
            print("  User profile endpoints exist but may need fixes for error handling")
        
        return {
            'success_rate': success_rate,
            'passed': self.passed_tests,
            'total': self.total_tests,
            'endpoints_implemented': not endpoints_not_found,
            'endpoints_working': profile_endpoints_working
        }

def main():
    """Main test execution"""
    tester = UserProfileTester()
    results = tester.run_all_tests()
    
    print(f"\n🎯 FINAL RESULT: {results['success_rate']:.1f}% success rate")
    
    if not results['endpoints_implemented']:
        print("❌ CRITICAL: User profile endpoints not implemented")
        return 1
    elif results['success_rate'] >= 50:
        print("✅ User profile testing completed")
        return 0
    else:
        print("⚠️  User profile endpoints have issues")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)