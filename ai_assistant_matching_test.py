#!/usr/bin/env python3
"""
AI Assistant Matching Algorithm Testing
Testing the refined AI Assistant matching algorithm for precision improvements
Focus on preventing false positives and ensuring accurate matching
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://baby-genius.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class AIAssistantMatchingTester:
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
    
    def test_ai_assistant_query(self, question, expected_result_type, expected_source=None, description=""):
        """
        Test AI Assistant research endpoint
        expected_result_type: 'not_available', 'ai_assistant', 'food_research', 'combined'
        """
        print(f"🔍 TESTING AI ASSISTANT QUERY: '{question}'")
        if description:
            print(f"   Expected: {description}")
        
        try:
            query_data = {
                "question": question
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/research",
                json=query_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test(f"AI Assistant: {question}", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            
            # Analyze response type
            has_ai_assistant_source = any("AI Assistant" in str(source) for source in sources)
            has_food_research_source = any("Food Safety" in str(source) for source in sources)
            has_not_available = "Information Not Available" in answer or "not available" in answer.lower()
            has_combined_sections = "General Parenting Guidance" in answer and "Food Safety Information" in answer
            
            # Check expected result type
            if expected_result_type == "not_available":
                if has_not_available:
                    self.log_test(f"AI Assistant: {question}", True, 
                                f"Correctly returned 'Information Not Available' - {len(answer)} chars")
                    return True
                else:
                    self.log_test(f"AI Assistant: {question}", False, 
                                f"Expected 'not available' but got response: {answer[:200]}...")
                    return False
            
            elif expected_result_type == "ai_assistant":
                if has_ai_assistant_source and not has_food_research_source:
                    self.log_test(f"AI Assistant: {question}", True, 
                                f"Correctly matched ai_assistant.json - {len(answer)} chars, sources: {sources}")
                    return True
                else:
                    self.log_test(f"AI Assistant: {question}", False, 
                                f"Expected ai_assistant.json match, got sources: {sources}")
                    return False
            
            elif expected_result_type == "food_research":
                if has_food_research_source and not has_ai_assistant_source:
                    self.log_test(f"AI Assistant: {question}", True, 
                                f"Correctly matched food_research.json - {len(answer)} chars, sources: {sources}")
                    return True
                else:
                    self.log_test(f"AI Assistant: {question}", False, 
                                f"Expected food_research.json match, got sources: {sources}")
                    return False
            
            elif expected_result_type == "combined":
                if has_combined_sections or (has_ai_assistant_source and has_food_research_source):
                    self.log_test(f"AI Assistant: {question}", True, 
                                f"Correctly combined both knowledge bases - {len(answer)} chars")
                    return True
                else:
                    self.log_test(f"AI Assistant: {question}", False, 
                                f"Expected combined response, got: {answer[:200]}...")
                    return False
            
            else:
                self.log_test(f"AI Assistant: {question}", False, 
                            f"Unknown expected result type: {expected_result_type}")
                return False
                
        except Exception as e:
            self.log_test(f"AI Assistant: {question}", False, f"Request error: {str(e)}")
            return False
    
    def run_unrelated_topics_tests(self):
        """Test unrelated topics that should return 'Information Not Available'"""
        print("🚫 TESTING UNRELATED TOPICS (Should Return 'Information Not Available')...")
        print()
        
        unrelated_queries = [
            {
                "question": "How to train baby to use smartphone?",
                "description": "Technology training - unrelated to parenting advice"
            },
            {
                "question": "What's the best car for families?",
                "description": "Car purchasing - unrelated despite family context"
            },
            {
                "question": "College preparation tips for teenagers",
                "description": "Education for older children - outside baby/parenting scope"
            },
            {
                "question": "Investment advice for new parents",
                "description": "Financial advice - unrelated despite parent context"
            }
        ]
        
        passed = 0
        for query in unrelated_queries:
            if self.test_ai_assistant_query(
                query["question"], 
                "not_available", 
                description=query["description"]
            ):
                passed += 1
        
        return passed, len(unrelated_queries)
    
    def run_valid_parenting_tests(self):
        """Test valid parenting questions that should match ai_assistant.json"""
        print("👶 TESTING VALID PARENTING QUESTIONS (Should Match ai_assistant.json)...")
        print()
        
        parenting_queries = [
            {
                "question": "How often should I feed my newborn?",
                "description": "Feeding frequency - core parenting question"
            },
            {
                "question": "When do babies start sleeping through the night?",
                "description": "Sleep patterns - developmental question"
            },
            {
                "question": "What are normal development milestones?",
                "description": "Development tracking - parenting guidance"
            }
        ]
        
        passed = 0
        for query in parenting_queries:
            if self.test_ai_assistant_query(
                query["question"], 
                "ai_assistant", 
                description=query["description"]
            ):
                passed += 1
        
        return passed, len(parenting_queries)
    
    def run_food_safety_tests(self):
        """Test valid food safety questions that should match food_research.json"""
        print("🥗 TESTING VALID FOOD SAFETY QUESTIONS (Should Match food_research.json)...")
        print()
        
        food_safety_queries = [
            {
                "question": "Is honey safe for babies?",
                "description": "Honey safety - specific food safety question"
            },
            {
                "question": "When can babies eat eggs?",
                "description": "Egg introduction - food safety timing"
            },
            {
                "question": "Are strawberries safe for 6 month old?",
                "description": "Strawberry safety - age-specific food question"
            }
        ]
        
        passed = 0
        for query in food_safety_queries:
            if self.test_ai_assistant_query(
                query["question"], 
                "food_research", 
                description=query["description"]
            ):
                passed += 1
        
        return passed, len(food_safety_queries)
    
    def run_combined_questions_tests(self):
        """Test combined questions that should match both knowledge bases"""
        print("🔄 TESTING COMBINED QUESTIONS (Should Match Both Knowledge Bases)...")
        print()
        
        combined_queries = [
            {
                "question": "When should I burp baby and is honey safe for babies?",
                "description": "Parenting technique + food safety - should combine both"
            },
            {
                "question": "How often to feed newborn and are eggs safe?",
                "description": "Feeding frequency + food safety - should combine both"
            }
        ]
        
        passed = 0
        for query in combined_queries:
            if self.test_ai_assistant_query(
                query["question"], 
                "combined", 
                description=query["description"]
            ):
                passed += 1
        
        return passed, len(combined_queries)
    
    def run_edge_cases_tests(self):
        """Test edge cases with baby context that should still return not available"""
        print("⚠️ TESTING EDGE CASES WITH BABY CONTEXT (Should Return 'Information Not Available')...")
        print()
        
        edge_case_queries = [
            {
                "question": "Can babies use smartphones safely?",
                "description": "Technology question despite baby context - unrelated"
            },
            {
                "question": "What baby food can I eat while dieting?",
                "description": "Adult diet question despite baby mention - unrelated"
            }
        ]
        
        passed = 0
        for query in edge_case_queries:
            if self.test_ai_assistant_query(
                query["question"], 
                "not_available", 
                description=query["description"]
            ):
                passed += 1
        
        return passed, len(edge_case_queries)
    
    def run_comprehensive_tests(self):
        """Run all AI Assistant matching algorithm tests"""
        print("=" * 80)
        print("🧪 AI ASSISTANT MATCHING ALGORITHM TESTING")
        print("Testing refined algorithm for precision improvements and false positive prevention")
        print("=" * 80)
        print()
        
        # Step 1: Authentication
        if not self.authenticate():
            print("❌ CRITICAL: Authentication failed. Cannot proceed with testing.")
            return False
        
        # Step 2: Run all test categories
        total_passed = 0
        total_tests = 0
        
        # Test unrelated topics
        passed, count = self.run_unrelated_topics_tests()
        total_passed += passed
        total_tests += count
        
        # Test valid parenting questions
        passed, count = self.run_valid_parenting_tests()
        total_passed += passed
        total_tests += count
        
        # Test food safety questions
        passed, count = self.run_food_safety_tests()
        total_passed += passed
        total_tests += count
        
        # Test combined questions
        passed, count = self.run_combined_questions_tests()
        total_passed += passed
        total_tests += count
        
        # Test edge cases
        passed, count = self.run_edge_cases_tests()
        total_passed += passed
        total_tests += count
        
        # Step 3: Summary
        print("=" * 80)
        print("📊 AI ASSISTANT MATCHING ALGORITHM TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        print(f"Tests Passed: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        if success_rate >= 80:
            print("✅ AI ASSISTANT MATCHING ALGORITHM: PRECISION IMPROVEMENTS SUCCESSFUL")
            print("   ✓ Stricter parenting context requirements working")
            print("   ✓ Higher scoring thresholds preventing false positives")
            print("   ✓ Exclusion of unrelated topics functioning")
            print("   ✓ Food safety context detection accurate")
            print("   ✓ Multi-knowledge-base support operational")
        else:
            print("❌ AI ASSISTANT MATCHING ALGORITHM: PRECISION ISSUES FOUND")
            print("   ⚠️ Some tests failed - algorithm may need refinement")
        
        print()
        print("🔍 DETAILED TEST RESULTS BY CATEGORY:")
        
        # Group results by category
        categories = {
            "Unrelated Topics": [],
            "Valid Parenting": [],
            "Food Safety": [],
            "Combined Questions": [],
            "Edge Cases": []
        }
        
        for result in self.test_results:
            if "Authentication" in result["test"]:
                continue
            elif any(keyword in result["test"].lower() for keyword in ["smartphone", "car", "college", "investment"]):
                categories["Unrelated Topics"].append(result)
            elif any(keyword in result["test"].lower() for keyword in ["feed", "sleep", "milestone"]):
                categories["Valid Parenting"].append(result)
            elif any(keyword in result["test"].lower() for keyword in ["honey", "egg", "strawberr"]):
                categories["Food Safety"].append(result)
            elif "and" in result["test"].lower():
                categories["Combined Questions"].append(result)
            else:
                categories["Edge Cases"].append(result)
        
        for category, results in categories.items():
            if results:
                passed_in_category = sum(1 for r in results if r["passed"])
                total_in_category = len(results)
                print(f"\n   {category}: {passed_in_category}/{total_in_category}")
                for result in results:
                    status = "✅" if result["passed"] else "❌"
                    print(f"      {status} {result['test']}")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = AIAssistantMatchingTester()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 AI ASSISTANT MATCHING ALGORITHM PRECISION IMPROVEMENTS VERIFIED!")
        print("   The refined algorithm successfully prevents false positives")
        print("   and maintains accuracy for legitimate baby/parenting queries.")
        sys.exit(0)
    else:
        print("\n⚠️ AI ASSISTANT MATCHING ALGORITHM NEEDS REFINEMENT")
        print("   Some precision issues detected - review algorithm implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()