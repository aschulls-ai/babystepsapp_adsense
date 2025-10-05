#!/usr/bin/env python3
"""
Backend API Testing Suite for Baby Steps Parenting Application
Tests authentication, food research, and baby profile management functionality
"""

import requests
import json
import uuid
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment, but use localhost for testing
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://babysteps-app.preview.emergentagent.com')
# Use localhost for direct backend testing
LOCAL_BACKEND_URL = "http://localhost:8001"
API_BASE = f"{LOCAL_BACKEND_URL}/api"

class BabyStepsAPITester:
    def __init__(self):
        self.session = requests.Session()
        # Set session timeout and retry settings
        self.session.timeout = 30
        self.auth_token = None
        self.test_user_email = f"sarah.johnson.{uuid.uuid4().hex[:8]}@example.com"
        self.test_user_name = "Sarah Johnson"
        self.test_user_password = "SecureParent2024!"
        self.baby_id = None
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
    
    def test_health_check(self):
        """Test API health endpoint"""
        try:
            # Use a fresh session for health check
            response = requests.get(f"{API_BASE}/health", timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_result("Health Check", True, f"API is healthy - {data.get('service', 'Unknown service')}")
                    return True
                else:
                    self.log_result("Health Check", False, f"Unhealthy status: {data}")
                    return False
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        try:
            user_data = {
                "email": self.test_user_email,
                "name": self.test_user_name,
                "password": self.test_user_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/register", json=user_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'email' in data:
                    self.log_result("User Registration", True, f"User registered successfully: {data['message']}")
                    return True
                else:
                    self.log_result("User Registration", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_result("User Registration", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_manual_verification(self):
        """Manually verify user for testing purposes"""
        try:
            verify_data = {
                "email": self.test_user_email
            }
            
            response = self.session.post(f"{API_BASE}/auth/manual-verify", json=verify_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data:
                    self.log_result("Manual User Verification", True, "User verified for testing")
                    return True
                else:
                    self.log_result("Manual User Verification", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_result("Manual User Verification", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Manual User Verification", False, f"Error: {str(e)}")
            return False

    def test_user_login(self):
        """Test user login endpoint"""
        try:
            login_data = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    # Update token in case it's different
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("User Login", True, "Login successful")
                    return True
                else:
                    self.log_result("User Login", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_result("User Login", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_baby_profile_creation(self):
        """Test baby profile creation"""
        try:
            baby_data = {
                "name": "Emma Johnson",
                "birth_date": "2024-06-15T10:30:00Z",
                "birth_weight": 7.2,
                "birth_length": 20.5,
                "gender": "female"
            }
            
            response = self.session.post(f"{API_BASE}/babies", json=baby_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data.get('name') == baby_data['name']:
                    self.baby_id = data['id']
                    self.log_result("Baby Profile Creation", True, f"Baby profile created: {data['name']}")
                    return True
                else:
                    self.log_result("Baby Profile Creation", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_result("Baby Profile Creation", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Baby Profile Creation", False, f"Error: {str(e)}")
            return False
    
    def test_get_babies(self):
        """Test retrieving baby profiles"""
        try:
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_result("Get Baby Profiles", True, f"Retrieved {len(data)} baby profile(s)")
                    return True
                else:
                    self.log_result("Get Baby Profiles", False, f"No baby profiles found: {data}")
                    return False
            else:
                self.log_result("Get Baby Profiles", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Get Baby Profiles", False, f"Error: {str(e)}")
            return False
    
    def test_food_research_endpoint(self):
        """Test the food research endpoint"""
        try:
            # Test food safety query
            food_query = {
                "question": "Is avocado safe for my baby to eat?",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['answer', 'safety_level', 'sources']
                if all(field in data for field in required_fields):
                    if data['safety_level'] in ['safe', 'caution', 'avoid', 'consult_doctor']:
                        self.log_result("Food Research Endpoint", True, f"Safety level: {data['safety_level']}")
                        return True
                    else:
                        self.log_result("Food Research Endpoint", False, f"Invalid safety level: {data['safety_level']}")
                        return False
                else:
                    self.log_result("Food Research Endpoint", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Food Research Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Food Research Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_unified_meal_search(self):
        """Test the new unified meal search endpoint"""
        try:
            # Test meal idea search
            search_query = {
                "query": "healthy finger foods for baby",
                "baby_age_months": 9
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['results', 'query', 'age_months']
                if all(field in data for field in required_fields):
                    if data['query'] == search_query['query'] and data['age_months'] == search_query['baby_age_months']:
                        self.log_result("Unified Meal Search", True, "Meal search working correctly")
                        return True
                    else:
                        self.log_result("Unified Meal Search", False, f"Query mismatch: {data}")
                        return False
                else:
                    self.log_result("Unified Meal Search", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Unified Meal Search", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Unified Meal Search", False, f"Error: {str(e)}")
            return False
    
    def test_food_safety_search(self):
        """Test food safety queries through unified search"""
        try:
            # Test food safety query through unified search
            search_query = {
                "query": "Can my baby eat honey?",
                "baby_age_months": 10
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    self.log_result("Food Safety via Unified Search", True, "Food safety query handled")
                    return True
                else:
                    self.log_result("Food Safety via Unified Search", False, f"Empty results: {data}")
                    return False
            else:
                self.log_result("Food Safety via Unified Search", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Food Safety via Unified Search", False, f"Error: {str(e)}")
            return False
    
    def test_ai_integration(self):
        """Test AI integration by making multiple queries"""
        try:
            # Test different types of queries to verify AI is working
            queries = [
                {"question": "What are good first foods for a 6 month old?", "baby_age_months": 6},
                {"question": "Is peanut butter safe for babies?", "baby_age_months": 12}
            ]
            
            ai_working = True
            for i, query in enumerate(queries):
                response = self.session.post(f"{API_BASE}/food/research", json=query, timeout=60)
                if response.status_code != 200:
                    ai_working = False
                    break
                
                data = response.json()
                # Check if we get a meaningful response (not just error message)
                if "sorry" in data.get('answer', '').lower() or "trouble" in data.get('answer', '').lower():
                    ai_working = False
                    break
            
            if ai_working:
                self.log_result("AI Integration", True, "AI responses working correctly")
                return True
            else:
                self.log_result("AI Integration", False, "AI not providing proper responses")
                return False
        except Exception as e:
            self.log_result("AI Integration", False, f"Error: {str(e)}")
            return False
    
    def test_authentication_required_endpoints(self):
        """Test that protected endpoints require authentication"""
        try:
            # Remove auth header temporarily
            original_headers = self.session.headers.copy()
            if 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']
            
            # Try to access protected endpoint
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            
            # Restore headers
            self.session.headers.update(original_headers)
            
            if response.status_code == 401:
                self.log_result("Authentication Protection", True, "Protected endpoints require auth")
                return True
            else:
                self.log_result("Authentication Protection", False, f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Authentication Protection", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting Baby Steps Backend API Tests")
        print(f"📍 Testing against: {API_BASE}")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return self.results
        
        # Test authentication flow
        if not self.test_user_registration():
            print("❌ Registration failed - stopping auth tests")
        else:
            # Manually verify user for testing
            if self.test_manual_verification():
                self.test_user_login()
                self.test_authentication_required_endpoints()
            else:
                print("❌ Manual verification failed - stopping auth tests")
        
        # Test baby profile management (requires auth)
        if self.auth_token:
            self.test_baby_profile_creation()
            self.test_get_babies()
        
        # Test food research functionality (high priority)
        if self.auth_token:
            self.test_food_research_endpoint()
            self.test_unified_meal_search()
            self.test_food_safety_search()
            self.test_ai_integration()
        
        print("=" * 60)
        print(f"📊 Test Results Summary:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests Details:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        return self.results

def main():
    """Main test execution"""
    tester = BabyStepsAPITester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()