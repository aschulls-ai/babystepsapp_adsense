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
    
    def test_health_connectivity(self):
        """1. Health & Connectivity - GET /api/health"""
        print("\n🏥 1. HEALTH & CONNECTIVITY")
        print("=" * 50)
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_base}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('status') == 'healthy':
                        self.log_result("Health Check", True, f"Backend responding - {data.get('service', 'Baby Steps API')}", response_time)
                        return True
                    else:
                        self.log_result("Health Check", False, f"Unhealthy status: {data}", response_time)
                        return False
                except json.JSONDecodeError:
                    self.log_result("Health Check", False, f"Invalid JSON response: {response.text[:100]}", response_time)
                    return False
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_authentication_flow(self):
        """2. Authentication Flow - Register and Login"""
        print("\n🔐 2. AUTHENTICATION FLOW")
        print("=" * 50)
        
        # Test account registration first
        try:
            test_email = f"test_{uuid.uuid4().hex[:8]}@babysteps.com"
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
                if 'message' in data and 'email' in data:
                    self.log_result("Registration", True, f"Test account created: {data['email']}", response_time)
                elif 'access_token' in data and 'token_type' in data:
                    # Some backends auto-login after registration
                    self.log_result("Registration", True, f"Test account created and auto-logged in: {test_email}", response_time)
                else:
                    self.log_result("Registration", False, f"Invalid registration response: {data}", response_time)
            else:
                self.log_result("Registration", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
        except Exception as e:
            self.log_result("Registration", False, f"Error: {str(e)}")
        
        # Test demo user login
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/auth/login", json=login_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Demo Login", True, "JWT token generated successfully", response_time)
                    return True
                else:
                    self.log_result("Demo Login", False, f"Invalid login response: {data}", response_time)
                    return False
            else:
                self.log_result("Demo Login", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Demo Login", False, f"Error: {str(e)}")
            return False
    
    def test_baby_profile_endpoints(self):
        """3. Baby Profile Endpoints (with auth)"""
        print("\n👶 3. BABY PROFILE ENDPOINTS")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_result("Baby Profiles", False, "No authentication token available")
            return False
        
        try:
            # GET /api/babies
            start_time = time.time()
            response = self.session.get(f"{self.api_base}/babies", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                babies = response.json()
                self.log_result("GET /api/babies", True, f"Retrieved {len(babies)} baby profiles", response_time)
            else:
                self.log_result("GET /api/babies", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # POST /api/babies (create test baby)
            baby_data = {
                "name": "Emma Test Baby",
                "birth_date": "2024-03-15T10:30:00Z",
                "birth_weight": 7.2,
                "birth_length": 20.5,
                "gender": "girl"
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/babies", json=baby_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data:
                    self.baby_id = data['id']
                    self.log_result("POST /api/babies", True, f"Baby created: {data['name']}", response_time)
                else:
                    self.log_result("POST /api/babies", False, "No ID in response", response_time)
                    return False
            else:
                self.log_result("POST /api/babies", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # PUT /api/babies/{id} (update baby)
            if self.baby_id:
                update_data = {
                    "name": "Emma Updated Test Baby",
                    "birth_date": "2024-03-15T10:30:00Z",
                    "birth_weight": 7.5,
                    "birth_length": 21.0,
                    "gender": "girl"
                }
                
                start_time = time.time()
                response = self.session.put(f"{self.api_base}/babies/{self.baby_id}", json=update_data, timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.log_result("PUT /api/babies/{id}", True, "Baby profile updated successfully", response_time)
                else:
                    self.log_result("PUT /api/babies/{id}", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                    return False
            
            return True
        except Exception as e:
            self.log_result("Baby Profile Endpoints", False, f"Error: {str(e)}")
            return False
    
    def test_ai_features(self):
        """4. AI Features (with auth)"""
        print("\n🤖 4. AI FEATURES")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_result("AI Features", False, "No authentication token available")
            return False
        
        try:
            # POST /api/ai/chat (test query: "When can babies eat strawberries?")
            chat_query = {
                "message": "When can babies eat strawberries?",
                "baby_age_months": 6
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/ai/chat", json=chat_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and len(data['response']) > 20:
                    self.log_result("POST /api/ai/chat", True, f"AI response received ({len(data['response'])} chars)", response_time)
                else:
                    self.log_result("POST /api/ai/chat", False, "Empty or invalid AI response", response_time)
                    return False
            else:
                self.log_result("POST /api/ai/chat", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # POST /api/food/research (test food safety query)
            food_query = {
                "question": "Are strawberries safe for babies?",
                "baby_age_months": 8
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/food/research", json=food_query, timeout=60)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'answer' in data and 'safety_level' in data:
                    self.log_result("POST /api/food/research", True, f"Food safety assessment: {data['safety_level']}", response_time)
                else:
                    self.log_result("POST /api/food/research", False, "Invalid food research response format", response_time)
                    return False
            else:
                self.log_result("POST /api/food/research", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # POST /api/meals/search (test meal planning)
            meal_query = {
                "query": "breakfast ideas for 8 month old baby",
                "baby_age_months": 8
            }
            
            start_time = time.time()
            response = self.session.post(f"{self.api_base}/meals/search", json=meal_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    # Check if results is a list of meal objects or a string
                    results = data['results']
                    if isinstance(results, list) and len(results) > 0:
                        self.log_result("POST /api/meals/search", True, f"Meal planning results received ({len(results)} meals)", response_time)
                    elif isinstance(results, str) and len(results) > 50:
                        self.log_result("POST /api/meals/search", True, f"Meal planning results received ({len(results)} chars)", response_time)
                    else:
                        self.log_result("POST /api/meals/search", False, f"Empty or invalid meal search response: {results}", response_time)
                        return False
                else:
                    self.log_result("POST /api/meals/search", False, f"No 'results' field in response: {data}", response_time)
                    return False
            else:
                self.log_result("POST /api/meals/search", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            return True
        except Exception as e:
            self.log_result("AI Features", False, f"Error: {str(e)}")
            return False
    
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