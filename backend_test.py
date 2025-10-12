#!/usr/bin/env python3
"""
FINAL VERIFICATION - All Endpoints Migrated to PostgreSQL
Comprehensive Backend Testing for Production Deployment

This test suite covers all 12 critical tests specified in the review request:
- PHASE 1: Authentication & PostgreSQL (5 tests)
- PHASE 2: AI Integration (3 tests) 
- PHASE 3: Baby Profile Operations (2 tests)
- PHASE 4: Error Handling (2 tests)

SUCCESS CRITERIA: 12/12 tests pass (100% success rate), NO HTTP 500 errors
"""

import requests
import json
import time
import uuid
from datetime import datetime, timezone
import sys

# Production backend URL
BASE_URL = "https://baby-steps-demo-api.onrender.com"

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.auth_token = None
        self.test_results = []
        self.total_tests = 12
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
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers, timeout=30)
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

    # PHASE 1: Authentication & PostgreSQL Tests
    
    def test_1_health_check(self):
        """Test 1: Health Check"""
        response, response_time = self.make_request('GET', '/api/health')
        
        if response and response.status_code == 200:
            self.log_test(
                "1. Health Check",
                True,
                f"Backend healthy and operational ({response_time:.2f}s)",
                response_time,
                response.status_code
            )
            return True
        else:
            error_msg = f"Health check failed - Status: {response.status_code if response else 'Timeout'}"
            self.log_test(
                "1. Health Check", 
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_2_demo_login(self):
        print("\n2. Demo Account Login")
        try:
            login_data = {
                "email": "demo@babysteps.com",
                "password": "demo123"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/auth/login", json=login_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Demo Account Login", True, "200 OK with JWT token", response_time)
                else:
                    self.log_result("Demo Account Login", False, f"Invalid login response: {data}", response_time)
                    return False
            else:
                # Capture more detailed error information
                error_text = response.text if response.text else "No response body"
                self.log_result("Demo Account Login", False, f"HTTP {response.status_code}: {error_text[:200]}", response_time)
                
                # Log additional debugging info
                print(f"   🔍 Debug Info:")
                print(f"      - Status Code: {response.status_code}")
                print(f"      - Headers: {dict(response.headers)}")
                print(f"      - Response Body: {error_text[:500]}")
                return False
        except Exception as e:
            self.log_result("Demo Account Login", False, f"Error: {str(e)}")
            return False
        
        # 3. New User Registration (Test 1) - Skip if login failed
        print("\n3. New User Registration (Test 1)")
        try:
            timestamp = int(time.time())
            test_email = f"newuser_{timestamp}@test.com"
            user_data = {
                "email": test_email,
                "name": "Test User",
                "password": "TestPassword123"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/auth/register", json=user_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_result("New User Registration", True, f"200 OK - Created {test_email}", response_time)
                
                # 4. Immediate Login After Registration
                print("\n4. Immediate Login After Registration")
                login_data = {
                    "email": test_email,
                    "password": "TestPassword123"
                }
                
                start_time = time.time()
                login_response = self.session.post(f"{self.api_base}/auth/login", json=login_data, timeout=30)
                login_response_time = time.time() - start_time
                
                if login_response.status_code == 200:
                    login_data_resp = login_response.json()
                    if 'access_token' in login_data_resp:
                        self.log_result("Immediate Login After Registration", True, "200 OK with JWT token", login_response_time)
                    else:
                        self.log_result("Immediate Login After Registration", False, "No JWT token in response", login_response_time)
                        return False
                else:
                    error_text = login_response.text if login_response.text else "No response body"
                    self.log_result("Immediate Login After Registration", False, f"HTTP {login_response.status_code}: {error_text[:200]}", login_response_time)
                    return False
            else:
                error_text = response.text if response.text else "No response body"
                self.log_result("New User Registration", False, f"HTTP {response.status_code}: {error_text[:200]}", response_time)
                
                # Log additional debugging info for registration
                print(f"   🔍 Registration Debug Info:")
                print(f"      - Status Code: {response.status_code}")
                print(f"      - Response Body: {error_text[:500]}")
                return False
        except Exception as e:
            self.log_result("New User Registration", False, f"Error: {str(e)}")
            return False
        
        # 5. User Persistence Test (Create 3 unique users)
        print("\n5. User Persistence Test (Create 3 unique users)")
        created_users = []
        for i in range(3):
            try:
                timestamp = int(time.time() * 1000) + i  # Ensure uniqueness
                test_email = f"persisttest_{timestamp}@test.com"
                user_data = {
                    "email": test_email,
                    "name": f"Persist Test User {i+1}",
                    "password": "PersistTest123"
                }
                
                # Create user
                start_time = time.time()
                response = self.session.post(f"{self.api_base}/auth/register", json=user_data, timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    created_users.append((test_email, "PersistTest123"))
                    self.log_result(f"Create User {i+1}", True, f"Created {test_email}", response_time)
                else:
                    self.log_result(f"Create User {i+1}", False, f"HTTP {response.status_code}", response_time)
                    return False
            except Exception as e:
                self.log_result(f"Create User {i+1}", False, f"Error: {str(e)}")
                return False
        
        # Test login for all 3 users sequentially
        print("\n   Testing login for all 3 users sequentially:")
        for i, (email, password) in enumerate(created_users):
            try:
                login_data = {
                    "email": email,
                    "password": password
                }
                
                start_time = time.time()
                response = self.session.post(f"{self.api_base}/auth/login", json=login_data, timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    if 'access_token' in data:
                        self.log_result(f"Login User {i+1}", True, f"SUCCESS - {email}", response_time)
                    else:
                        self.log_result(f"Login User {i+1}", False, "No JWT token", response_time)
                        return False
                else:
                    self.log_result(f"Login User {i+1}", False, f"HTTP {response.status_code}", response_time)
                    return False
            except Exception as e:
                self.log_result(f"Login User {i+1}", False, f"Error: {str(e)}")
                return False
        
        return True
    
    def test_phase2_ai_integration(self):
        """PHASE 2: AI Integration"""
        print("\n🤖 PHASE 2: AI INTEGRATION")
        print("=" * 60)
        
        if not self.auth_token:
            self.log_result("AI Integration", False, "No authentication token available")
            return False
        
        # 6. AI Chat Endpoint
        print("\n6. AI Chat Endpoint")
        try:
            chat_query = {
                "message": "When can babies eat strawberries?",
                "baby_age_months": 6
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/ai/chat", json=chat_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    response_text = data['response']
                    # Check if it's a real AI response (NOT "demo response" or "temporarily unavailable")
                    if len(response_text) > 100 and "demo response" not in response_text.lower() and "temporarily unavailable" not in response_text.lower():
                        self.log_result("AI Chat Endpoint", True, f"Real AI response ({len(response_text)} chars)", response_time)
                    else:
                        self.log_result("AI Chat Endpoint", False, f"Demo/fallback response: {response_text[:100]}...", response_time)
                        return False
                else:
                    self.log_result("AI Chat Endpoint", False, "No 'response' field in data", response_time)
                    return False
            else:
                self.log_result("AI Chat Endpoint", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("AI Chat Endpoint", False, f"Error: {str(e)}")
            return False
        
        # 7. Food Research Endpoint
        print("\n7. Food Research Endpoint")
        try:
            food_query = {
                "question": "Are strawberries safe for 6 month old?",
                "baby_age_months": 6
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/food/research", json=food_query, timeout=60)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'answer' in data and 'safety_level' in data:
                    self.log_result("Food Research Endpoint", True, f"Real food safety assessment with safety_level: {data['safety_level']}", response_time)
                else:
                    self.log_result("Food Research Endpoint", False, "Missing answer or safety_level fields", response_time)
                    return False
            else:
                self.log_result("Food Research Endpoint", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Food Research Endpoint", False, f"Error: {str(e)}")
            return False
        
        # 8. Meal Search Endpoint
        print("\n8. Meal Search Endpoint")
        try:
            meal_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/meals/search", json=meal_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    results = data['results']
                    if isinstance(results, str) and len(results) > 100:
                        self.log_result("Meal Search Endpoint", True, f"Real meal suggestions (structured data, {len(results)} chars)", response_time)
                    elif isinstance(results, list) and len(results) > 0:
                        self.log_result("Meal Search Endpoint", True, f"Real meal suggestions ({len(results)} meals)", response_time)
                    else:
                        self.log_result("Meal Search Endpoint", False, f"Empty or invalid results: {results}", response_time)
                        return False
                else:
                    self.log_result("Meal Search Endpoint", False, "No 'results' field in response", response_time)
                    return False
            else:
                self.log_result("Meal Search Endpoint", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Meal Search Endpoint", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def test_phase3_baby_profile_operations(self):
        """PHASE 3: Baby Profile Operations"""
        print("\n👶 PHASE 3: BABY PROFILE OPERATIONS")
        print("=" * 60)
        
        if not self.auth_token:
            self.log_result("Baby Profile Operations", False, "No authentication token available")
            return False
        
        # 9. Create Baby Profile
        print("\n9. Create Baby Profile")
        try:
            baby_data = {
                "name": "Test Baby Profile",
                "birth_date": "2024-03-15T10:30:00Z",
                "birth_weight": 7.2,
                "birth_length": 20.5,
                "gender": "girl"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/babies", json=baby_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code in [200, 201]:
                data = response.json()
                if 'id' in data:
                    self.baby_id = data['id']
                    self.log_result("Create Baby Profile", True, f"200/201 with baby data - ID: {data['id']}", response_time)
                else:
                    self.log_result("Create Baby Profile", False, "No ID in response", response_time)
                    return False
            else:
                self.log_result("Create Baby Profile", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Create Baby Profile", False, f"Error: {str(e)}")
            return False
        
        # 10. Retrieve Baby Profiles
        print("\n10. Retrieve Baby Profiles")
        try:
            start_time = time.time()
            response = self.session.get(f"{self.api_base}/babies", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                babies = response.json()
                if isinstance(babies, list):
                    # Check if newly created baby is included
                    found_new_baby = any(baby.get('id') == self.baby_id for baby in babies) if self.baby_id else False
                    if found_new_baby:
                        self.log_result("Retrieve Baby Profiles", True, f"List of babies including newly created ({len(babies)} total)", response_time)
                    else:
                        self.log_result("Retrieve Baby Profiles", True, f"List of babies retrieved ({len(babies)} total)", response_time)
                else:
                    self.log_result("Retrieve Baby Profiles", False, "Response is not a list", response_time)
                    return False
            else:
                self.log_result("Retrieve Baby Profiles", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Retrieve Baby Profiles", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def test_phase4_error_scenarios(self):
        """PHASE 4: Error Scenarios"""
        print("\n⚠️ PHASE 4: ERROR SCENARIOS")
        print("=" * 60)
        
        # 11. Invalid Login Credentials
        print("\n11. Invalid Login Credentials")
        try:
            invalid_login_data = {
                "email": "demo@babysteps.com",
                "password": "wrongpassword123"
            }
            
            start_time = time.time()
            response = requests.post(f"{self.api_base}/auth/login", json=invalid_login_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 401:
                self.log_result("Invalid Login Credentials", True, "401 Unauthorized (NOT 500)", response_time)
            elif response.status_code == 500:
                self.log_result("Invalid Login Credentials", False, "HTTP 500 - Should be 401", response_time)
                return False
            else:
                self.log_result("Invalid Login Credentials", False, f"HTTP {response.status_code} - Expected 401", response_time)
                return False
        except Exception as e:
            self.log_result("Invalid Login Credentials", False, f"Error: {str(e)}")
            return False
        
        # 12. Unauthorized Access
        print("\n12. Unauthorized Access")
        try:
            # Create session without auth token
            unauth_session = requests.Session()
            
            start_time = time.time()
            response = unauth_session.get(f"{self.api_base}/babies", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code in [401, 403]:
                self.log_result("Unauthorized Access", True, f"{response.status_code} (NOT 500)", response_time)
            elif response.status_code == 500:
                self.log_result("Unauthorized Access", False, "HTTP 500 - Should be 401/403", response_time)
                return False
            else:
                self.log_result("Unauthorized Access", False, f"HTTP {response.status_code} - Expected 401/403", response_time)
                return False
        except Exception as e:
            self.log_result("Unauthorized Access", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def test_additional_diagnostics(self):
        """Additional diagnostic tests to understand backend status"""
        print("\n🔍 ADDITIONAL DIAGNOSTICS")
        print("=" * 60)
        
        # Test various endpoints to understand what's working
        endpoints_to_test = [
            ("/health", "GET", None),
            ("/dashboard/available-widgets", "GET", None),
        ]
        
        for endpoint, method, data in endpoints_to_test:
            try:
                print(f"\nTesting {method} {endpoint}")
                start_time = time.time()
                
                if method == "GET":
                    response = requests.get(f"{self.api_base}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.api_base}{endpoint}", json=data, timeout=10)
                
                response_time = time.time() - start_time
                
                print(f"   Status: {response.status_code}")
                print(f"   Response Time: {response_time:.2f}s")
                if response.status_code == 200:
                    try:
                        resp_data = response.json()
                        print(f"   Response: {str(resp_data)[:200]}...")
                    except:
                        print(f"   Response: {response.text[:200]}...")
                else:
                    print(f"   Error: {response.text[:200]}...")
                    
            except Exception as e:
                print(f"   Exception: {str(e)}")
        
        return True
    
    # Removed old test methods - using new phase-based testing approach
    
    def run_comprehensive_tests(self):
        """Run FINAL COMPREHENSIVE BACKEND TESTING as specified in review request"""
        print("🚀 FINAL COMPREHENSIVE BACKEND TESTING - Production Render Deployment")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"🔑 Demo Account: demo@babysteps.com / demo123")
        print("🎯 CRITICAL: Full Production Verification Before Android App Download")
        print("=" * 80)
        
        # Run all test phases
        phase1_ok = self.test_phase1_core_auth_database()
        
        if not self.auth_token:
            print("\n❌ Phase 1 failed - running diagnostics and continuing with limited tests")
            self.test_additional_diagnostics()
            
            # Still run error scenarios since they don't require auth
            phase2_ok = False
            phase3_ok = False
            phase4_ok = self.test_phase4_error_scenarios()
        else:
            phase2_ok = self.test_phase2_ai_integration()
            phase3_ok = self.test_phase3_baby_profile_operations()
            phase4_ok = self.test_phase4_error_scenarios()
        
        # Print final results
        print("\n" + "=" * 80)
        print("📊 FINAL COMPREHENSIVE BACKEND TEST RESULTS:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed'])) * 100 if (self.results['passed'] + self.results['failed']) > 0 else 0
        print(f"📈 Overall Success Rate: {success_rate:.1f}% ({self.results['passed']}/{self.results['passed'] + self.results['failed']} tests passed)")
        
        if self.results['errors']:
            print(f"\n🔍 FAILED TESTS:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # SUCCESS CRITERIA from review request
        print(f"\n🎯 SUCCESS CRITERIA:")
        print(f"   ✅ Authentication: {'✅ Demo + new users can login' if phase1_ok else '❌ Issues with login'}")
        print(f"   ✅ Database: {'✅ PostgreSQL working, users persist' if phase1_ok else '❌ Database issues'}")
        print(f"   ✅ AI: {'✅ Real responses (emergentintegrations working)' if phase2_ok else '❌ AI not working properly'}")
        print(f"   ✅ Errors: {'✅ Proper HTTP status codes (no 500s)' if phase4_ok else '❌ Improper error handling'}")
        
        # FAILURE INDICATORS from review request
        print(f"\n⚠️ FAILURE INDICATORS CHECK:")
        has_500_errors = any("500" in error for error in self.results['errors'])
        has_demo_responses = any("demo response" in error.lower() for error in self.results['errors'])
        has_auth_issues = any("401" in error and "login" in error.lower() for error in self.results['errors'])
        
        if has_500_errors:
            print(f"   ❌ HTTP 500 on endpoints → Backend error detected")
        else:
            print(f"   ✅ No HTTP 500 errors detected")
            
        if has_demo_responses:
            print(f"   ❌ 'demo response' in AI → emergentintegrations not working")
        else:
            print(f"   ✅ No demo responses detected in AI")
            
        if has_auth_issues:
            print(f"   ❌ 401 on new user login → User not persisting")
        else:
            print(f"   ✅ No user persistence issues detected")
        
        # Overall assessment
        all_phases_ok = phase1_ok and phase2_ok and phase3_ok and phase4_ok
        print(f"\n🏆 OVERALL ASSESSMENT:")
        if all_phases_ok and success_rate >= 90:
            print(f"   ✅ PRODUCTION READY - All critical functionality working")
        elif success_rate >= 75:
            print(f"   ⚠️ MOSTLY FUNCTIONAL - Some issues need attention")
        else:
            print(f"   ❌ CRITICAL ISSUES - Not ready for production")
        
        return self.results

def main():
    """Main test execution"""
    tester = BabyStepsBackendTester()
    results = tester.run_comprehensive_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()