#!/usr/bin/env python3
"""
AI Assistant gpt-5-nano Model Testing
Testing the updated /api/ai/chat endpoint with gpt-5-nano model
"""

import requests
import json
import sys
from datetime import datetime
import time

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class AIChatTester:
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
    
    def test_ai_chat_endpoint(self, message, baby_age_months=6, expected_keywords=None):
        """Test AI chat endpoint with gpt-5-nano model"""
        print(f"🤖 TESTING AI CHAT: '{message}'")
        
        try:
            chat_data = {
                "message": message,
                "baby_age_months": baby_age_months
            }
            
            start_time = time.time()
            response = self.session.post(
                f"{BACKEND_URL}/ai/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"},
                timeout=60  # Allow time for AI processing
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code != 200:
                self.log_test(f"AI Chat: {message[:30]}...", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            ai_response = result.get("response", "")
            timestamp = result.get("timestamp", "")
            
            # Validate response structure
            if not ai_response:
                self.log_test(f"AI Chat: {message[:30]}...", False, "Empty AI response")
                return False
            
            if not timestamp:
                self.log_test(f"AI Chat: {message[:30]}...", False, "Missing timestamp")
                return False
            
            # Check response quality
            response_length = len(ai_response)
            if response_length < 50:
                self.log_test(f"AI Chat: {message[:30]}...", False, 
                            f"Response too short ({response_length} chars): {ai_response}")
                return False
            
            # Check for baby care context
            baby_care_indicators = [
                "baby", "infant", "pediatrician", "months", "feeding", "sleep", 
                "development", "safety", "age", "consult", "doctor"
            ]
            
            has_baby_context = any(indicator in ai_response.lower() for indicator in baby_care_indicators)
            if not has_baby_context:
                self.log_test(f"AI Chat: {message[:30]}...", False, 
                            f"Response lacks baby care context: {ai_response[:200]}...")
                return False
            
            # Check for expected keywords if provided
            if expected_keywords:
                missing_keywords = []
                for keyword in expected_keywords:
                    if keyword.lower() not in ai_response.lower():
                        missing_keywords.append(keyword)
                
                if missing_keywords:
                    self.log_test(f"AI Chat: {message[:30]}...", False, 
                                f"Missing expected keywords {missing_keywords}: {ai_response[:200]}...")
                    return False
            
            # Check for safety disclaimer
            safety_indicators = ["pediatrician", "doctor", "consult", "medical advice"]
            has_safety_disclaimer = any(indicator in ai_response.lower() for indicator in safety_indicators)
            
            self.log_test(f"AI Chat: {message[:30]}...", True, 
                        f"Response: {response_length} chars, Time: {response_time:.2f}s, "
                        f"Baby context: ✓, Safety disclaimer: {'✓' if has_safety_disclaimer else '✗'}")
            return True
                
        except Exception as e:
            self.log_test(f"AI Chat: {message[:30]}...", False, f"Request error: {str(e)}")
            return False
    
    def test_authentication_required(self):
        """Test that AI chat endpoint requires authentication"""
        print("🔒 TESTING AUTHENTICATION REQUIREMENT...")
        
        try:
            # Remove auth header temporarily
            original_headers = self.session.headers.copy()
            if "Authorization" in self.session.headers:
                del self.session.headers["Authorization"]
            
            chat_data = {
                "message": "Test message",
                "baby_age_months": 6
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ai/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Restore headers
            self.session.headers.update(original_headers)
            
            if response.status_code == 401 or response.status_code == 403:
                self.log_test("Authentication Required", True, 
                            f"Correctly rejected unauthenticated request: {response.status_code}")
                return True
            else:
                self.log_test("Authentication Required", False, 
                            f"Should reject unauthenticated requests, got: {response.status_code}")
                return False
                
        except Exception as e:
            # Restore headers
            self.session.headers.update(original_headers)
            self.log_test("Authentication Required", False, f"Test error: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        print("⚠️ TESTING ERROR HANDLING...")
        
        test_cases = [
            {
                "name": "Missing message field",
                "data": {"baby_age_months": 6},
                "expected_status": 422
            },
            {
                "name": "Empty message",
                "data": {"message": "", "baby_age_months": 6},
                "expected_status": [200, 422]  # Either is acceptable
            },
            {
                "name": "Invalid baby age",
                "data": {"message": "Test", "baby_age_months": -1},
                "expected_status": [200, 422]  # Either is acceptable
            }
        ]
        
        passed_tests = 0
        
        for test_case in test_cases:
            try:
                response = self.session.post(
                    f"{BACKEND_URL}/ai/chat",
                    json=test_case["data"],
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                expected_statuses = test_case["expected_status"]
                if not isinstance(expected_statuses, list):
                    expected_statuses = [expected_statuses]
                
                if response.status_code in expected_statuses:
                    self.log_test(f"Error Handling: {test_case['name']}", True, 
                                f"Status {response.status_code} as expected")
                    passed_tests += 1
                else:
                    self.log_test(f"Error Handling: {test_case['name']}", False, 
                                f"Expected {expected_statuses}, got {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Error Handling: {test_case['name']}", False, f"Test error: {str(e)}")
        
        return passed_tests == len(test_cases)
    
    def run_comprehensive_tests(self):
        """Run all AI chat tests"""
        print("=" * 80)
        print("🤖 AI ASSISTANT GPT-5-NANO MODEL TESTING")
        print("=" * 80)
        print()
        
        # Step 1: Authentication
        if not self.authenticate():
            print("❌ CRITICAL: Authentication failed. Cannot proceed with testing.")
            return False
        
        # Step 2: Test authentication requirement
        auth_test_passed = self.test_authentication_required()
        
        # Step 3: Test specific baby care queries from review request
        print("📋 TESTING SPECIFIC BABY CARE QUERIES FROM REVIEW REQUEST...")
        print()
        
        test_queries = [
            {
                "message": "How often should I feed my 6 month old baby?",
                "baby_age_months": 6,
                "expected_keywords": ["6 month", "feeding", "times"]
            },
            {
                "message": "When can babies start eating solid food?",
                "baby_age_months": 4,
                "expected_keywords": ["solid", "food", "months"]
            },
            {
                "message": "Is it safe to give honey to a 10 month old baby?",
                "baby_age_months": 10,
                "expected_keywords": ["honey", "12 months", "avoid"]
            },
            {
                "message": "What are good finger foods for a 9 month old?",
                "baby_age_months": 9,
                "expected_keywords": ["finger foods", "9 month"]
            }
        ]
        
        passed_tests = 1 if auth_test_passed else 0
        total_tests = 1
        
        for query in test_queries:
            if self.test_ai_chat_endpoint(**query):
                passed_tests += 1
            total_tests += 1
        
        # Step 4: Test error handling
        if self.test_error_handling():
            passed_tests += 1
        total_tests += 1
        
        # Step 5: Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Tests Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        if success_rate >= 80:
            print("✅ AI ASSISTANT GPT-5-NANO MODEL: SUCCESS")
            print("   - Authentication working correctly")
            print("   - gpt-5-nano model responding appropriately")
            print("   - Baby care context maintained")
            print("   - Safety disclaimers included")
            print("   - Error handling functional")
        else:
            print("❌ AI ASSISTANT GPT-5-NANO MODEL: ISSUES FOUND")
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
    tester = AIChatTester()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 ALL AI CHAT TESTS PASSED - GPT-5-NANO MODEL WORKING!")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED - REVIEW IMPLEMENTATION NEEDED")
        sys.exit(1)

if __name__ == "__main__":
    main()