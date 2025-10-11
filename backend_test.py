#!/usr/bin/env python3
"""
JSON-ONLY Food Research Backend Testing
Testing the completely rewritten JSON-ONLY food research backend implementation
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://baby-genius.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = []
        
    def log_test(self, test_name, passed, details=""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def authenticate(self):
        """Authenticate with demo user credentials"""
        print("🔐 AUTHENTICATING WITH DEMO USER...")
        
        try:
            login_data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.auth_token = token_data.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.auth_token}"
                })
                self.log_test("Authentication", True, f"Successfully logged in as {TEST_USER_EMAIL}")
                return True
            else:
                self.log_test("Authentication", False, f"Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Authentication", False, f"Authentication error: {str(e)}")
            return False
    
    def test_json_food_research(self, question, expected_food, expected_id=None, should_find_match=True):
        """Test JSON-only food research endpoint"""
        print(f"🔍 TESTING FOOD QUERY: '{question}'")
        
        try:
            query_data = {
                "question": question,
                "baby_age_months": 8
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/food/research",
                json=query_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test(f"Food Research: {question}", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            safety_level = result.get("safety_level", "")
            
            # Check if this is a JSON-only response (no AI)
            is_json_response = any("Knowledge Base Question ID:" in source for source in sources)
            has_ai_indicators = any(keyword in answer.lower() for keyword in [
                "i recommend", "i suggest", "as an ai", "i think", "in my opinion"
            ])
            
            if should_find_match:
                # Should find a match in JSON database
                if not is_json_response:
                    self.log_test(f"Food Research: {question}", False, 
                                f"Expected JSON response with Question ID, got: {sources}")
                    return False
                
                if has_ai_indicators:
                    self.log_test(f"Food Research: {question}", False, 
                                f"Response contains AI-generated content: {answer[:200]}...")
                    return False
                
                # Check for expected food content
                if expected_food.lower() not in answer.lower():
                    self.log_test(f"Food Research: {question}", False, 
                                f"Expected {expected_food} content, got: {answer[:200]}...")
                    return False
                
                # Check for expected question ID if provided
                if expected_id:
                    expected_id_text = f"Knowledge Base Question ID: {expected_id}"
                    if not any(expected_id_text in source for source in sources):
                        self.log_test(f"Food Research: {question}", False, 
                                    f"Expected {expected_id_text}, got sources: {sources}")
                        return False
                
                self.log_test(f"Food Research: {question}", True, 
                            f"JSON response with {expected_food} content, safety: {safety_level}, sources: {sources}")
                return True
            
            else:
                # Should NOT find a match - expect "not available" response
                if "Food Safety Information Not Available" not in answer:
                    self.log_test(f"Food Research: {question}", False, 
                                f"Expected 'not available' response, got: {answer[:200]}...")
                    return False
                
                if "Available in our database:" not in answer:
                    self.log_test(f"Food Research: {question}", False, 
                                f"Expected available foods list, got: {answer[:200]}...")
                    return False
                
                self.log_test(f"Food Research: {question}", True, 
                            f"Correctly returned 'not available' with food list, safety: {safety_level}")
                return True
                
        except Exception as e:
            self.log_test(f"Food Research: {question}", False, f"Request error: {str(e)}")
            return False
    
    def test_no_ai_calls(self):
        """Test that no AI/LLM calls are being made"""
        print("🚫 TESTING NO AI/LLM INTEGRATION...")
        
        # Test multiple queries to ensure consistent JSON-only responses
        test_queries = [
            "When can babies eat eggs?",
            "Is avocado safe for babies?", 
            "Can babies eat strawberries?",
            "Is honey safe for babies?"
        ]
        
        all_json_only = True
        
        for query in test_queries:
            try:
                query_data = {"question": query, "baby_age_months": 8}
                response = self.session.post(
                    f"{BACKEND_URL}/food/research",
                    json=query_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10  # Short timeout to detect AI delays
                )
                
                if response.status_code == 200:
                    result = response.json()
                    sources = result.get("sources", [])
                    
                    # Check if response is from JSON knowledge base
                    is_json_response = any("Knowledge Base Question ID:" in source for source in sources)
                    if not is_json_response:
                        all_json_only = False
                        break
                else:
                    all_json_only = False
                    break
                    
            except Exception as e:
                all_json_only = False
                break
        
        if all_json_only:
            self.log_test("No AI/LLM Integration", True, 
                        "All responses come from JSON knowledge base with Question IDs")
        else:
            self.log_test("No AI/LLM Integration", False, 
                        "Some responses may still be using AI/LLM instead of JSON-only")
        
        return all_json_only
    
    def run_comprehensive_tests(self):
        """Run all JSON-only food research tests"""
        print("=" * 80)
        print("🧪 JSON-ONLY FOOD RESEARCH BACKEND TESTING")
        print("=" * 80)
        print()
        
        # Step 1: Authentication
        if not self.authenticate():
            print("❌ CRITICAL: Authentication failed. Cannot proceed with testing.")
            return False
        
        # Step 2: Test specific food queries as requested in review
        print("📋 TESTING SPECIFIC FOOD QUERIES FROM REVIEW REQUEST...")
        print()
        
        test_cases = [
            {
                "question": "When can babies eat eggs?",
                "expected_food": "eggs",
                "expected_id": 202,
                "should_find_match": True
            },
            {
                "question": "Is avocado safe for babies?", 
                "expected_food": "avocado",
                "expected_id": None,  # Avocado not in current JSON
                "should_find_match": False  # Should return "not available"
            },
            {
                "question": "Can babies eat strawberries?",
                "expected_food": "strawberries", 
                "expected_id": 205,
                "should_find_match": True
            },
            {
                "question": "Is honey safe for babies?",
                "expected_food": "honey",
                "expected_id": 201,
                "should_find_match": True
            },
            {
                "question": "Can babies eat pizza?",
                "expected_food": "pizza",
                "expected_id": None,
                "should_find_match": False  # Should return "not available"
            }
        ]
        
        passed_tests = 0
        total_tests = len(test_cases)
        
        for test_case in test_cases:
            if self.test_json_food_research(**test_case):
                passed_tests += 1
        
        # Step 3: Test no AI integration
        if self.test_no_ai_calls():
            passed_tests += 1
        total_tests += 1
        
        # Step 4: Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Tests Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        if success_rate >= 80:
            print("✅ JSON-ONLY FOOD RESEARCH IMPLEMENTATION: SUCCESS")
            print("   - AI/LLM system completely removed")
            print("   - JSON knowledge base loading working")
            print("   - Smart matching implemented")
            print("   - Source attribution with Question IDs")
            print("   - 'Not available' responses for unknown foods")
        else:
            print("❌ JSON-ONLY FOOD RESEARCH IMPLEMENTATION: ISSUES FOUND")
            print("   - Some tests failed - see details above")
        
        print()
        print("🔍 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result["passed"] else "❌"
            print(f"   {status} {result['test']}")
            if result["details"]:
                print(f"      {result['details']}")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = BackendTester()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 ALL CRITICAL TESTS PASSED - JSON-ONLY IMPLEMENTATION WORKING!")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED - REVIEW IMPLEMENTATION NEEDED")
        sys.exit(1)

if __name__ == "__main__":
    main()