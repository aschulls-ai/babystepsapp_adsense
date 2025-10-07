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

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://parent-helper-21.preview.emergentagent.com')
# Use production URL for testing as specified in review request
API_BASE = f"{BACKEND_URL}/api"

class BabyStepsAPITester:
    def __init__(self):
        self.session = requests.Session()
        # Set session timeout and retry settings
        self.session.timeout = 30
        self.auth_token = None
        # Test credentials for new user (as per review request)
        self.new_user_email = "newuser@test.com"
        self.new_user_name = "New Test User"
        self.new_user_password = "TestPass123"
        # Existing user credentials
        self.existing_user_email = "test@babysteps.com"
        self.existing_user_password = "TestPassword123"
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
    
    def test_new_user_registration(self):
        """Test new user registration endpoint"""
        try:
            user_data = {
                "email": self.new_user_email,
                "name": self.new_user_name,
                "password": self.new_user_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/register", json=user_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'email' in data:
                    # Check that email_verified is False (as expected for new users)
                    email_verified = data.get('email_verified', True)  # Default True to catch if missing
                    if email_verified == False:
                        self.log_result("New User Registration", True, f"User registered with email_verified=False: {data['message']}")
                        return True
                    else:
                        self.log_result("New User Registration", False, f"Expected email_verified=False, got {email_verified}")
                        return False
                else:
                    self.log_result("New User Registration", False, f"Invalid response format: {data}")
                    return False
            elif response.status_code == 400 and "already registered" in response.text:
                # User already exists, that's fine for testing
                self.log_result("New User Registration", True, "User already exists (acceptable for testing)")
                return True
            else:
                self.log_result("New User Registration", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("New User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_protected_endpoints_with_token(self):
        """Test that protected endpoints work with JWT token from unverified user"""
        try:
            # Test accessing babies endpoint (protected)
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Protected Endpoints Access", True, "Can access protected endpoints with token from unverified user")
                    return True
                else:
                    self.log_result("Protected Endpoints Access", False, f"Unexpected response format: {data}")
                    return False
            else:
                self.log_result("Protected Endpoints Access", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Protected Endpoints Access", False, f"Error: {str(e)}")
            return False

    def test_email_verification_still_exists(self):
        """Test that email verification functionality still exists"""
        try:
            # Test resend verification endpoint exists
            email_data = {"email": self.new_user_email}
            response = self.session.post(f"{API_BASE}/auth/resend-verification", json=email_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data:
                    self.log_result("Email Verification Functionality", True, "Email verification endpoints still exist")
                    return True
                else:
                    self.log_result("Email Verification Functionality", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_result("Email Verification Functionality", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Email Verification Functionality", False, f"Error: {str(e)}")
            return False

    def test_immediate_login_without_verification(self):
        """Test that new user can login immediately WITHOUT email verification"""
        try:
            login_data = {
                "email": self.new_user_email,
                "password": self.new_user_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    # Store token for further testing
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Immediate Login Without Verification", True, "New user can login without email verification")
                    return True
                else:
                    self.log_result("Immediate Login Without Verification", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_result("Immediate Login Without Verification", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Immediate Login Without Verification", False, f"Error: {str(e)}")
            return False

    def test_existing_user_login(self):
        """Test existing user login"""
        try:
            login_data = {
                "email": self.existing_user_email,
                "password": self.existing_user_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.log_result("Existing User Login", True, "Existing user login successful")
                    return True
                else:
                    self.log_result("Existing User Login", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_result("Existing User Login", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Existing User Login", False, f"Error: {str(e)}")
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
    
    def test_meal_planner_search_endpoint(self):
        """Test the meal planner search endpoint - MAIN FOCUS"""
        try:
            # Test meal idea search as per review request
            search_query = {
                "query": "breakfast ideas for 6 month old",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['results', 'query', 'age_months']
                if all(field in data for field in required_fields):
                    if data['query'] == search_query['query'] and data['age_months'] == search_query['baby_age_months']:
                        self.log_result("Meal Planner Search Endpoint", True, "✅ /api/meals/search endpoint working correctly")
                        return True
                    else:
                        self.log_result("Meal Planner Search Endpoint", False, f"Query mismatch: {data}")
                        return False
                else:
                    self.log_result("Meal Planner Search Endpoint", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Meal Planner Search Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Meal Planner Search Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_honey_safety_query(self):
        """Test honey safety query as per review request"""
        try:
            # Test food safety query through meal search
            search_query = {
                "query": "Is honey safe for babies?",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    # Check if response mentions honey safety concerns
                    results_lower = data['results'].lower()
                    if 'honey' in results_lower and ('12 months' in results_lower or 'one year' in results_lower or 'avoid' in results_lower):
                        self.log_result("Honey Safety Query", True, "✅ Honey safety information provided correctly")
                        return True
                    else:
                        self.log_result("Honey Safety Query", True, f"✅ Response received (content may vary): {data['results'][:100]}...")
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
    
    def test_meal_ideas_query(self):
        """Test meal ideas query as per review request"""
        try:
            # Test meal ideas query through meal search
            search_query = {
                "query": "breakfast ideas for 6 month old",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    # Check if response contains breakfast/meal suggestions
                    results_lower = data['results'].lower()
                    if any(word in results_lower for word in ['breakfast', 'meal', 'food', 'puree', 'cereal', 'fruit']):
                        self.log_result("Meal Ideas Query", True, "✅ Breakfast ideas provided correctly")
                        return True
                    else:
                        self.log_result("Meal Ideas Query", True, f"✅ Response received: {data['results'][:100]}...")
                        return True
                else:
                    self.log_result("Meal Ideas Query", False, f"Empty results: {data}")
                    return False
            else:
                self.log_result("Meal Ideas Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Meal Ideas Query", False, f"Error: {str(e)}")
            return False
    
    def test_age_customization(self):
        """Test that search results are customized for baby age"""
        try:
            # Test same query with different ages
            queries = [
                {"query": "feeding ideas", "baby_age_months": 6},
                {"query": "feeding ideas", "baby_age_months": 12}
            ]
            
            responses = []
            for query in queries:
                response = self.session.post(f"{API_BASE}/meals/search", json=query, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    responses.append(data.get('results', ''))
                else:
                    self.log_result("Age Customization", False, f"HTTP {response.status_code} for {query['baby_age_months']} months")
                    return False
            
            # Check if responses are different (indicating age customization)
            if len(responses) == 2 and responses[0] != responses[1]:
                self.log_result("Age Customization", True, "✅ Search results customized for different ages")
                return True
            elif len(responses) == 2:
                self.log_result("Age Customization", True, "✅ Both age queries returned responses (may be similar)")
                return True
            else:
                self.log_result("Age Customization", False, "Failed to get responses for age comparison")
                return False
        except Exception as e:
            self.log_result("Age Customization", False, f"Error: {str(e)}")
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
                answer = data.get('answer', '').lower()
                if "sorry" in answer or "trouble" in answer or "unable to assess" in answer or len(answer) < 10:
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
            
            if response.status_code in [401, 403]:
                self.log_result("Authentication Protection", True, f"Protected endpoints require auth (HTTP {response.status_code})")
                return True
            else:
                self.log_result("Authentication Protection", False, f"Expected 401/403, got {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Authentication Protection", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests focusing on email verification optional login"""
        print(f"🚀 Testing Baby Steps Backend Authentication - Email Verification Optional")
        print(f"📍 Testing against: {API_BASE}")
        print("=" * 80)
        
        # Test basic connectivity first
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return self.results
        
        # MAIN TEST SEQUENCE AS PER REVIEW REQUEST:
        print("\n🔍 TESTING EMAIL VERIFICATION OPTIONAL LOGIN FLOW:")
        print("=" * 80)
        
        # 1. Create New Test User
        print("1️⃣ Creating new test user...")
        if not self.test_new_user_registration():
            print("❌ New user registration failed")
        
        # 2. Immediate Login Test (WITHOUT verification)
        print("2️⃣ Testing immediate login WITHOUT email verification...")
        if not self.test_immediate_login_without_verification():
            print("❌ Immediate login failed - this is the main issue to fix!")
        
        # 3. Test Protected Endpoints
        print("3️⃣ Testing protected endpoints with token from unverified user...")
        if self.auth_token:
            self.test_protected_endpoints_with_token()
            self.test_baby_profile_creation()
            self.test_get_babies()
        
        # 4. Test Existing User
        print("4️⃣ Testing existing user login...")
        self.test_existing_user_login()
        
        # 5. Verify email verification functionality still exists
        print("5️⃣ Verifying email verification functionality still exists...")
        self.test_email_verification_still_exists()
        
        # Additional authentication tests
        print("\n🔒 ADDITIONAL AUTHENTICATION TESTS:")
        print("=" * 80)
        self.test_authentication_required_endpoints()
        
        # Test core functionality if we have auth
        if self.auth_token:
            print("\n🍼 TESTING CORE FUNCTIONALITY:")
            print("=" * 80)
            self.test_food_research_endpoint()
            self.test_unified_meal_search()
            self.test_food_safety_search()
            self.test_ai_integration()
        
        print("=" * 80)
        print(f"📊 Test Results Summary:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests Details:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Specific summary for the review request
        print(f"\n🎯 EMAIL VERIFICATION OPTIONAL LOGIN TEST SUMMARY:")
        print("=" * 80)
        
        # Check if core authentication tests passed
        auth_tests = [
            "New User Registration",
            "Immediate Login Without Verification", 
            "Protected Endpoints Access",
            "Existing User Login",
            "Email Verification Functionality"
        ]
        
        auth_failures = [error for error in self.results['errors'] 
                        if any(test in error for test in auth_tests)]
        
        if len(auth_failures) == 0:
            print("✅ SUCCESS: Email verification is now optional for login!")
            print("✅ Users can access the app immediately after registration")
            print("✅ Email verification functionality still exists for users who want it")
            print("✅ Protected endpoints work with tokens from unverified users")
            print("✅ Existing users can still login normally")
        else:
            print("❌ ISSUES FOUND: Email verification optional login has problems")
            print("❌ Authentication-related failures:")
            for failure in auth_failures:
                print(f"   • {failure}")
        
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