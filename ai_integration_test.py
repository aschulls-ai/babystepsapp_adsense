#!/usr/bin/env python3
"""
AI Integration Testing Suite for Baby Steps App
Tests AI endpoints with emergentintegrations as requested in review
"""

import requests
import json
import time
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

class AIIntegrationTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 60  # AI responses can take up to 60 seconds
        self.auth_token = None
        # Demo user credentials as specified in review request
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
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
    
    def test_backend_health(self):
        """Test backend is running"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Backend Health Check", True, f"Backend running: {data.get('service', 'Unknown')}")
                return True
            else:
                self.log_result("Backend Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Backend Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_demo_user_authentication(self):
        """Test authentication with demo user credentials"""
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Demo User Authentication", True, f"Login successful for {self.demo_email}")
                    return True
                else:
                    self.log_result("Demo User Authentication", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_result("Demo User Authentication", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Demo User Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_food_research_endpoint(self):
        """Test /api/food/research with emergentintegrations"""
        try:
            # Test honey safety query as specified in review
            food_query = {
                "question": "Is honey safe for babies?",
                "baby_age_months": 8
            }
            
            print(f"🍯 Testing food safety query: '{food_query['question']}'")
            start_time = time.time()
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
            
            response_time = time.time() - start_time
            print(f"⏱️ Response time: {response_time:.2f} seconds")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['answer', 'safety_level', 'sources']
                
                if all(field in data for field in required_fields):
                    # Check if safety level is appropriate for honey
                    safety_level = data['safety_level']
                    answer = data['answer'].lower()
                    
                    # Honey should be marked as avoid or caution for babies under 12 months
                    if safety_level in ['avoid', 'caution', 'consult_doctor']:
                        self.log_result("Food Research - Honey Safety", True, 
                                      f"Correct safety assessment: {safety_level}")
                    else:
                        self.log_result("Food Research - Honey Safety", False, 
                                      f"Unexpected safety level for honey: {safety_level}")
                    
                    # Check response quality
                    if len(data['answer']) > 50 and 'honey' in answer:
                        self.log_result("Food Research - Response Quality", True, 
                                      f"Comprehensive response ({len(data['answer'])} chars)")
                    else:
                        self.log_result("Food Research - Response Quality", False, 
                                      "Response too short or doesn't mention honey")
                    
                    # Check response time
                    if response_time < 60:
                        self.log_result("Food Research - Response Time", True, 
                                      f"Response within 60 seconds ({response_time:.2f}s)")
                    else:
                        self.log_result("Food Research - Response Time", False, 
                                      f"Response too slow ({response_time:.2f}s)")
                    
                    return True
                else:
                    self.log_result("Food Research Endpoint", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Food Research Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Food Research Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_meals_search_endpoint(self):
        """Test /api/meals/search for meal planning functionality"""
        try:
            # Test breakfast ideas query as specified in review
            search_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            print(f"🥣 Testing meal planning query: '{search_query['query']}'")
            start_time = time.time()
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            response_time = time.time() - start_time
            print(f"⏱️ Response time: {response_time:.2f} seconds")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['results', 'query', 'age_months']
                
                if all(field in data for field in required_fields):
                    # Check query echo
                    if data['query'] == search_query['query'] and data['age_months'] == search_query['baby_age_months']:
                        self.log_result("Meals Search - Query Echo", True, "Query parameters correctly echoed")
                    else:
                        self.log_result("Meals Search - Query Echo", False, "Query parameters not echoed correctly")
                    
                    # Check response quality
                    results = data['results']
                    if len(results) > 100 and any(word in results.lower() for word in ['breakfast', 'meal', 'food', 'baby']):
                        self.log_result("Meals Search - Response Quality", True, 
                                      f"Age-appropriate meal suggestions provided ({len(results)} chars)")
                    else:
                        self.log_result("Meals Search - Response Quality", False, 
                                      "Response too short or not meal-related")
                    
                    # Check response time
                    if response_time < 60:
                        self.log_result("Meals Search - Response Time", True, 
                                      f"Response within 60 seconds ({response_time:.2f}s)")
                    else:
                        self.log_result("Meals Search - Response Time", False, 
                                      f"Response too slow ({response_time:.2f}s)")
                    
                    return True
                else:
                    self.log_result("Meals Search Endpoint", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Meals Search Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Meals Search Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_research_endpoint(self):
        """Test /api/research for general parenting questions"""
        try:
            # Test sleep schedule query as specified in review
            research_query = {
                "question": "sleep schedule for 6 month old"
            }
            
            print(f"💤 Testing general research query: '{research_query['question']}'")
            start_time = time.time()
            
            response = self.session.post(f"{API_BASE}/research", json=research_query, timeout=60)
            
            response_time = time.time() - start_time
            print(f"⏱️ Response time: {response_time:.2f} seconds")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['answer', 'sources']
                
                if all(field in data for field in required_fields):
                    # Check response quality
                    answer = data['answer']
                    if len(answer) > 100 and any(word in answer.lower() for word in ['sleep', 'schedule', 'baby', 'month']):
                        self.log_result("Research - Response Quality", True, 
                                      f"Helpful sleep advice provided ({len(answer)} chars)")
                    else:
                        self.log_result("Research - Response Quality", False, 
                                      "Response too short or not sleep-related")
                    
                    # Check sources provided
                    sources = data['sources']
                    if isinstance(sources, list) and len(sources) > 0:
                        self.log_result("Research - Sources Provided", True, 
                                      f"{len(sources)} sources provided")
                    else:
                        self.log_result("Research - Sources Provided", False, 
                                      "No sources provided")
                    
                    # Check response time
                    if response_time < 60:
                        self.log_result("Research - Response Time", True, 
                                      f"Response within 60 seconds ({response_time:.2f}s)")
                    else:
                        self.log_result("Research - Response Time", False, 
                                      f"Response too slow ({response_time:.2f}s)")
                    
                    return True
                else:
                    self.log_result("Research Endpoint", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_result("Research Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Research Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_ai_endpoints_require_authentication(self):
        """Test that AI endpoints require proper authentication"""
        try:
            # Remove auth header temporarily
            original_headers = self.session.headers.copy()
            if 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']
            
            ai_endpoints = [
                ("/food/research", {"question": "test", "baby_age_months": 6}),
                ("/meals/search", {"query": "test", "baby_age_months": 6}),
                ("/research", {"question": "test"})
            ]
            
            all_protected = True
            for endpoint, test_data in ai_endpoints:
                response = self.session.post(f"{API_BASE}{endpoint}", json=test_data, timeout=10)
                if response.status_code not in [401, 403]:
                    print(f"❌ {endpoint} not properly protected: HTTP {response.status_code}")
                    all_protected = False
                else:
                    print(f"✅ {endpoint} properly protected: HTTP {response.status_code}")
            
            # Restore headers
            self.session.headers.update(original_headers)
            
            if all_protected:
                self.log_result("AI Endpoints Authentication", True, "All AI endpoints require authentication")
                return True
            else:
                self.log_result("AI Endpoints Authentication", False, "Some AI endpoints not protected")
                return False
        except Exception as e:
            self.log_result("AI Endpoints Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_emergentintegrations_configuration(self):
        """Test that emergentintegrations is properly configured"""
        try:
            # Test multiple AI queries to verify emergentintegrations is working
            test_queries = [
                {"endpoint": "/food/research", "data": {"question": "Is banana safe for babies?", "baby_age_months": 6}},
                {"endpoint": "/meals/search", "data": {"query": "lunch ideas for toddler", "baby_age_months": 15}},
                {"endpoint": "/research", "data": {"question": "when do babies start walking?"}}
            ]
            
            successful_queries = 0
            for query in test_queries:
                try:
                    response = self.session.post(f"{API_BASE}{query['endpoint']}", json=query['data'], timeout=60)
                    if response.status_code == 200:
                        data = response.json()
                        # Check if we get a real AI response (not error message)
                        if query['endpoint'] == '/food/research':
                            answer = data.get('answer', '').lower()
                        elif query['endpoint'] == '/meals/search':
                            answer = data.get('results', '').lower()
                        else:  # research
                            answer = data.get('answer', '').lower()
                        
                        # Check if response looks like AI-generated content
                        if len(answer) > 50 and not any(error_word in answer for error_word in 
                                                       ['sorry', 'trouble', 'unable', 'error', 'unavailable']):
                            successful_queries += 1
                            print(f"✅ {query['endpoint']}: AI response received")
                        else:
                            print(f"❌ {query['endpoint']}: Error response or too short")
                    else:
                        print(f"❌ {query['endpoint']}: HTTP {response.status_code}")
                except Exception as e:
                    print(f"❌ {query['endpoint']}: Exception - {str(e)}")
            
            if successful_queries == len(test_queries):
                self.log_result("Emergentintegrations Configuration", True, 
                              f"All {successful_queries} AI endpoints working with emergentintegrations")
                return True
            elif successful_queries > 0:
                self.log_result("Emergentintegrations Configuration", False, 
                              f"Only {successful_queries}/{len(test_queries)} AI endpoints working")
                return False
            else:
                self.log_result("Emergentintegrations Configuration", False, 
                              "No AI endpoints working - emergentintegrations may not be configured")
                return False
        except Exception as e:
            self.log_result("Emergentintegrations Configuration", False, f"Error: {str(e)}")
            return False
    
    def run_ai_integration_tests(self):
        """Run comprehensive AI integration testing as requested in review"""
        print("🤖 AI INTEGRATION TESTING FOR BABY STEPS APP")
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Demo user: {self.demo_email}")
        print("=" * 80)
        
        # 1. Test backend connectivity
        print("\n🏥 1. BACKEND CONNECTIVITY:")
        print("=" * 50)
        if not self.test_backend_health():
            print("❌ Backend not accessible - stopping tests")
            return self.results
        
        # 2. Test authentication with demo user
        print("\n🔐 2. AUTHENTICATION & AI INTEGRATION:")
        print("=" * 50)
        if not self.test_demo_user_authentication():
            print("❌ Demo user authentication failed - stopping tests")
            return self.results
        
        # Test AI endpoints require authentication
        self.test_ai_endpoints_require_authentication()
        
        # 3. Test specific AI query functionality as requested
        print("\n🧠 3. SPECIFIC AI QUERY TESTING:")
        print("=" * 50)
        
        # Food Safety: "Is honey safe for babies?" - should return avoid recommendation
        self.test_food_research_endpoint()
        
        # Meal Planning: "breakfast ideas for 8 month old" - should provide age-appropriate meals
        self.test_meals_search_endpoint()
        
        # General Research: "sleep schedule for 6 month old" - should provide helpful advice
        self.test_research_endpoint()
        
        # 4. Test emergentintegrations configuration
        print("\n⚙️ 4. EMERGENTINTEGRATIONS VERIFICATION:")
        print("=" * 50)
        self.test_emergentintegrations_configuration()
        
        # 5. Summary
        print("\n📊 AI INTEGRATION TEST RESULTS:")
        print("=" * 50)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests Details:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Specific review request summary
        print(f"\n🎯 REVIEW REQUEST VERIFICATION:")
        print("=" * 50)
        
        ai_endpoint_tests = [error for error in self.results['errors'] 
                           if any(test in error for test in ["Food Research", "Meals Search", "Research Endpoint"])]
        
        if len(ai_endpoint_tests) == 0:
            print("✅ AI ENDPOINTS VERIFICATION: All tests passed")
            print("   • /api/food/research working with emergentintegrations")
            print("   • /api/meals/search working for meal planning")
            print("   • /api/research working for general parenting questions")
        else:
            print("❌ AI ENDPOINTS VERIFICATION: Issues found")
            for test in ai_endpoint_tests:
                print(f"   • {test}")
        
        auth_tests = [error for error in self.results['errors'] 
                     if "Authentication" in error]
        
        if len(auth_tests) == 0:
            print("✅ AUTHENTICATION & AI INTEGRATION: Working correctly")
            print("   • Demo user credentials working")
            print("   • AI endpoints require proper authentication")
        else:
            print("❌ AUTHENTICATION & AI INTEGRATION: Issues found")
            for test in auth_tests:
                print(f"   • {test}")
        
        config_tests = [error for error in self.results['errors'] 
                       if "Emergentintegrations" in error]
        
        if len(config_tests) == 0:
            print("✅ EMERGENTINTEGRATIONS SETUP: Working correctly")
            print("   • All AI responses comprehensive and helpful")
            print("   • Response times reasonable (under 60 seconds)")
            print("   • Proper JSON response structure")
        else:
            print("❌ EMERGENTINTEGRATIONS SETUP: Issues found")
            for test in config_tests:
                print(f"   • {test}")
        
        return self.results

def main():
    """Main test execution"""
    tester = AIIntegrationTester()
    results = tester.run_ai_integration_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()