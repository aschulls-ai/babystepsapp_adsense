#!/usr/bin/env python3
"""
Edge Case Testing for Refined Algorithms
Testing additional scenarios to ensure robustness
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class EdgeCaseTester:
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
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def test_food_variations(self):
        """Test different variations of food queries"""
        print("🍓 TESTING FOOD QUERY VARIATIONS...")
        
        variations = [
            ("strawberries safe babies", "205", "strawberr"),
            ("strawberry baby safe", "205", "strawberr"), 
            ("can baby eat strawberry", "205", "strawberr"),
            ("honey safe for baby", "201", "honey"),
            ("is honey ok for babies", "201", "honey"),
            ("baby honey safety", "201", "honey"),
            ("eggs for babies", "202", "egg"),
            ("baby eating eggs", "202", "egg"),
            ("when eggs baby", "202", "egg")
        ]
        
        passed = 0
        
        for query, expected_id, expected_content in variations:
            try:
                query_data = {"question": query, "baby_age_months": 8}
                response = self.session.post(
                    f"{BACKEND_URL}/food/research",
                    json=query_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    sources = result.get("sources", [])
                    answer = result.get("answer", "").lower()
                    
                    has_correct_id = any(f"question id: {expected_id}" in source.lower() for source in sources)
                    has_content = expected_content.lower() in answer
                    
                    if has_correct_id and has_content:
                        passed += 1
                        self.log_test(f"Food Variation: {query}", True, f"✓ ID {expected_id} ✓ Content '{expected_content}'")
                    else:
                        self.log_test(f"Food Variation: {query}", False, f"Missing ID {expected_id} or content '{expected_content}'")
                else:
                    self.log_test(f"Food Variation: {query}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Food Variation: {query}", False, f"Error: {str(e)}")
        
        return passed, len(variations)
    
    def test_false_positive_prevention(self):
        """Test that unrelated queries don't match incorrectly"""
        print("🚫 TESTING FALSE POSITIVE PREVENTION...")
        
        unrelated_queries = [
            "What's the weather like?",
            "How to fix my car?", 
            "Best smartphone for adults?",
            "Investment advice for retirement?",
            "College application tips?"
        ]
        
        passed = 0
        
        for query in unrelated_queries:
            try:
                # Test AI Assistant endpoint
                query_data = {"question": query}
                response = self.session.post(
                    f"{BACKEND_URL}/research",
                    json=query_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "")
                    
                    # Should return "Information Not Available" for unrelated topics
                    if "Information Not Available" in answer or "not available" in answer.lower():
                        passed += 1
                        self.log_test(f"False Positive Prevention: {query}", True, "✓ Correctly rejected unrelated query")
                    else:
                        self.log_test(f"False Positive Prevention: {query}", False, f"Incorrectly matched: {answer[:100]}...")
                else:
                    self.log_test(f"False Positive Prevention: {query}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"False Positive Prevention: {query}", False, f"Error: {str(e)}")
        
        return passed, len(unrelated_queries)
    
    def test_combined_query_robustness(self):
        """Test complex combined queries"""
        print("🔄 TESTING COMBINED QUERY ROBUSTNESS...")
        
        combined_queries = [
            "How to burp baby and when can they eat honey?",
            "Sleep schedule for newborn and strawberry safety?", 
            "Feeding frequency and egg introduction timing?",
            "Baby crying reasons and honey safety information?"
        ]
        
        passed = 0
        
        for query in combined_queries:
            try:
                query_data = {"question": query}
                response = self.session.post(
                    f"{BACKEND_URL}/research",
                    json=query_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "")
                    sources = result.get("sources", [])
                    
                    # Should have multiple sections or comprehensive response
                    has_multiple_sources = len(sources) >= 2
                    has_substantial_content = len(answer) > 200
                    
                    if has_multiple_sources and has_substantial_content:
                        passed += 1
                        self.log_test(f"Combined Query: {query}", True, f"✓ {len(sources)} sources ✓ {len(answer)} chars")
                    else:
                        self.log_test(f"Combined Query: {query}", False, f"Insufficient response: {len(sources)} sources, {len(answer)} chars")
                else:
                    self.log_test(f"Combined Query: {query}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Combined Query: {query}", False, f"Error: {str(e)}")
        
        return passed, len(combined_queries)
    
    def run_edge_case_tests(self):
        """Run all edge case tests"""
        print("=" * 80)
        print("🧪 EDGE CASE TESTING FOR REFINED ALGORITHMS")
        print("=" * 80)
        print()
        
        if not self.authenticate():
            print("❌ CRITICAL: Authentication failed.")
            return False
        
        # Run edge case tests
        var_passed, var_total = self.test_food_variations()
        fp_passed, fp_total = self.test_false_positive_prevention()
        comb_passed, comb_total = self.test_combined_query_robustness()
        
        # Calculate results
        total_passed = var_passed + fp_passed + comb_passed
        total_tests = var_total + fp_total + comb_total
        
        print("=" * 80)
        print("📊 EDGE CASE TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        print(f"Overall Tests Passed: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        print("📋 CATEGORY BREAKDOWN:")
        print(f"   Food Query Variations: {var_passed}/{var_total}")
        print(f"   False Positive Prevention: {fp_passed}/{fp_total}")
        print(f"   Combined Query Robustness: {comb_passed}/{comb_total}")
        print()
        
        if success_rate >= 80:
            print("✅ EDGE CASE TESTING: EXCELLENT ROBUSTNESS")
        elif success_rate >= 60:
            print("⚠️  EDGE CASE TESTING: GOOD WITH MINOR ISSUES")
        else:
            print("❌ EDGE CASE TESTING: NEEDS IMPROVEMENT")
        
        return success_rate >= 70

def main():
    """Main test execution"""
    tester = EdgeCaseTester()
    success = tester.run_edge_case_tests()
    
    if success:
        print("\n🎉 EDGE CASE TESTS PASSED - ALGORITHMS ARE ROBUST!")
        sys.exit(0)
    else:
        print("\n⚠️  SOME EDGE CASE TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()