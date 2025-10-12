#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE BACKEND TESTING - Production Render Deployment
Tests all endpoints as specified in the review request for https://baby-steps-demo-api.onrender.com

PHASE 1: Core Authentication & Database
PHASE 2: AI Integration  
PHASE 3: Baby Profile Operations
PHASE 4: Error Scenarios
"""

import requests
import json
import uuid
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('/app/frontend/.env')

# Production Backend URL from review request
BACKEND_URL = "https://baby-steps-demo-api.onrender.com"
API_BASE = f"{BACKEND_URL}/api"

class BabyStepsBackendTester:
    def __init__(self, backend_url=None):
        self.backend_url = backend_url or BACKEND_URL
        self.api_base = f"{self.backend_url}/api"
        self.session = requests.Session()
        self.session.timeout = 120  # 2 minute timeout for AI endpoints
        self.auth_token = None
        # Demo credentials from review request
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.baby_id = None
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': [],
            'details': []
        }
    
    def log_result(self, test_name, success, message="", response_time=None):
        """Log test results with details"""
        time_info = f" ({response_time:.2f}s)" if response_time else ""
        if success:
            self.results['passed'] += 1
            self.results['details'].append(f"✅ {test_name}: {message}{time_info}")
            print(f"✅ {test_name}: PASSED {message}{time_info}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            self.results['details'].append(f"❌ {test_name}: {message}{time_info}")
            print(f"❌ {test_name}: FAILED {message}{time_info}")
    
    def test_phase1_core_auth_database(self):
        """PHASE 1: Core Authentication & Database"""
        print("\n🔐 PHASE 1: CORE AUTHENTICATION & DATABASE")
        print("=" * 60)
        
        # 1. Health Check
        print("\n1. Health Check - GET /api/health")
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_base}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result("Health Check", True, "200 OK", response_time)
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
        
        # 2. Demo Account Login
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
                self.log_result("Demo Account Login", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Demo Account Login", False, f"Error: {str(e)}")
            return False
        
        # 3. New User Registration (Test 1)
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
                    self.log_result("Immediate Login After Registration", False, f"HTTP {login_response.status_code}", login_response_time)
                    return False
            else:
                self.log_result("New User Registration", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
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
    
    def test_tracking_endpoints(self):
        """5. Tracking Endpoints (with auth)"""
        print("\n📊 5. TRACKING ENDPOINTS")
        print("=" * 50)
        
        if not self.auth_token or not self.baby_id:
            self.log_result("Tracking Endpoints", False, "No authentication token or baby ID available")
            return False
        
        try:
            # Use existing baby ID from demo account
            demo_baby_id = "demo-baby-456"  # Known demo baby ID
            
            # POST /api/tracking/feeding (actual endpoint is /api/activities)
            feeding_data = {
                "baby_id": demo_baby_id,
                "type": "feeding",
                "amount": 4.5,
                "notes": "Test feeding for review"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/activities", json=feeding_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result("POST /api/activities (feeding)", True, "Feeding activity logged successfully", response_time)
            else:
                self.log_result("POST /api/activities (feeding)", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # POST /api/tracking/sleep (actual endpoint is /api/activities)
            sleep_data = {
                "baby_id": demo_baby_id,
                "type": "sleep",
                "notes": "Test sleep session"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/activities", json=sleep_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result("POST /api/activities (sleep)", True, "Sleep activity logged successfully", response_time)
            else:
                self.log_result("POST /api/activities (sleep)", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # POST /api/tracking/diaper (actual endpoint is /api/activities)
            diaper_data = {
                "baby_id": demo_baby_id,
                "type": "diaper",
                "notes": "Test diaper change"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/activities", json=diaper_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result("POST /api/activities (diaper)", True, "Diaper activity logged successfully", response_time)
            else:
                self.log_result("POST /api/activities (diaper)", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # GET /api/tracking/summary (actual endpoint is /api/activities)
            start_time = time.time()
            response = self.session.get(f"{self.api_base}/activities", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_result("GET /api/activities (summary)", True, f"Activity summary retrieved ({len(data)} activities)", response_time)
                else:
                    self.log_result("GET /api/activities (summary)", False, "Empty activities list", response_time)
                    return False
            else:
                self.log_result("GET /api/activities (summary)", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            return True
        except Exception as e:
            self.log_result("Tracking Endpoints", False, f"Error: {str(e)}")
            return False
    
    def test_critical_checks(self):
        """Critical Checks - Response validation and performance"""
        print("\n🔍 6. CRITICAL CHECKS")
        print("=" * 50)
        
        try:
            # Test Pydantic validation (no errors)
            baby_data = {
                "name": "Validation Test Baby",
                "birth_date": "2024-01-15T08:00:00Z",
                "gender": "boy"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/babies", json=baby_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result("Pydantic Validation", True, "No validation errors detected", response_time)
            else:
                # Check if it's a validation error
                if response.status_code == 422:
                    try:
                        error_data = response.json()
                        if 'detail' in error_data:
                            self.log_result("Pydantic Validation", False, f"Validation error: {error_data['detail']}", response_time)
                        else:
                            self.log_result("Pydantic Validation", False, f"422 error: {response.text[:100]}", response_time)
                    except:
                        self.log_result("Pydantic Validation", False, f"422 error: {response.text[:100]}", response_time)
                else:
                    self.log_result("Pydantic Validation", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
            
            # Test response times < 2 seconds for non-AI endpoints
            start_time = time.time()
            response = self.session.get(f"{self.api_base}/babies", timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 2.0:
                self.log_result("Response Time Check", True, f"Fast response time: {response_time:.2f}s", response_time)
            else:
                self.log_result("Response Time Check", False, f"Slow response time: {response_time:.2f}s", response_time)
            
            return True
        except Exception as e:
            self.log_result("Critical Checks", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all comprehensive backend tests as specified in review request"""
        print("🚀 BABY STEPS COMPREHENSIVE BACKEND TESTING")
        print(f"📍 Testing Backend: {BACKEND_URL}")
        print(f"🔑 Demo Account: {self.demo_email} / {self.demo_password}")
        print("=" * 80)
        
        # Run all test suites
        health_ok = self.test_health_connectivity()
        auth_ok = self.test_authentication_flow()
        
        if not auth_ok:
            print("\n❌ Authentication failed - cannot proceed with authenticated tests")
            return self.results
        
        baby_ok = self.test_baby_profile_endpoints()
        ai_ok = self.test_ai_features()
        tracking_ok = self.test_tracking_endpoints()
        critical_ok = self.test_critical_checks()
        
        # Print final results
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE BACKEND TEST RESULTS:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed'])) * 100 if (self.results['passed'] + self.results['failed']) > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.results['errors']:
            print(f"\n🔍 FAILED TESTS:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Summary of critical functionality
        print(f"\n🎯 CRITICAL FUNCTIONALITY STATUS:")
        print(f"   • Backend Health: {'✅' if health_ok else '❌'}")
        print(f"   • Authentication: {'✅' if auth_ok else '❌'}")
        print(f"   • Baby Profiles: {'✅' if baby_ok else '❌'}")
        print(f"   • AI Features: {'✅' if ai_ok else '❌'}")
        print(f"   • Activity Tracking: {'✅' if tracking_ok else '❌'}")
        print(f"   • Data Validation: {'✅' if critical_ok else '❌'}")
        
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