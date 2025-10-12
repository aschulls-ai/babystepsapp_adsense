#!/usr/bin/env python3
"""
Food Research Knowledge Base Fix Testing
URGENT: Test the food research knowledge base fix that removed hardcoded food responses
that were bypassing the knowledge base system.

CRITICAL FIX VERIFICATION:
- Test specific food queries return correct food-specific information instead of defaulting to honey
- Each food query should return information specific to that food
- NO MORE defaulting to honey responses for non-honey queries
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://openai-parent.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class FoodResearchFixTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 60  # Increased for AI responses
        self.auth_token = None
        # Demo credentials as specified in review request
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': [],
            'test_details': []
        }
    
    def log_result(self, test_name, success, message="", response_preview=""):
        """Log test results with detailed information"""
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
            if response_preview:
                print(f"   📝 Response preview: {response_preview[:100]}...")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
            if response_preview:
                print(f"   📝 Response preview: {response_preview[:100]}...")
        
        self.results['test_details'].append({
            'test': test_name,
            'success': success,
            'message': message,
            'response_preview': response_preview
        })
    
    def test_health_check(self):
        """Test API health endpoint"""
        try:
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
    
    def test_demo_user_login(self):
        """Test demo user login as specified in review request"""
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    # Store token for further testing
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Demo User Login", True, "Demo user login successful")
                    return True
                else:
                    self.log_result("Demo User Login", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_result("Demo User Login", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Demo User Login", False, f"Error: {str(e)}")
            return False
    
    def test_food_query(self, query_text, expected_food_keyword, test_name):
        """Test a specific food query and verify it returns food-specific information"""
        try:
            food_query = {
                "question": query_text,
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                answer_lower = answer.lower()
                
                # Check if response contains the expected food keyword
                if expected_food_keyword.lower() in answer_lower and len(answer) > 50:
                    # Additional check: make sure it's not just defaulting to honey
                    if expected_food_keyword.lower() != 'honey':
                        # For non-honey queries, check that honey is not the primary focus
                        honey_mentions = answer_lower.count('honey')
                        food_mentions = answer_lower.count(expected_food_keyword.lower())
                        
                        if food_mentions >= honey_mentions:
                            self.log_result(test_name, True, 
                                          f"Found {expected_food_keyword}-specific answer (not defaulting to honey)", 
                                          answer)
                            return True
                        else:
                            self.log_result(test_name, False, 
                                          f"Response mentions honey more than {expected_food_keyword} - may be defaulting to honey", 
                                          answer)
                            return False
                    else:
                        # For honey queries, it should mention honey
                        self.log_result(test_name, True, 
                                      f"Found honey-specific answer as expected", 
                                      answer)
                        return True
                else:
                    self.log_result(test_name, False, 
                                  f"No {expected_food_keyword}-specific answer found or response too short", 
                                  answer)
                    return False
            else:
                self.log_result(test_name, False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result(test_name, False, f"Error: {str(e)}")
            return False
    
    def run_food_research_fix_tests(self):
        """Run the specific food research fix tests as requested in the review"""
        print(f"🚀 FOOD RESEARCH KNOWLEDGE BASE FIX TESTING")
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Demo user: {self.demo_email}")
        print("=" * 80)
        print("🎯 CRITICAL FIX VERIFICATION:")
        print("   • Test specific food queries return correct food-specific information")
        print("   • Verify NO MORE defaulting to honey responses for non-honey queries")
        print("   • Each food query should return information specific to that food")
        print("=" * 80)
        
        # Test basic connectivity first
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return self.results
        
        # Login with demo user as specified in review request
        print("\n🔐 AUTHENTICATION WITH DEMO CREDENTIALS:")
        print("=" * 50)
        if not self.test_demo_user_login():
            print("❌ Demo login failed - cannot proceed with authenticated tests")
            return self.results
        
        print("\n🥗 FOOD RESEARCH KNOWLEDGE BASE FIX TESTS:")
        print("=" * 50)
        
        # Test the specific food queries mentioned in the review request
        test_cases = [
            {
                "query": "When can babies eat eggs?",
                "expected_keyword": "egg",
                "test_name": "Eggs Query (should NOT return honey)"
            },
            {
                "query": "Is avocado safe for babies?",
                "expected_keyword": "avocado",
                "test_name": "Avocado Query (should NOT return honey)"
            },
            {
                "query": "Can babies eat strawberries?",
                "expected_keyword": "strawberr",
                "test_name": "Strawberries Query (should NOT return honey)"
            },
            {
                "query": "Are peanuts safe for babies?",
                "expected_keyword": "peanut",
                "test_name": "Peanuts Query (should NOT return honey)"
            },
            {
                "query": "Is honey safe for babies?",
                "expected_keyword": "honey",
                "test_name": "Honey Query (should return honey)"
            }
        ]
        
        print(f"🧪 Testing {len(test_cases)} specific food queries...")
        print()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{i}. Testing: '{test_case['query']}'")
            self.test_food_query(
                test_case['query'],
                test_case['expected_keyword'],
                test_case['test_name']
            )
            print()
        
        # Results summary
        print("=" * 80)
        print(f"📊 FOOD RESEARCH FIX TEST RESULTS:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests Details:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Specific analysis for the fix
        print(f"\n🎯 KNOWLEDGE BASE FIX VERIFICATION:")
        print("=" * 50)
        
        non_honey_tests = [detail for detail in self.results['test_details'] 
                          if 'should NOT return honey' in detail['test']]
        honey_test = [detail for detail in self.results['test_details'] 
                     if 'should return honey' in detail['test']]
        
        non_honey_passed = sum(1 for test in non_honey_tests if test['success'])
        
        if non_honey_passed == len(non_honey_tests) and len(non_honey_tests) > 0:
            print("✅ SUCCESS: Non-honey food queries return food-specific information")
            print("   • Eggs query returns egg-specific answer (NOT honey)")
            print("   • Avocado query returns avocado-specific answer (NOT honey)")
            print("   • Strawberries query returns strawberry-specific answer (NOT honey)")
            print("   • Peanuts query returns peanut-specific answer (NOT honey)")
        else:
            print("❌ ISSUE: Some non-honey queries may still be defaulting to honey")
            for test in non_honey_tests:
                if not test['success']:
                    print(f"   • {test['test']}: {test['message']}")
        
        if honey_test and honey_test[0]['success']:
            print("✅ SUCCESS: Honey query correctly returns honey-specific information")
        elif honey_test:
            print("❌ ISSUE: Honey query not working correctly")
            print(f"   • {honey_test[0]['message']}")
        
        # Overall fix assessment
        if self.results['failed'] == 0:
            print(f"\n🎉 KNOWLEDGE BASE FIX VERIFICATION: SUCCESSFUL")
            print("   • All food queries return food-specific information")
            print("   • No more defaulting to honey for non-honey queries")
            print("   • Knowledge base properly matches food names to correct entries")
        else:
            print(f"\n⚠️  KNOWLEDGE BASE FIX VERIFICATION: ISSUES FOUND")
            print("   • Some food queries may still have issues")
            print("   • Review failed tests above for details")
        
        return self.results

def main():
    """Main test execution"""
    tester = FoodResearchFixTester()
    results = tester.run_food_research_fix_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()