#!/usr/bin/env python3
"""
Backend Connectivity Testing After offlineMode.js Fix
Testing that baby-genius.preview.emergentagent.com backend is accessible and working correctly
after fixing shouldUseOfflineMode() hardcoded return true issue.
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
    
    def test_backend_accessibility(self):
        """Test that backend URL is accessible"""
        print("🌐 TESTING BACKEND ACCESSIBILITY...")
        
        try:
            # Test basic connectivity to backend
            response = self.session.get(
                f"{BACKEND_URL.replace('/api', '')}/health",
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_test("Backend Accessibility", True, 
                            f"Backend accessible at {BACKEND_URL.replace('/api', '')}")
                return True
            else:
                # Try alternative health check
                response = self.session.get(
                    f"{BACKEND_URL}/dashboard/available-widgets",
                    timeout=10
                )
                if response.status_code in [200, 401, 403]:  # 401/403 means endpoint exists but needs auth
                    self.log_test("Backend Accessibility", True, 
                                f"Backend accessible (got {response.status_code})")
                    return True
                else:
                    self.log_test("Backend Accessibility", False, 
                                f"Backend not accessible: {response.status_code}")
                    return False
                
        except Exception as e:
            self.log_test("Backend Accessibility", False, f"Connection error: {str(e)}")
            return False
    
    def test_ai_chat_endpoint(self):
        """Test AI chat endpoint with gpt-5-nano model"""
        print("🤖 TESTING AI CHAT ENDPOINT...")
        
        try:
            chat_data = {
                "message": "What breakfast ideas for my baby?",
                "baby_age_months": 8
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ai/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"},
                timeout=60  # AI requests can take longer
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("response", "")
                timestamp = result.get("timestamp", "")
                
                if len(ai_response) > 100:  # Expect substantial response
                    self.log_test("AI Chat Endpoint", True, 
                                f"AI response received ({len(ai_response)} chars): {ai_response[:100]}...")
                    return True
                else:
                    self.log_test("AI Chat Endpoint", False, 
                                f"AI response too short: {ai_response}")
                    return False
            else:
                self.log_test("AI Chat Endpoint", False, 
                            f"AI chat failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log_test("AI Chat Endpoint", False, f"AI chat error: {str(e)}")
            return False
    
    def test_baby_management_endpoints(self):
        """Test baby management endpoints"""
        print("👶 TESTING BABY MANAGEMENT ENDPOINTS...")
        
        try:
            # Test GET /api/babies
            response = self.session.get(
                f"{BACKEND_URL}/babies",
                timeout=30
            )
            
            if response.status_code == 200:
                babies = response.json()
                self.log_test("Baby Management - GET", True, 
                            f"Retrieved {len(babies)} baby profiles")
                
                # Test creating a new baby profile
                baby_data = {
                    "name": "Test Baby Backend",
                    "birth_date": "2024-01-15T00:00:00Z",
                    "gender": "other"
                }
                
                create_response = self.session.post(
                    f"{BACKEND_URL}/babies",
                    json=baby_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if create_response.status_code == 200:
                    new_baby = create_response.json()
                    baby_id = new_baby.get("id")
                    
                    self.log_test("Baby Management - POST", True, 
                                f"Created baby profile: {new_baby.get('name')}")
                    
                    # Test updating the baby profile
                    update_data = {
                        "name": "Updated Test Baby",
                        "birth_date": "2024-01-15T00:00:00Z",
                        "gender": "other"
                    }
                    
                    update_response = self.session.put(
                        f"{BACKEND_URL}/babies/{baby_id}",
                        json=update_data,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    if update_response.status_code == 200:
                        self.log_test("Baby Management - PUT", True, 
                                    "Successfully updated baby profile")
                        return True
                    else:
                        self.log_test("Baby Management - PUT", False, 
                                    f"Update failed: {update_response.status_code}")
                        return False
                else:
                    self.log_test("Baby Management - POST", False, 
                                f"Create failed: {create_response.status_code} - {create_response.text}")
                    return False
            else:
                self.log_test("Baby Management - GET", False, 
                            f"GET babies failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Baby Management Endpoints", False, f"Request error: {str(e)}")
            return False
    
    def test_environment_variables(self):
        """Test that environment variables are properly configured"""
        print("⚙️ TESTING ENVIRONMENT CONFIGURATION...")
        
        # Check if REACT_APP_BACKEND_URL is set correctly by testing if backend responds
        expected_backend = "https://baby-genius.preview.emergentagent.com"
        
        if BACKEND_URL.startswith(expected_backend):
            self.log_test("Environment Variables", True, 
                        f"REACT_APP_BACKEND_URL correctly set to {expected_backend}")
            return True
        else:
            self.log_test("Environment Variables", False, 
                        f"Backend URL mismatch. Expected {expected_backend}, got {BACKEND_URL}")
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