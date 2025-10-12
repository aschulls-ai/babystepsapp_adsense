#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE PRODUCTION BACKEND TESTING
Testing production backend at: https://baby-steps-demo-api.onrender.com

This script tests all critical functionality as specified in the review request:
- PHASE 1: Core Authentication & PostgreSQL
- PHASE 2: AI Integration (emergentintegrations)
- PHASE 3: Baby Profile Operations  
- PHASE 4: Error Handling
"""

import requests
import json
import time
from datetime import datetime, timezone
import uuid

# Configuration
BACKEND_URL = "https://baby-steps-demo-api.onrender.com"
TIMEOUT = 30

class ProductionBackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
        self.jwt_token = None
        self.test_results = []
        self.success_count = 0
        self.total_tests = 0
        
    def log_test(self, test_name, success, details, response_time=None):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.success_count += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        time_info = f" ({response_time:.2f}s)" if response_time else ""
        print(f"{status}: {test_name}{time_info}")
        if not success:
            print(f"   Details: {details}")
        print()
        
    def make_request(self, method, endpoint, **kwargs):
        """Make HTTP request with error handling"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            if self.jwt_token and 'headers' not in kwargs:
                kwargs['headers'] = {'Authorization': f'Bearer {self.jwt_token}'}
            elif self.jwt_token and 'headers' in kwargs:
                kwargs['headers']['Authorization'] = f'Bearer {self.jwt_token}'
                
            response = self.session.request(method, url, **kwargs)
            response_time = time.time() - start_time
            return response, response_time
        except Exception as e:
            response_time = time.time() - start_time
            return None, response_time

    def test_health_check(self):
        """PHASE 1: Health Check"""
        response, response_time = self.make_request('GET', '/api/health')
        
        if response is None:
            self.log_test("Health Check", False, "Network error or timeout", response_time)
            return False
            
        success = response.status_code == 200
        details = f"Status: {response.status_code}"
        if success:
            details += f" - Backend healthy and operational"
        else:
            details += f" - Backend health check failed: {response.text[:200]}"
            
        self.log_test("Health Check", success, details, response_time)
        return success

    def test_demo_login(self):
        """PHASE 1: Demo Account Login"""
        login_data = {
            "email": "demo@babysteps.com",
            "password": "demo123"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', json=login_data)
        
        if response is None:
            self.log_test("Demo Account Login", False, "Network error or timeout", response_time)
            return False
            
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                self.jwt_token = data.get('access_token')
                details = f"Status: {response.status_code} - JWT token generated successfully"
                if self.jwt_token:
                    details += f" (Token: {self.jwt_token[:20]}...)"
                else:
                    success = False
                    details = "No access token in response"
            except:
                success = False
                details = f"Status: {response.status_code} - Invalid JSON response"
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            
        self.log_test("Demo Account Login", success, details, response_time)
        return success

    def test_new_user_registration(self):
        """PHASE 1: New User Registration"""
        timestamp = int(time.time())
        user_data = {
            "name": "Test User Production",
            "email": f"testuser_{timestamp}@test.com",
            "password": "TestPass123"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/register', json=user_data)
        
        if response is None:
            self.log_test("New User Registration", False, "Network error or timeout", response_time)
            return False, None
            
        success = response.status_code in [200, 201]
        
        if success:
            details = f"Status: {response.status_code} - User created successfully"
            return_email = user_data["email"]
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            return_email = None
            
        self.log_test("New User Registration", success, details, response_time)
        return success, return_email

    def test_new_user_login(self, email, password="TestPass123"):
        """PHASE 1: Login with newly created user"""
        if not email:
            self.log_test("New User Login", False, "No email provided from registration", 0)
            return False
            
        login_data = {
            "email": email,
            "password": password
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', json=login_data)
        
        if response is None:
            self.log_test("New User Login", False, "Network error or timeout", response_time)
            return False
            
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                token = data.get('access_token')
                details = f"Status: {response.status_code} - New user login successful"
                if token:
                    details += f" (Token: {token[:20]}...)"
                else:
                    success = False
                    details = "No access token in response"
            except:
                success = False
                details = f"Status: {response.status_code} - Invalid JSON response"
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            
        self.log_test("New User Login", success, details, response_time)
        return success

    def test_user_persistence(self):
        """PHASE 1: User Persistence Test - Create 3 users and verify all can login"""
        users_created = []
        
        # Create 3 users
        for i in range(3):
            timestamp = int(time.time()) + i
            user_data = {
                "name": f"Persistence Test User {i+1}",
                "email": f"persist_test_{timestamp}@test.com", 
                "password": "PersistTest123"
            }
            
            response, response_time = self.make_request('POST', '/api/auth/register', json=user_data)
            
            if response and response.status_code in [200, 201]:
                users_created.append(user_data)
            else:
                self.log_test("User Persistence Test", False, f"Failed to create user {i+1}: {response.status_code if response else 'Network error'}", response_time)
                return False
        
        # Test login for all 3 users
        successful_logins = 0
        for i, user in enumerate(users_created):
            login_data = {
                "email": user["email"],
                "password": user["password"]
            }
            
            response, response_time = self.make_request('POST', '/api/auth/login', json=login_data)
            
            if response and response.status_code == 200:
                successful_logins += 1
            else:
                self.log_test("User Persistence Test", False, f"User {i+1} login failed: {response.status_code if response else 'Network error'}", response_time)
                return False
        
        success = successful_logins == 3
        details = f"Created 3 users, {successful_logins}/3 successful logins - PostgreSQL persistence {'VERIFIED' if success else 'FAILED'}"
        self.log_test("User Persistence Test", success, details, response_time)
        return success

    def test_ai_chat(self):
        """PHASE 2: AI Chat Endpoint"""
        if not self.jwt_token:
            self.log_test("AI Chat Endpoint", False, "No JWT token available", 0)
            return False
            
        chat_data = {
            "message": "When can babies eat strawberries?",
            "baby_age_months": 6
        }
        
        headers = {'Authorization': f'Bearer {self.jwt_token}'}
        response, response_time = self.make_request('POST', '/api/ai/chat', json=chat_data, headers=headers)
        
        if response is None:
            self.log_test("AI Chat Endpoint", False, "Network error or timeout", response_time)
            return False
            
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                ai_response = data.get('response', '')
                response_length = len(ai_response)
                
                # Check if it's a real AI response (not demo/fallback)
                is_real_ai = (
                    response_length > 200 and
                    'demo response' not in ai_response.lower() and
                    'temporarily unavailable' not in ai_response.lower() and
                    'full ai functionality requires proper setup' not in ai_response.lower()
                )
                
                if is_real_ai:
                    details = f"Status: {response.status_code} - REAL AI response ({response_length} chars) - emergentintegrations WORKING"
                    details += f"\nSample: {ai_response[:150]}..."
                else:
                    success = False
                    details = f"Status: {response.status_code} - FALLBACK response detected ({response_length} chars) - AI integration NOT working"
                    details += f"\nResponse: {ai_response[:150]}..."
                    
            except:
                success = False
                details = f"Status: {response.status_code} - Invalid JSON response"
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            
        self.log_test("AI Chat Endpoint", success, details, response_time)
        return success

    def test_food_research(self):
        """PHASE 2: Food Research Endpoint"""
        if not self.jwt_token:
            self.log_test("Food Research Endpoint", False, "No JWT token available", 0)
            return False
            
        food_data = {
            "question": "Are strawberries safe for babies?",
            "baby_age_months": 6
        }
        
        headers = {'Authorization': f'Bearer {self.jwt_token}'}
        response, response_time = self.make_request('POST', '/api/food/research', json=food_data, headers=headers)
        
        if response is None:
            self.log_test("Food Research Endpoint", False, "Network error or timeout", response_time)
            return False
            
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                answer = data.get('answer', '')
                safety_level = data.get('safety_level', '')
                response_length = len(answer)
                
                has_safety_assessment = safety_level in ['safe', 'caution', 'avoid', 'consult_doctor']
                
                if has_safety_assessment and response_length > 50:
                    details = f"Status: {response.status_code} - Real food safety assessment (safety_level: {safety_level}, {response_length} chars)"
                else:
                    success = False
                    details = f"Status: {response.status_code} - Invalid food research response (safety_level: {safety_level})"
                    
            except:
                success = False
                details = f"Status: {response.status_code} - Invalid JSON response"
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            
        self.log_test("Food Research Endpoint", success, details, response_time)
        return success

    def test_meal_search(self):
        """PHASE 2: Meal Search Endpoint"""
        if not self.jwt_token:
            self.log_test("Meal Search Endpoint", False, "No JWT token available", 0)
            return False
            
        meal_data = {
            "query": "breakfast ideas",
            "baby_age_months": 8
        }
        
        headers = {'Authorization': f'Bearer {self.jwt_token}'}
        response, response_time = self.make_request('POST', '/api/meals/search', json=meal_data, headers=headers)
        
        if response is None:
            self.log_test("Meal Search Endpoint", False, "Network error or timeout", response_time)
            return False
            
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                results = data.get('results', '')
                response_length = len(results)
                
                # Check for structured meal suggestions
                has_meal_content = (
                    response_length > 100 and
                    any(word in results.lower() for word in ['breakfast', 'meal', 'recipe', 'ingredient'])
                )
                
                if has_meal_content:
                    details = f"Status: {response.status_code} - Structured meal suggestions ({response_length} chars)"
                else:
                    success = False
                    details = f"Status: {response.status_code} - Invalid meal search response ({response_length} chars)"
                    
            except:
                success = False
                details = f"Status: {response.status_code} - Invalid JSON response"
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            
        self.log_test("Meal Search Endpoint", success, details, response_time)
        return success

    def test_create_baby_profile(self):
        """PHASE 3: Create Baby Profile"""
        if not self.jwt_token:
            self.log_test("Create Baby Profile", False, "No JWT token available", 0)
            return False, None
            
        baby_data = {
            "name": "Emma",
            "birth_date": "2024-01-15T00:00:00Z",
            "gender": "girl"
        }
        
        headers = {'Authorization': f'Bearer {self.jwt_token}'}
        response, response_time = self.make_request('POST', '/api/babies', json=baby_data, headers=headers)
        
        if response is None:
            self.log_test("Create Baby Profile", False, "Network error or timeout", response_time)
            return False, None
            
        success = response.status_code in [200, 201]
        baby_id = None
        
        if success:
            try:
                data = response.json()
                baby_id = data.get('id')
                details = f"Status: {response.status_code} - Baby profile created successfully"
                if baby_id:
                    details += f" (ID: {baby_id})"
            except:
                success = False
                details = f"Status: {response.status_code} - Invalid JSON response"
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            
        self.log_test("Create Baby Profile", success, details, response_time)
        return success, baby_id

    def test_retrieve_baby_profiles(self):
        """PHASE 3: Retrieve Baby Profiles"""
        if not self.jwt_token:
            self.log_test("Retrieve Baby Profiles", False, "No JWT token available", 0)
            return False
            
        headers = {'Authorization': f'Bearer {self.jwt_token}'}
        response, response_time = self.make_request('GET', '/api/babies', headers=headers)
        
        if response is None:
            self.log_test("Retrieve Baby Profiles", False, "Network error or timeout", response_time)
            return False
            
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                baby_count = len(data) if isinstance(data, list) else 0
                details = f"Status: {response.status_code} - Retrieved {baby_count} baby profiles"
            except:
                success = False
                details = f"Status: {response.status_code} - Invalid JSON response"
        else:
            details = f"Status: {response.status_code} - {response.text[:200]}"
            
        self.log_test("Retrieve Baby Profiles", success, details, response_time)
        return success

    def test_invalid_credentials(self):
        """PHASE 4: Invalid Credentials Error Handling"""
        login_data = {
            "email": "demo@babysteps.com",
            "password": "wrongpassword"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', json=login_data)
        
        if response is None:
            self.log_test("Invalid Credentials Test", False, "Network error or timeout", response_time)
            return False
            
        # Should return 401, NOT 500
        success = response.status_code == 401
        
        if success:
            details = f"Status: {response.status_code} - Proper 401 Unauthorized (NOT 500)"
        elif response.status_code == 500:
            details = f"Status: {response.status_code} - CRITICAL: Should be 401, not 500 - Server error on invalid credentials"
        else:
            details = f"Status: {response.status_code} - Unexpected status code"
            
        self.log_test("Invalid Credentials Test", success, details, response_time)
        return success

    def test_unauthorized_access(self):
        """PHASE 4: Unauthorized Access Error Handling"""
        # Try to access protected endpoint without token
        response, response_time = self.make_request('GET', '/api/babies')
        
        if response is None:
            self.log_test("Unauthorized Access Test", False, "Network error or timeout", response_time)
            return False
            
        # Should return 401/403, NOT 500
        success = response.status_code in [401, 403]
        
        if success:
            details = f"Status: {response.status_code} - Proper unauthorized response (NOT 500)"
        elif response.status_code == 500:
            details = f"Status: {response.status_code} - CRITICAL: Should be 401/403, not 500 - Server error on unauthorized access"
        else:
            details = f"Status: {response.status_code} - Unexpected status code"
            
        self.log_test("Unauthorized Access Test", success, details, response_time)
        return success

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 STARTING FINAL COMPREHENSIVE PRODUCTION BACKEND TESTING")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        # PHASE 1: Core Authentication & PostgreSQL
        print("📋 PHASE 1: CORE AUTHENTICATION & POSTGRESQL")
        print("-" * 50)
        
        health_ok = self.test_health_check()
        demo_login_ok = self.test_demo_login()
        
        reg_ok, new_user_email = self.test_new_user_registration()
        new_login_ok = self.test_new_user_login(new_user_email) if reg_ok else False
        
        persistence_ok = self.test_user_persistence()
        
        print()
        
        # PHASE 2: AI Integration (only if we have auth token)
        print("📋 PHASE 2: AI INTEGRATION (emergentintegrations)")
        print("-" * 50)
        
        if self.jwt_token:
            ai_chat_ok = self.test_ai_chat()
            food_research_ok = self.test_food_research()
            meal_search_ok = self.test_meal_search()
        else:
            print("❌ SKIPPED: No authentication token available")
            ai_chat_ok = food_research_ok = meal_search_ok = False
            
        print()
        
        # PHASE 3: Baby Profile Operations (only if we have auth token)
        print("📋 PHASE 3: BABY PROFILE OPERATIONS")
        print("-" * 50)
        
        if self.jwt_token:
            create_baby_ok, baby_id = self.test_create_baby_profile()
            retrieve_babies_ok = self.test_retrieve_baby_profiles()
        else:
            print("❌ SKIPPED: No authentication token available")
            create_baby_ok = retrieve_babies_ok = False
            
        print()
        
        # PHASE 4: Error Handling
        print("📋 PHASE 4: ERROR HANDLING")
        print("-" * 50)
        
        invalid_creds_ok = self.test_invalid_credentials()
        unauthorized_ok = self.test_unauthorized_access()
        
        print()
        
        # FINAL RESULTS
        print("=" * 80)
        print("🎯 FINAL COMPREHENSIVE TEST RESULTS")
        print("=" * 80)
        
        success_rate = (self.success_count / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Overall Success Rate: {success_rate:.1f}% ({self.success_count}/{self.total_tests} tests passed)")
        print()
        
        # Critical Success Criteria
        print("🔍 CRITICAL SUCCESS CRITERIA VERIFICATION:")
        print(f"✅ All authentication endpoints return 200/401 (NO 500 errors): {'YES' if (demo_login_ok and invalid_creds_ok) else 'NO'}")
        print(f"✅ PostgreSQL working (users persist): {'YES' if persistence_ok else 'NO'}")
        print(f"✅ AI returns REAL responses (emergentintegrations working): {'YES' if (ai_chat_ok and food_research_ok) else 'NO'}")
        print(f"✅ Proper error codes (401/403, not 500): {'YES' if (invalid_creds_ok and unauthorized_ok) else 'NO'}")
        print(f"✅ Overall success rate: >90%: {'YES' if success_rate > 90 else 'NO'}")
        print()
        
        # Determine overall status
        critical_failures = []
        if not health_ok:
            critical_failures.append("Health check failed")
        if not demo_login_ok:
            critical_failures.append("Demo login failed")
        if not persistence_ok:
            critical_failures.append("Database persistence failed")
        if not (ai_chat_ok and food_research_ok):
            critical_failures.append("AI integration failed")
        if not (invalid_creds_ok and unauthorized_ok):
            critical_failures.append("Error handling failed")
        if success_rate <= 90:
            critical_failures.append("Success rate below 90%")
            
        if not critical_failures:
            print("🎉 PRODUCTION BACKEND STATUS: ✅ READY FOR PRODUCTION")
            print("All critical functionality verified and working correctly!")
            print("✅ AI integration available")
            print("✅ PostgreSQL persistence confirmed")
            print("✅ Authentication working perfectly")
        else:
            print("❌ PRODUCTION BACKEND STATUS: ❌ NOT READY FOR PRODUCTION")
            print("Critical issues found:")
            for failure in critical_failures:
                print(f"  • {failure}")
                
        print()
        print("📊 DETAILED TEST BREAKDOWN:")
        for result in self.test_results:
            print(f"{result['status']}: {result['test']}")
            if not result['success']:
                print(f"   {result['details']}")
                
        return success_rate >= 90 and len(critical_failures) == 0

if __name__ == "__main__":
    tester = ProductionBackendTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 CONCLUSION: Backend is ready for Android app download!")
    else:
        print("\n⚠️  CONCLUSION: Backend requires fixes before Android app download!")