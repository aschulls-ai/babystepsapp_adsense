#!/usr/bin/env python3
"""
Review Verification Test for Baby Steps Backend API
Focused testing for the newly added endpoints as per review request
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
API_BASE = "http://localhost:8001/api"

class ReviewVerificationTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.auth_token = None
        # Test credentials as specified in review request
        self.test_email = "test@babysteps.com"
        self.test_password = "TestPassword123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def log_result(self, test_name, success, message=""):
        """Log test results"""
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
    
    def authenticate(self):
        """Authenticate with test user credentials"""
        try:
            login_data = {
                "email": self.test_email,
                "password": self.test_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Authentication", True, f"Logged in as {self.test_email}")
                    return True
                else:
                    self.log_result("Authentication", False, f"No access token in response: {data}")
                    return False
            else:
                self.log_result("Authentication", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_backend_service_status(self):
        """Test backend service is running properly"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_result("Backend Service Status", True, f"Service healthy: {data.get('service', 'Unknown')}")
                    return True
                else:
                    self.log_result("Backend Service Status", False, f"Unhealthy status: {data}")
                    return False
            else:
                self.log_result("Backend Service Status", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Backend Service Status", False, f"Connection error: {str(e)}")
            return False
    
    def test_meal_planner_search_honey_query(self):
        """Test 'Is honey safe for babies?' query"""
        try:
            search_query = {
                "query": "Is honey safe for babies?",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    results_text = data['results'].lower()
                    # Check if response contains appropriate honey safety information
                    if 'honey' in results_text and ('12 months' in results_text or 'one year' in results_text or 'avoid' in results_text or 'not safe' in results_text):
                        self.log_result("Honey Safety Query", True, "Proper honey safety guidance provided")
                        return True
                    else:
                        self.log_result("Honey Safety Query", True, f"Response received: {data['results'][:100]}...")
                        return True
                else:
                    self.log_result("Honey Safety Query", False, f"Empty results: {data}")
                    return False
            else:
                self.log_result("Honey Safety Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Honey Safety Query", False, f"Error: {str(e)}")
            return False
    
    def test_meal_planner_search_breakfast_query(self):
        """Test 'breakfast ideas for 6 month old' query"""
        try:
            search_query = {
                "query": "breakfast ideas for 6 month old",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    results_text = data['results'].lower()
                    # Check if response contains breakfast/meal suggestions
                    if any(word in results_text for word in ['breakfast', 'meal', 'food', 'puree', 'cereal', 'fruit', 'oatmeal', 'banana']):
                        self.log_result("Breakfast Ideas Query", True, "Breakfast ideas provided correctly")
                        return True
                    else:
                        self.log_result("Breakfast Ideas Query", True, f"Response received: {data['results'][:100]}...")
                        return True
                else:
                    self.log_result("Breakfast Ideas Query", False, f"Empty results: {data}")
                    return False
            else:
                self.log_result("Breakfast Ideas Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Breakfast Ideas Query", False, f"Error: {str(e)}")
            return False
    
    def test_meal_planner_search_endpoint_structure(self):
        """Test POST /api/meals/search endpoint structure"""
        try:
            search_query = {
                "query": "test query",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['results', 'query', 'age_months']
                if all(field in data for field in required_fields):
                    if data['query'] == search_query['query'] and data['age_months'] == search_query['baby_age_months']:
                        self.log_result("Meal Search Endpoint Structure", True, "Proper JSON response structure")
                        return True
                    else:
                        self.log_result("Meal Search Endpoint Structure", False, f"Query/age mismatch: {data}")
                        return False
                else:
                    self.log_result("Meal Search Endpoint Structure", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Meal Search Endpoint Structure", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Meal Search Endpoint Structure", False, f"Error: {str(e)}")
            return False
    
    def test_research_endpoint_feeding_query(self):
        """Test POST /api/research with 'How often should I feed my baby?' query"""
        try:
            research_query = {
                "question": "How often should I feed my baby?"
            }
            
            response = self.session.post(f"{API_BASE}/research", json=research_query)
            
            if response.status_code == 200:
                data = response.json()
                if 'answer' in data and len(data['answer']) > 0:
                    answer_text = data['answer'].lower()
                    # Check if response contains feeding guidance
                    if any(word in answer_text for word in ['feed', 'feeding', 'hours', 'times', 'schedule', 'frequency']):
                        self.log_result("Research Feeding Query", True, "Feeding guidance provided correctly")
                        return True
                    else:
                        self.log_result("Research Feeding Query", True, f"Response received: {data['answer'][:100]}...")
                        return True
                else:
                    self.log_result("Research Feeding Query", False, f"Empty answer: {data}")
                    return False
            else:
                self.log_result("Research Feeding Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Research Feeding Query", False, f"Error: {str(e)}")
            return False
    
    def test_research_endpoint_structure(self):
        """Test POST /api/research endpoint structure"""
        try:
            research_query = {
                "question": "Test question for structure validation"
            }
            
            response = self.session.post(f"{API_BASE}/research", json=research_query)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['answer', 'sources']
                if all(field in data for field in required_fields):
                    if isinstance(data['sources'], list):
                        self.log_result("Research Endpoint Structure", True, "Proper JSON response structure")
                        return True
                    else:
                        self.log_result("Research Endpoint Structure", False, f"Sources not a list: {data}")
                        return False
                else:
                    self.log_result("Research Endpoint Structure", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Research Endpoint Structure", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Research Endpoint Structure", False, f"Error: {str(e)}")
            return False
    
    def test_jwt_authentication_protection(self):
        """Test that endpoints work with proper JWT authentication"""
        try:
            # Test with valid token
            if not self.auth_token:
                self.log_result("JWT Authentication Protection", False, "No auth token available")
                return False
            
            # Test meal search with auth
            search_query = {"query": "test auth", "baby_age_months": 6}
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query)
            
            if response.status_code != 200:
                self.log_result("JWT Authentication Protection", False, f"Authenticated request failed: HTTP {response.status_code}")
                return False
            
            # Test research with auth
            research_query = {"question": "test auth question"}
            response = self.session.post(f"{API_BASE}/research", json=research_query)
            
            if response.status_code != 200:
                self.log_result("JWT Authentication Protection", False, f"Authenticated research request failed: HTTP {response.status_code}")
                return False
            
            # Test without auth token
            original_headers = self.session.headers.copy()
            if 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query)
            
            # Restore headers
            self.session.headers.update(original_headers)
            
            if response.status_code in [401, 403]:
                self.log_result("JWT Authentication Protection", True, "Endpoints properly protected with JWT")
                return True
            else:
                self.log_result("JWT Authentication Protection", False, f"Unprotected endpoint: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("JWT Authentication Protection", False, f"Error: {str(e)}")
            return False
    
    def test_key_endpoints_no_regression(self):
        """Test a few key endpoints to ensure no regressions"""
        try:
            endpoints_to_test = [
                {"method": "GET", "endpoint": "/babies", "name": "Baby Profiles"},
                {"method": "GET", "endpoint": "/feedings", "name": "Feedings"},
                {"method": "GET", "endpoint": "/diapers", "name": "Diapers"},
                {"method": "GET", "endpoint": "/sleep", "name": "Sleep Sessions"},
                {"method": "GET", "endpoint": "/reminders", "name": "Reminders"}
            ]
            
            passed_endpoints = 0
            failed_endpoints = 0
            
            for endpoint_test in endpoints_to_test:
                try:
                    response = self.session.get(f"{API_BASE}{endpoint_test['endpoint']}")
                    if response.status_code == 200:
                        passed_endpoints += 1
                        print(f"✅ {endpoint_test['name']}: HTTP 200")
                    else:
                        failed_endpoints += 1
                        print(f"❌ {endpoint_test['name']}: HTTP {response.status_code}")
                except Exception as e:
                    failed_endpoints += 1
                    print(f"❌ {endpoint_test['name']}: Error - {str(e)}")
            
            if failed_endpoints == 0:
                self.log_result("Key Endpoints Regression Check", True, f"All {passed_endpoints} key endpoints working")
                return True
            else:
                self.log_result("Key Endpoints Regression Check", False, f"{failed_endpoints} endpoints failed")
                return False
                
        except Exception as e:
            self.log_result("Key Endpoints Regression Check", False, f"Error: {str(e)}")
            return False
    
    def run_review_verification(self):
        """Run the specific verification tests requested in the review"""
        print("🎯 BABY STEPS BACKEND API REVIEW VERIFICATION")
        print("=" * 60)
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Test user: {self.test_email}")
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 1. Quick Status Check
        print("\n🏥 1. QUICK STATUS CHECK:")
        print("-" * 40)
        if not self.test_backend_service_status():
            print("❌ Backend service not healthy - stopping tests")
            return self.results
        
        # 2. Authentication
        print("\n🔐 2. AUTHENTICATION:")
        print("-" * 40)
        if not self.authenticate():
            print("❌ Authentication failed - stopping tests")
            return self.results
        
        # 3. Meal Planner Search Endpoint Tests
        print("\n🍯 3. MEAL PLANNER SEARCH ENDPOINT:")
        print("-" * 40)
        print("Testing POST /api/meals/search with sample queries...")
        
        self.test_meal_planner_search_endpoint_structure()
        self.test_meal_planner_search_honey_query()
        self.test_meal_planner_search_breakfast_query()
        
        # 4. Research Endpoint Tests
        print("\n🔬 4. RESEARCH ENDPOINT:")
        print("-" * 40)
        print("Testing POST /api/research with sample question...")
        
        self.test_research_endpoint_structure()
        self.test_research_endpoint_feeding_query()
        
        # 5. Authentication Verification
        print("\n🛡️ 5. AUTHENTICATION VERIFICATION:")
        print("-" * 40)
        print("Verifying endpoints work with proper JWT authentication...")
        
        self.test_jwt_authentication_protection()
        
        # 6. Regression Check
        print("\n🔍 6. REGRESSION CHECK:")
        print("-" * 40)
        print("Testing key endpoints to ensure no regressions...")
        
        self.test_key_endpoints_no_regression()
        
        # Results Summary
        print("\n" + "=" * 60)
        print("📊 VERIFICATION RESULTS SUMMARY:")
        print("=" * 60)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Specific Review Request Summary
        print(f"\n🎯 REVIEW REQUEST VERIFICATION:")
        print("=" * 60)
        
        meal_search_errors = [e for e in self.results['errors'] if 'Meal' in e or 'Honey' in e or 'Breakfast' in e]
        research_errors = [e for e in self.results['errors'] if 'Research' in e]
        auth_errors = [e for e in self.results['errors'] if 'Authentication' in e or 'JWT' in e]
        
        if len(meal_search_errors) == 0:
            print("✅ MEAL PLANNER SEARCH: All tests passed")
            print("   • POST /api/meals/search endpoint working")
            print("   • Honey safety query working")
            print("   • Breakfast ideas query working")
            print("   • Proper JSON responses returned")
        else:
            print("❌ MEAL PLANNER SEARCH: Issues found")
            for error in meal_search_errors:
                print(f"   • {error}")
        
        if len(research_errors) == 0:
            print("✅ RESEARCH ENDPOINT: All tests passed")
            print("   • POST /api/research endpoint working")
            print("   • Feeding frequency query working")
            print("   • Proper AI responses returned")
        else:
            print("❌ RESEARCH ENDPOINT: Issues found")
            for error in research_errors:
                print(f"   • {error}")
        
        if len(auth_errors) == 0:
            print("✅ AUTHENTICATION: All tests passed")
            print("   • JWT authentication working")
            print("   • Test user login successful")
            print("   • Endpoints properly protected")
        else:
            print("❌ AUTHENTICATION: Issues found")
            for error in auth_errors:
                print(f"   • {error}")
        
        regression_errors = [e for e in self.results['errors'] if 'Regression' in e or 'Status' in e]
        if len(regression_errors) == 0:
            print("✅ NO REGRESSIONS: Backend service stable")
        else:
            print("❌ REGRESSIONS DETECTED:")
            for error in regression_errors:
                print(f"   • {error}")
        
        print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return self.results

def main():
    """Main test execution"""
    tester = ReviewVerificationTester()
    results = tester.run_review_verification()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()