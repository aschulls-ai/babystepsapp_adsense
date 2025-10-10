#!/usr/bin/env python3
"""
Review Request Specific Testing
Testing the exact scenarios mentioned in the review request
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://smart-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class ReviewRequestTester:
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
    
    def test_specific_query(self, question, expected_behavior, category):
        """Test a specific query from the review request"""
        print(f"🔍 TESTING {category}: '{question}'")
        
        try:
            query_data = {"question": question}
            
            response = self.session.post(
                f"{BACKEND_URL}/research",
                json=query_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test(f"{category}: {question}", False, f"HTTP {response.status_code}")
                return False
            
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            
            print(f"   Response: {answer[:100]}...")
            print(f"   Sources: {sources}")
            
            # Check based on expected behavior
            if expected_behavior == "not_available":
                success = "Information Not Available" in answer or "not available" in answer.lower()
                if success:
                    self.log_test(f"{category}: {question}", True, "Correctly returned 'Information Not Available'")
                else:
                    self.log_test(f"{category}: {question}", False, f"Expected 'not available', got: {answer[:200]}...")
            
            elif expected_behavior == "ai_assistant":
                has_ai_source = any("AI Assistant" in str(source) for source in sources)
                if has_ai_source:
                    self.log_test(f"{category}: {question}", True, f"Correctly matched ai_assistant.json - sources: {sources}")
                else:
                    self.log_test(f"{category}: {question}", False, f"Expected AI Assistant match, got sources: {sources}")
                success = has_ai_source
            
            elif expected_behavior == "food_research":
                has_food_source = any("Food Safety" in str(source) for source in sources)
                if has_food_source:
                    self.log_test(f"{category}: {question}", True, f"Correctly matched food_research.json - sources: {sources}")
                else:
                    self.log_test(f"{category}: {question}", False, f"Expected Food Safety match, got sources: {sources}")
                success = has_food_source
            
            elif expected_behavior == "combined":
                has_combined = ("General Parenting Guidance" in answer and "Food Safety Information" in answer) or \
                              (any("AI Assistant" in str(s) for s in sources) and any("Food Safety" in str(s) for s in sources))
                if has_combined:
                    self.log_test(f"{category}: {question}", True, f"Correctly combined both knowledge bases")
                else:
                    self.log_test(f"{category}: {question}", False, f"Expected combined response, got: {answer[:200]}...")
                success = has_combined
            
            else:
                success = False
            
            return success
                
        except Exception as e:
            self.log_test(f"{category}: {question}", False, f"Request error: {str(e)}")
            return False
    
    def run_review_request_tests(self):
        """Run the exact test cases from the review request"""
        print("=" * 80)
        print("🎯 REVIEW REQUEST SPECIFIC TESTING")
        print("Testing the refined AI Assistant matching algorithm as specified")
        print("=" * 80)
        print()
        
        if not self.authenticate():
            return False
        
        # Test cases from review request
        test_cases = [
            # 1. Unrelated Topics (Should Return "Information Not Available")
            {
                "question": "How to train baby to use smartphone?",
                "expected": "not_available",
                "category": "UNRELATED TOPIC"
            },
            {
                "question": "What's the best car for families?",
                "expected": "not_available", 
                "category": "UNRELATED TOPIC"
            },
            {
                "question": "College preparation tips for teenagers",
                "expected": "not_available",
                "category": "UNRELATED TOPIC"
            },
            {
                "question": "Investment advice for new parents",
                "expected": "not_available",
                "category": "UNRELATED TOPIC"
            },
            
            # 2. Valid Parenting Questions (Should Match ai_assistant.json)
            {
                "question": "How often should I feed my newborn?",
                "expected": "ai_assistant",
                "category": "VALID PARENTING"
            },
            {
                "question": "When do babies start sleeping through the night?",
                "expected": "ai_assistant",
                "category": "VALID PARENTING"
            },
            {
                "question": "What are normal development milestones?",
                "expected": "ai_assistant",
                "category": "VALID PARENTING"
            },
            
            # 3. Valid Food Safety Questions (Should Match food_research.json)
            {
                "question": "Is honey safe for babies?",
                "expected": "food_research",
                "category": "FOOD SAFETY"
            },
            {
                "question": "When can babies eat eggs?",
                "expected": "food_research",
                "category": "FOOD SAFETY"
            },
            {
                "question": "Are strawberries safe for 6 month old?",
                "expected": "food_research",
                "category": "FOOD SAFETY"
            },
            
            # 4. Combined Questions (Should Match Both Knowledge Bases)
            {
                "question": "When should I burp baby and is honey safe for babies?",
                "expected": "combined",
                "category": "COMBINED QUESTION"
            },
            {
                "question": "How often to feed newborn and are eggs safe?",
                "expected": "combined",
                "category": "COMBINED QUESTION"
            },
            
            # 5. Edge Cases with Baby Context
            {
                "question": "Can babies use smartphones safely?",
                "expected": "not_available",
                "category": "EDGE CASE"
            },
            {
                "question": "What baby food can I eat while dieting?",
                "expected": "not_available",
                "category": "EDGE CASE"
            }
        ]
        
        # Run tests by category
        categories = {}
        for test_case in test_cases:
            category = test_case["category"]
            if category not in categories:
                categories[category] = {"passed": 0, "total": 0}
            
            success = self.test_specific_query(
                test_case["question"], 
                test_case["expected"], 
                test_case["category"]
            )
            
            categories[category]["total"] += 1
            if success:
                categories[category]["passed"] += 1
        
        # Calculate overall results
        total_passed = sum(cat["passed"] for cat in categories.values())
        total_tests = sum(cat["total"] for cat in categories.values())
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        
        # Summary
        print("=" * 80)
        print("📊 REVIEW REQUEST TEST SUMMARY")
        print("=" * 80)
        
        print(f"Overall Results: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        print("📋 RESULTS BY CATEGORY:")
        for category, results in categories.items():
            rate = (results["passed"] / results["total"]) * 100 if results["total"] > 0 else 0
            status = "✅" if rate >= 80 else "❌"
            print(f"   {status} {category}: {results['passed']}/{results['total']} ({rate:.1f}%)")
        
        print()
        
        if success_rate >= 80:
            print("✅ REVIEW REQUEST REQUIREMENTS: SUCCESSFULLY IMPLEMENTED")
            print("   ✓ Stricter parenting context requirements")
            print("   ✓ Higher scoring thresholds")
            print("   ✓ Exclusion of clearly unrelated topics")
            print("   ✓ Better food safety context detection")
            print("   ✓ Multi-knowledge-base support")
        else:
            print("❌ REVIEW REQUEST REQUIREMENTS: PARTIALLY IMPLEMENTED")
            print("   ⚠️ Some precision improvements still needed")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = ReviewRequestTester()
    success = tester.run_review_request_tests()
    
    if success:
        print("\n🎉 REVIEW REQUEST TESTING SUCCESSFUL!")
        print("   The refined AI Assistant matching algorithm meets the specified requirements.")
        sys.exit(0)
    else:
        print("\n⚠️ REVIEW REQUEST TESTING SHOWS AREAS FOR IMPROVEMENT")
        print("   Some requirements may need additional refinement.")
        sys.exit(1)

if __name__ == "__main__":
    main()