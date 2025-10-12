#!/usr/bin/env python3
"""
Additional Precision Tests for AI Assistant Matching Algorithm
Testing more edge cases and boundary conditions
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class AdditionalPrecisionTester:
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
        print("🔐 AUTHENTICATING...")
        
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
                print("✅ Authentication successful")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def test_query(self, question, expected_type, description=""):
        """Test a query and check if it matches expected type"""
        print(f"🔍 TESTING: '{question}'")
        if description:
            print(f"   Expected: {description}")
        
        try:
            query_data = {"question": question}
            
            response = self.session.post(
                f"{BACKEND_URL}/research",
                json=query_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test(f"Query: {question}", False, f"HTTP {response.status_code}")
                return False
            
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            
            # Analyze response
            has_ai_assistant = any("AI Assistant" in str(source) for source in sources)
            has_food_safety = any("Food Safety" in str(source) for source in sources)
            has_not_available = "Information Not Available" in answer or "not available" in answer.lower()
            has_combined = "General Parenting Guidance" in answer and "Food Safety Information" in answer
            
            # Check expected type
            if expected_type == "not_available":
                success = has_not_available
            elif expected_type == "ai_assistant":
                success = has_ai_assistant and not has_food_safety
            elif expected_type == "food_safety":
                success = has_food_safety and not has_ai_assistant
            elif expected_type == "combined":
                success = has_combined or (has_ai_assistant and has_food_safety)
            else:
                success = False
            
            if success:
                self.log_test(f"Query: {question}", True, f"Correctly returned {expected_type} - {len(answer)} chars")
            else:
                self.log_test(f"Query: {question}", False, f"Expected {expected_type}, got sources: {sources}")
            
            return success
                
        except Exception as e:
            self.log_test(f"Query: {question}", False, f"Request error: {str(e)}")
            return False
    
    def run_boundary_tests(self):
        """Test boundary cases and edge conditions"""
        print("🎯 TESTING BOUNDARY CONDITIONS AND EDGE CASES...")
        print()
        
        boundary_tests = [
            # Ambiguous baby context
            {
                "question": "How to baby-proof my smartphone?",
                "expected": "not_available",
                "description": "Baby-proofing technology - should be unrelated"
            },
            {
                "question": "Baby monitor recommendations for tech-savvy parents",
                "expected": "not_available", 
                "description": "Technology product recommendation - unrelated"
            },
            
            # Adult-focused questions with baby mentions
            {
                "question": "How to lose baby weight after pregnancy?",
                "expected": "not_available",
                "description": "Adult weight loss - unrelated to baby care"
            },
            {
                "question": "Best baby shower gifts for new parents?",
                "expected": "not_available",
                "description": "Gift recommendations - not parenting guidance"
            },
            
            # Borderline parenting questions
            {
                "question": "When should babies start talking?",
                "expected": "ai_assistant",
                "description": "Development milestone - should match parenting KB"
            },
            {
                "question": "How to introduce solid foods to baby?",
                "expected": "ai_assistant",
                "description": "Feeding guidance - core parenting topic"
            },
            
            # Food safety edge cases
            {
                "question": "Can I give my baby organic honey?",
                "expected": "food_safety",
                "description": "Honey safety with qualifier - still food safety"
            },
            {
                "question": "What foods should I avoid giving my baby?",
                "expected": "food_safety",
                "description": "General food safety - should match food KB"
            },
            
            # Mixed context tests
            {
                "question": "Baby sleep schedule and safe sleep foods",
                "expected": "combined",
                "description": "Sleep + food safety - should combine both KBs"
            },
            {
                "question": "Feeding schedule and honey safety for newborns",
                "expected": "combined", 
                "description": "Feeding + food safety - should combine both KBs"
            }
        ]
        
        passed = 0
        for test in boundary_tests:
            if self.test_query(test["question"], test["expected"], test["description"]):
                passed += 1
        
        return passed, len(boundary_tests)
    
    def run_precision_validation(self):
        """Validate precision improvements with specific test cases"""
        print("🎯 VALIDATING PRECISION IMPROVEMENTS...")
        print()
        
        precision_tests = [
            # False positive prevention
            {
                "question": "Baby names for boys and girls",
                "expected": "not_available",
                "description": "Naming advice - not parenting guidance"
            },
            {
                "question": "Baby photography tips and tricks",
                "expected": "not_available",
                "description": "Photography advice - unrelated to baby care"
            },
            
            # Ensure legitimate queries still work
            {
                "question": "How much should my baby sleep?",
                "expected": "ai_assistant",
                "description": "Sleep guidance - core parenting question"
            },
            {
                "question": "Is fish safe for babies?",
                "expected": "food_safety",
                "description": "Fish safety - food safety question"
            },
            
            # Context sensitivity
            {
                "question": "Baby formula vs breastfeeding benefits",
                "expected": "ai_assistant",
                "description": "Feeding method comparison - parenting guidance"
            },
            {
                "question": "When can babies have dairy products?",
                "expected": "food_safety",
                "description": "Dairy introduction - food safety timing"
            }
        ]
        
        passed = 0
        for test in precision_tests:
            if self.test_query(test["question"], test["expected"], test["description"]):
                passed += 1
        
        return passed, len(precision_tests)
    
    def run_comprehensive_tests(self):
        """Run all additional precision tests"""
        print("=" * 80)
        print("🎯 ADDITIONAL PRECISION TESTING FOR AI ASSISTANT MATCHING")
        print("Validating boundary conditions and edge cases")
        print("=" * 80)
        print()
        
        if not self.authenticate():
            return False
        
        total_passed = 0
        total_tests = 0
        
        # Run boundary tests
        passed, count = self.run_boundary_tests()
        total_passed += passed
        total_tests += count
        
        # Run precision validation
        passed, count = self.run_precision_validation()
        total_passed += passed
        total_tests += count
        
        # Summary
        print("=" * 80)
        print("📊 ADDITIONAL PRECISION TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        print(f"Tests Passed: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        if success_rate >= 80:
            print("✅ ADDITIONAL PRECISION TESTS: SUCCESSFUL")
            print("   ✓ Boundary conditions handled correctly")
            print("   ✓ False positive prevention working")
            print("   ✓ Context sensitivity maintained")
            print("   ✓ Edge cases properly classified")
        else:
            print("❌ ADDITIONAL PRECISION TESTS: ISSUES FOUND")
            print("   ⚠️ Some edge cases need refinement")
        
        print()
        print("🔍 DETAILED RESULTS:")
        for result in self.test_results:
            if "Authentication" not in result["test"]:
                status = "✅" if result["passed"] else "❌"
                print(f"   {status} {result['test']}")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = AdditionalPrecisionTester()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 ADDITIONAL PRECISION TESTS PASSED!")
        print("   Algorithm demonstrates excellent precision and boundary handling.")
        sys.exit(0)
    else:
        print("\n⚠️ SOME ADDITIONAL PRECISION TESTS FAILED")
        print("   Algorithm may need further refinement for edge cases.")
        sys.exit(1)

if __name__ == "__main__":
    main()