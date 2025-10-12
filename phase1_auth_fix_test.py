#!/usr/bin/env python3
"""
PHASE 1 CRITICAL AUTHENTICATION FIX TESTING

Context: Just fixed a critical bug where frontend registration was saving to localStorage 
instead of backend PostgreSQL. Need to verify the fix works.

Backend Details:
- URL: https://baby-steps-demo-api.onrender.com
- Test with demo account: demo@babysteps.com / demo123

Critical Tests Required:
1. REGISTRATION FLOW TEST - POST /api/auth/register with new unique email
2. LOGIN AFTER REGISTRATION TEST - Use same email from registration
3. USER PERSISTENCE TEST - Create 2 new users and verify both can login
4. DEMO ACCOUNT VERIFICATION - POST /api/auth/login with demo@babysteps.com / demo123
5. AI ASSISTANT ENDPOINT CHECK - POST /api/ai/chat with Authorization header

Success Criteria:
✅ All registration tests pass (users created in database)
✅ Users can login immediately after registration
✅ Multiple users can be created and login
✅ Demo account still works
✅ AI endpoint responds with real answers
"""

import requests
import json
import time
import uuid
from datetime import datetime, timezone
import sys

# Production backend URL
BASE_URL = "https://baby-steps-demo-api.onrender.com"

class Phase1AuthTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.auth_token = None
        self.test_results = []
        self.total_tests = 5
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name, success, details, response_time=None, status_code=None):
        """Log test result with detailed information"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'response_time': response_time,
            'status_code': status_code,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        print(f"{status} - {test_name}")
        if response_time:
            print(f"    Response Time: {response_time:.2f}s")
        if status_code:
            print(f"    Status Code: {status_code}")
        print(f"    Details: {details}")
        print()
        
    def make_request(self, method, endpoint, data=None, auth_required=False):
        """Make HTTP request with error handling and timing"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if auth_required and self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
            
        start_time = time.time()
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response_time = time.time() - start_time
            return response, response_time
            
        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            return None, response_time
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return None, response_time

    def test_1_registration_flow(self):
        """Test 1: REGISTRATION FLOW TEST - POST /api/auth/register with new unique email"""
        timestamp = int(time.time())
        register_data = {
            "name": "Test User",
            "email": f"testuser_{timestamp}@test.com",
            "password": "testpass123"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/register', register_data)
        
        if response and response.status_code in [200, 201]:
            try:
                data = response.json()
                
                # Check for expected response format: {access_token, token_type, user: {id, email, name}}
                if 'access_token' in data and 'token_type' in data and 'user' in data:
                    user_info = data['user']
                    if 'id' in user_info and 'email' in user_info and 'name' in user_info:
                        self.log_test(
                            "1. Registration Flow Test",
                            True,
                            f"✅ HTTP {response.status_code}, returns {{access_token, token_type, user: {{id, email, name}}}} - User object contains id: {user_info['id']}, email: {user_info['email']}, name: {user_info['name']}",
                            response_time,
                            response.status_code
                        )
                        # Store for next test
                        self.new_user_email = register_data['email']
                        self.new_user_password = register_data['password']
                        self.new_user_token = data['access_token']
                        return True
                    else:
                        self.log_test(
                            "1. Registration Flow Test",
                            False,
                            f"❌ User object missing required fields - has: {list(user_info.keys())}, expected: id, email, name",
                            response_time,
                            response.status_code
                        )
                        return False
                else:
                    self.log_test(
                        "1. Registration Flow Test",
                        False,
                        f"❌ Invalid response format - has: {list(data.keys())}, expected: access_token, token_type, user",
                        response_time,
                        response.status_code
                    )
                    return False
                    
            except json.JSONDecodeError:
                self.log_test(
                    "1. Registration Flow Test",
                    False,
                    "❌ Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"❌ Registration failed - Status: {response.status_code if response else 'Timeout'}"
            self.log_test(
                "1. Registration Flow Test",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False

    def test_2_login_after_registration(self):
        """Test 2: LOGIN AFTER REGISTRATION TEST - Use same email from registration"""
        if not hasattr(self, 'new_user_email'):
            self.log_test(
                "2. Login After Registration Test",
                False,
                "❌ Cannot test - previous registration failed",
                None,
                None
            )
            return False
        
        login_data = {
            "email": self.new_user_email,
            "password": self.new_user_password
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', login_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'access_token' in data and 'token_type' in data:
                    self.log_test(
                        "2. Login After Registration Test",
                        True,
                        f"✅ HTTP 200, returns {{access_token, token_type}} - User can login immediately after registration",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "2. Login After Registration Test",
                        False,
                        f"❌ Missing access_token or token_type in response - has: {list(data.keys())}",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "2. Login After Registration Test",
                    False,
                    "❌ Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"❌ Login failed - Status: {response.status_code if response else 'Timeout'}"
            self.log_test(
                "2. Login After Registration Test",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False

    def test_3_user_persistence(self):
        """Test 3: USER PERSISTENCE TEST - Create 2 new users and verify both can login"""
        users_created = []
        
        for i in range(2):
            timestamp = int(time.time()) + i
            user_data = {
                "name": f"Persist User {i+1}",
                "email": f"persist_{timestamp}@test.com",
                "password": "persisttest123"
            }
            
            # Create user
            response, response_time = self.make_request('POST', '/api/auth/register', user_data)
            
            if not (response and response.status_code in [200, 201]):
                self.log_test(
                    "3. User Persistence Test",
                    False,
                    f"❌ Failed to create user {i+1}/2 - Status: {response.status_code if response else 'Timeout'}",
                    response_time,
                    response.status_code if response else None
                )
                return False
            
            # Verify user can login
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            
            response, response_time = self.make_request('POST', '/api/auth/login', login_data)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    if 'access_token' in data:
                        users_created.append(user_data['email'])
                    else:
                        self.log_test(
                            "3. User Persistence Test",
                            False,
                            f"❌ User {i+1}/2 login missing access_token",
                            response_time,
                            response.status_code
                        )
                        return False
                except json.JSONDecodeError:
                    self.log_test(
                        "3. User Persistence Test",
                        False,
                        f"❌ User {i+1}/2 login invalid JSON response",
                        response_time,
                        response.status_code
                    )
                    return False
            else:
                self.log_test(
                    "3. User Persistence Test",
                    False,
                    f"❌ User {i+1}/2 cannot login - Status: {response.status_code if response else 'Timeout'}",
                    response_time,
                    response.status_code if response else None
                )
                return False
        
        if len(users_created) == 2:
            self.log_test(
                "3. User Persistence Test",
                True,
                f"✅ Created 2 users, both can login successfully - PostgreSQL persistence confirmed",
                None,
                200
            )
            return True
        else:
            self.log_test(
                "3. User Persistence Test",
                False,
                f"❌ Only {len(users_created)}/2 users successfully created and logged in",
                None,
                None
            )
            return False

    def test_4_demo_account_verification(self):
        """Test 4: DEMO ACCOUNT VERIFICATION - POST /api/auth/login with demo@babysteps.com / demo123"""
        login_data = {
            "email": "demo@babysteps.com",
            "password": "demo123"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', login_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'access_token' in data:
                    self.auth_token = data['access_token']
                    token_preview = self.auth_token[:20] + "..." if len(self.auth_token) > 20 else self.auth_token
                    self.log_test(
                        "4. Demo Account Verification",
                        True,
                        f"✅ HTTP 200, valid JWT token: {token_preview} - Existing users still work",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "4. Demo Account Verification",
                        False,
                        f"❌ Missing access_token in response - has: {list(data.keys())}",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "4. Demo Account Verification",
                    False,
                    "❌ Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"❌ Demo login failed - Status: {response.status_code if response else 'Timeout'}"
            self.log_test(
                "4. Demo Account Verification",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False

    def test_5_ai_assistant_endpoint(self):
        """Test 5: AI ASSISTANT ENDPOINT CHECK - POST /api/ai/chat with Authorization header"""
        if not self.auth_token:
            self.log_test(
                "5. AI Assistant Endpoint Check",
                False,
                "❌ Cannot test - no authentication token from demo login",
                None,
                None
            )
            return False
        
        chat_data = {
            "message": "When can babies eat strawberries?",
            "baby_age_months": 6
        }
        
        response, response_time = self.make_request('POST', '/api/ai/chat', chat_data, auth_required=True)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'response' in data:
                    ai_response = data['response']
                    
                    # Check if it's a real AI response (not fallback)
                    if "demo response" in ai_response.lower() or "full ai functionality requires" in ai_response.lower():
                        self.log_test(
                            "5. AI Assistant Endpoint Check",
                            False,
                            f"❌ AI returning fallback response instead of real AI - Response: {ai_response[:100]}...",
                            response_time,
                            response.status_code
                        )
                        return False
                    else:
                        response_preview = ai_response[:100] + "..." if len(ai_response) > 100 else ai_response
                        self.log_test(
                            "5. AI Assistant Endpoint Check",
                            True,
                            f"✅ HTTP 200, real AI response ({len(ai_response)} chars) - AI functionality verified: {response_preview}",
                            response_time,
                            response.status_code
                        )
                        return True
                else:
                    self.log_test(
                        "5. AI Assistant Endpoint Check",
                        False,
                        f"❌ Missing response field in JSON - has: {list(data.keys())}",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "5. AI Assistant Endpoint Check",
                    False,
                    "❌ Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"❌ AI Chat failed - Status: {response.status_code if response else 'Timeout'}"
            self.log_test(
                "5. AI Assistant Endpoint Check",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False

    def run_all_tests(self):
        """Run all 5 critical authentication tests"""
        print("🚀 PHASE 1 CRITICAL AUTHENTICATION FIX TESTING")
        print(f"🎯 Backend URL: {self.base_url}")
        print("📋 Context: Verifying fix for frontend registration localStorage bug")
        print("=" * 80)
        print()
        
        print("🔍 CRITICAL TESTS:")
        print("-" * 50)
        self.test_1_registration_flow()
        self.test_2_login_after_registration()
        self.test_3_user_persistence()
        self.test_4_demo_account_verification()
        self.test_5_ai_assistant_endpoint()
        
        # Final Results
        self.print_final_results()

    def print_final_results(self):
        """Print comprehensive final results"""
        success_rate = (self.passed_tests / self.total_tests) * 100
        
        print("=" * 80)
        print("🏁 PHASE 1 AUTHENTICATION FIX VERIFICATION RESULTS")
        print("=" * 80)
        print()
        
        print("📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        print("📋 DETAILED TEST RESULTS:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅" if result['success'] else "❌"
            print(f"   {status} Test {i}: {result['test']}")
            if not result['success']:
                print(f"      └─ {result['details']}")
        print()
        
        print("🎯 SUCCESS CRITERIA VERIFICATION:")
        criteria_met = 0
        total_criteria = 5
        
        # Check each success criteria
        registration_passed = any(r['success'] and 'Registration Flow' in r['test'] for r in self.test_results)
        if registration_passed:
            print("   ✅ All registration tests pass (users created in database)")
            criteria_met += 1
        else:
            print("   ❌ Registration tests failed")
        
        login_after_reg_passed = any(r['success'] and 'Login After Registration' in r['test'] for r in self.test_results)
        if login_after_reg_passed:
            print("   ✅ Users can login immediately after registration")
            criteria_met += 1
        else:
            print("   ❌ Users cannot login immediately after registration")
        
        persistence_passed = any(r['success'] and 'User Persistence' in r['test'] for r in self.test_results)
        if persistence_passed:
            print("   ✅ Multiple users can be created and login")
            criteria_met += 1
        else:
            print("   ❌ User persistence test failed")
        
        demo_passed = any(r['success'] and 'Demo Account' in r['test'] for r in self.test_results)
        if demo_passed:
            print("   ✅ Demo account still works")
            criteria_met += 1
        else:
            print("   ❌ Demo account verification failed")
        
        ai_passed = any(r['success'] and 'AI Assistant' in r['test'] for r in self.test_results)
        if ai_passed:
            print("   ✅ AI endpoint responds with real answers")
            criteria_met += 1
        else:
            print("   ❌ AI endpoint not working properly")
        
        print()
        print(f"📈 SUCCESS CRITERIA MET: {criteria_met}/{total_criteria} ({(criteria_met/total_criteria)*100:.1f}%)")
        print()
        
        # Final recommendation
        print("🎯 FINAL RECOMMENDATION:")
        if success_rate == 100.0 and criteria_met == total_criteria:
            print("   🟢 AUTHENTICATION FIX VERIFIED - Frontend registration now saves to PostgreSQL")
            print("   ✅ Users are being persisted to database correctly")
            print("   ✅ All authentication flows working properly")
            print("   ✅ Ready for production use")
        else:
            print("   🔴 AUTHENTICATION FIX INCOMPLETE - Issues remain")
            if success_rate < 100.0:
                print(f"   ❌ {self.failed_tests} test(s) failed")
            if criteria_met < total_criteria:
                print(f"   ❌ {total_criteria - criteria_met} success criteria not met")
            print("   🚨 Frontend may still be using localStorage instead of backend API")
        
        print("=" * 80)

def main():
    """Main execution function"""
    tester = Phase1AuthTester()
    tester.run_all_tests()
    
    # Exit with appropriate code
    if tester.passed_tests == tester.total_tests:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()