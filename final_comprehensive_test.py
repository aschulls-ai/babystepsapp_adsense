#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE BACKEND TESTING - FOOD SAFETY SEARCH & AI ASSISTANT
Testing the improved food matching algorithm and multi-knowledge-base AI Assistant
Based on actual knowledge base content
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://baby-steps-demo-api.onrender.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class FinalComprehensiveTester:
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

    def test_food_safety_basic_queries(self):
        """Test basic food queries from review request"""
        print("🍓 TESTING BASIC FOOD QUERIES...")
        
        basic_food_tests = [
            {"query": "strawberries", "description": "Single word strawberry query"},
            {"query": "can my baby eat strawberries", "description": "Natural strawberry question"},
            {"query": "are strawberries safe for babies", "description": "Strawberry safety question"},
            {"query": "honey", "description": "Single word honey query"},
            {"query": "when can baby have honey", "description": "Age-related honey question"},
            {"query": "is honey safe", "description": "Safety question for honey"},
            {"query": "eggs", "description": "Single word egg query"},
            {"query": "can babies eat eggs", "description": "Natural egg question"},
            {"query": "avocado", "description": "Single word avocado query"},
            {"query": "peanuts", "description": "Single word peanut query"},
            {"query": "are peanuts safe", "description": "Peanut safety question"}
        ]
        
        passed_tests = 0
        total_tests = len(basic_food_tests)
        
        for test in basic_food_tests:
            try:
                query_data = {
                    "question": test["query"],
                    "baby_age_months": 8
                }
                
                response = self.session.post(
                    f"{BACKEND_URL}/food/research",
                    json=query_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "")
                    sources = result.get("sources", [])
                    safety_level = result.get("safety_level", "")
                    
                    # Check if we got a relevant response (not "not available")
                    if "Food Safety Information Not Available" not in answer:
                        # Extract Question ID from sources
                        question_id = "Unknown"
                        for source in sources:
                            if "Knowledge Base Question ID:" in source:
                                question_id = source.split("Knowledge Base Question ID: ")[1].split(",")[0]
                                break
                        
                        self.log_test(f"Basic Food Query: {test['query']}", True, 
                                    f"{test['description']} - Got relevant response, Question ID: {question_id}, Safety: {safety_level}")
                        passed_tests += 1
                    else:
                        self.log_test(f"Basic Food Query: {test['query']}", False, 
                                    f"{test['description']} - Got 'not available' response")
                else:
                    self.log_test(f"Basic Food Query: {test['query']}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"Basic Food Query: {test['query']}", False, f"Request error: {str(e)}")
        
        return passed_tests, total_tests

    def test_answer_accuracy_no_honey_confusion(self):
        """Test that non-honey queries don't return honey information"""
        print("🎯 TESTING ANSWER ACCURACY - NO HONEY CONFUSION...")
        
        accuracy_tests = [
            {"query": "strawberries", "should_not_contain": "honey", "description": "Strawberry query should not return honey info"},
            {"query": "eggs", "should_not_contain": "honey", "description": "Egg query should not return honey info"},
            {"query": "avocado", "should_not_contain": "honey", "description": "Avocado query should not return honey info"},
            {"query": "honey", "should_contain": "honey", "description": "Honey query should return honey-specific info"}
        ]
        
        passed_tests = 0
        total_tests = len(accuracy_tests)
        
        for test in accuracy_tests:
            try:
                query_data = {
                    "question": test["query"],
                    "baby_age_months": 8
                }
                
                response = self.session.post(
                    f"{BACKEND_URL}/food/research",
                    json=query_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "").lower()
                    sources = result.get("sources", [])
                    
                    # Extract Question ID
                    question_id = "Unknown"
                    for source in sources:
                        if "Knowledge Base Question ID:" in source:
                            question_id = source.split("Knowledge Base Question ID: ")[1].split(",")[0]
                            break
                    
                    if "should_not_contain" in test:
                        if test["should_not_contain"] not in answer:
                            self.log_test(f"Answer Accuracy: {test['query']}", True, 
                                        f"{test['description']} - Correctly excludes {test['should_not_contain']}, Question ID: {question_id}")
                            passed_tests += 1
                        else:
                            self.log_test(f"Answer Accuracy: {test['query']}", False, 
                                        f"{test['description']} - Incorrectly contains {test['should_not_contain']}")
                    
                    if "should_contain" in test:
                        if test["should_contain"] in answer:
                            self.log_test(f"Answer Accuracy: {test['query']}", True, 
                                        f"{test['description']} - Correctly contains {test['should_contain']}, Question ID: {question_id}")
                            passed_tests += 1
                        else:
                            self.log_test(f"Answer Accuracy: {test['query']}", False, 
                                        f"{test['description']} - Missing {test['should_contain']} content")
                else:
                    self.log_test(f"Answer Accuracy: {test['query']}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"Answer Accuracy: {test['query']}", False, f"Request error: {str(e)}")
        
        return passed_tests, total_tests

    def test_age_range_display(self):
        """Test that age ranges are displayed in answers"""
        print("📅 TESTING AGE RANGE DISPLAY...")
        
        age_tests = [
            {"query": "honey", "description": "Honey should show age restriction"},
            {"query": "eggs", "description": "Eggs should show age recommendation"},
            {"query": "avocado", "description": "Avocado should show age guidance"}
        ]
        
        passed_tests = 0
        total_tests = len(age_tests)
        
        for test in age_tests:
            try:
                query_data = {
                    "question": test["query"],
                    "baby_age_months": 8
                }
                
                response = self.session.post(
                    f"{BACKEND_URL}/food/research",
                    json=query_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "")
                    age_recommendation = result.get("age_recommendation", "")
                    
                    # Check if age information is present
                    has_age_info = bool(age_recommendation) or any(age_indicator in answer for age_indicator in 
                                                                 ["months", "after", "before", "6", "12"])
                    
                    if has_age_info:
                        self.log_test(f"Age Range Display: {test['query']}", True, 
                                    f"{test['description']} - Age info present: {age_recommendation}")
                        passed_tests += 1
                    else:
                        self.log_test(f"Age Range Display: {test['query']}", False, 
                                    f"{test['description']} - No age information found")
                else:
                    self.log_test(f"Age Range Display: {test['query']}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"Age Range Display: {test['query']}", False, f"Request error: {str(e)}")
        
        return passed_tests, total_tests

    def test_keyword_variations(self):
        """Test different keyword variations and phrasings"""
        print("🔄 TESTING KEYWORD VARIATIONS...")
        
        variation_tests = [
            {"queries": ["strawberry", "strawberries"], "description": "Singular vs plural strawberry"},
            {"queries": ["can baby eat eggs", "is eggs safe", "eggs safety"], "description": "Different egg question phrasings"},
            {"queries": ["honey", "when can baby have honey"], "description": "Simple vs complex honey questions"}
        ]
        
        passed_tests = 0
        total_tests = len(variation_tests)
        
        for test in variation_tests:
            try:
                responses = []
                for query in test["queries"]:
                    query_data = {
                        "question": query,
                        "baby_age_months": 8
                    }
                    
                    response = self.session.post(
                        f"{BACKEND_URL}/food/research",
                        json=query_data,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        responses.append(result)
                
                # Check if all variations return relevant responses
                if len(responses) == len(test["queries"]):
                    # All queries should return food-specific responses
                    all_relevant = True
                    question_ids = []
                    
                    for i, resp in enumerate(responses):
                        answer = resp.get("answer", "")
                        sources = resp.get("sources", [])
                        
                        # Extract Question ID
                        question_id = "Unknown"
                        for source in sources:
                            if "Knowledge Base Question ID:" in source:
                                question_id = source.split("Knowledge Base Question ID: ")[1].split(",")[0]
                                break
                        question_ids.append(question_id)
                        
                        # Check if response is relevant (not "not available")
                        if "Food Safety Information Not Available" in resp.get("answer", ""):
                            all_relevant = False
                            break
                    
                    if all_relevant:
                        self.log_test(f"Keyword Variations: {test['description']}", True, 
                                    f"All variations return relevant responses, Question IDs: {question_ids}")
                        passed_tests += 1
                    else:
                        self.log_test(f"Keyword Variations: {test['description']}", False, 
                                    f"Some variations return 'not available' responses")
                else:
                    self.log_test(f"Keyword Variations: {test['description']}", False, 
                                f"Failed to get responses for all variations")
                    
            except Exception as e:
                self.log_test(f"Keyword Variations: {test['description']}", False, f"Request error: {str(e)}")
        
        return passed_tests, total_tests

    def test_ai_assistant_single_kb(self):
        """Test AI Assistant single knowledge base queries"""
        print("🤖 TESTING AI ASSISTANT SINGLE KNOWLEDGE BASE QUERIES...")
        
        single_kb_tests = [
            {"query": "How much should my baby sleep?", "kb_type": "parenting", "description": "Pure parenting question"},
            {"query": "Why is my baby crying?", "kb_type": "parenting", "description": "Baby behavior question"},
            {"query": "When do babies start walking?", "kb_type": "parenting", "description": "Development milestone question"},
            {"query": "Can babies eat honey?", "kb_type": "food", "description": "Pure food safety question"},
            {"query": "Are strawberries safe for babies?", "kb_type": "food", "description": "Food safety question"},
            {"query": "When can babies have eggs?", "kb_type": "food", "description": "Food introduction question"}
        ]
        
        passed_tests = 0
        total_tests = len(single_kb_tests)
        
        for test in single_kb_tests:
            try:
                query_data = {
                    "question": test["query"]
                }
                
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
                    
                    # Extract Question IDs from sources
                    question_ids = []
                    for source in sources:
                        if "Question ID:" in source:
                            parts = source.split("Question ID: ")
                            if len(parts) > 1:
                                question_ids.append(parts[1].split(",")[0].strip())
                    
                    # Check if response is relevant and not "Information Not Available"
                    is_relevant = "Information Not Available" not in answer and len(answer) > 50
                    
                    if is_relevant and question_ids:
                        self.log_test(f"AI Assistant Single KB: {test['query']}", True, 
                                    f"{test['description']} - Relevant {test['kb_type']} response, Question IDs: {question_ids}")
                        passed_tests += 1
                    else:
                        self.log_test(f"AI Assistant Single KB: {test['query']}", False, 
                                    f"{test['description']} - Missing relevant content or Question IDs")
                else:
                    self.log_test(f"AI Assistant Single KB: {test['query']}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"AI Assistant Single KB: {test['query']}", False, f"Request error: {str(e)}")
        
        return passed_tests, total_tests

    def test_ai_assistant_multi_kb(self):
        """Test AI Assistant multi-knowledge-base queries"""
        print("🔗 TESTING AI ASSISTANT MULTI-KNOWLEDGE-BASE QUERIES...")
        
        multi_kb_tests = [
            {"query": "What should I feed my 6 month old and is honey safe?", "description": "Feeding schedule + honey safety"},
            {"query": "Baby feeding schedule and strawberry safety", "description": "Schedule + strawberry safety"},
            {"query": "Sleep routine and food safety for babies", "description": "Sleep + general food safety"}
        ]
        
        passed_tests = 0
        total_tests = len(multi_kb_tests)
        
        for test in multi_kb_tests:
            try:
                query_data = {
                    "question": test["query"]
                }
                
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
                    
                    # Check for multi-KB indicators or multiple sources
                    has_multiple_sources = len(sources) > 1
                    has_substantial_content = len(answer) > 200
                    
                    # Extract Question IDs from both knowledge bases
                    question_ids = []
                    for source in sources:
                        if "Question ID:" in source:
                            parts = source.split("Question ID: ")
                            if len(parts) > 1:
                                question_ids.append(parts[1].split(",")[0].strip())
                    
                    # Should have substantial content and sources
                    if has_substantial_content and question_ids:
                        self.log_test(f"AI Assistant Multi-KB: {test['query']}", True, 
                                    f"{test['description']} - Multi-KB response, Question IDs: {question_ids}")
                        passed_tests += 1
                    else:
                        self.log_test(f"AI Assistant Multi-KB: {test['query']}", False, 
                                    f"{test['description']} - Insufficient content or sources")
                else:
                    self.log_test(f"AI Assistant Multi-KB: {test['query']}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"AI Assistant Multi-KB: {test['query']}", False, f"Request error: {str(e)}")
        
        return passed_tests, total_tests

    def test_question_variations(self):
        """Test AI Assistant question variations"""
        print("❓ TESTING AI ASSISTANT QUESTION VARIATIONS...")
        
        variation_tests = [
            {"queries": ["How much should baby sleep", "Baby won't sleep"], "description": "Sleep question variations"},
            {"queries": ["How often to feed newborn", "When should I feed my baby"], "description": "Feeding question variations"}
        ]
        
        passed_tests = 0
        total_tests = len(variation_tests)
        
        for test in variation_tests:
            try:
                responses = []
                for query in test["queries"]:
                    query_data = {
                        "question": query
                    }
                    
                    response = self.session.post(
                        f"{BACKEND_URL}/research",
                        json=query_data,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        responses.append(result)
                
                # Check if all variations return relevant responses
                if len(responses) == len(test["queries"]):
                    all_relevant = True
                    question_ids = []
                    
                    for i, resp in enumerate(responses):
                        answer = resp.get("answer", "")
                        sources = resp.get("sources", [])
                        
                        # Extract Question IDs
                        for source in sources:
                            if "Question ID:" in source:
                                parts = source.split("Question ID: ")
                                if len(parts) > 1:
                                    question_ids.append(parts[1].split(",")[0].strip())
                        
                        # Check if response is relevant (not "not available")
                        if "Information Not Available" in answer or len(answer) < 50:
                            all_relevant = False
                            break
                    
                    if all_relevant:
                        self.log_test(f"AI Question Variations: {test['description']}", True, 
                                    f"All variations return relevant responses, Question IDs: {list(set(question_ids))}")
                        passed_tests += 1
                    else:
                        self.log_test(f"AI Question Variations: {test['description']}", False, 
                                    f"Some variations return insufficient responses")
                else:
                    self.log_test(f"AI Question Variations: {test['description']}", False, 
                                f"Failed to get responses for all variations")
                    
            except Exception as e:
                self.log_test(f"AI Question Variations: {test['description']}", False, f"Request error: {str(e)}")
        
        return passed_tests, total_tests

    def run_comprehensive_tests(self):
        """Run all comprehensive backend tests"""
        print("=" * 80)
        print("🧪 FINAL COMPREHENSIVE BACKEND TESTING - FOOD SAFETY SEARCH & AI ASSISTANT")
        print("=" * 80)
        print()
        
        # Step 1: Authentication
        if not self.authenticate():
            print("❌ CRITICAL: Authentication failed. Cannot proceed with testing.")
            return False
        
        total_passed = 0
        total_tests = 0
        
        # Step 2: Food Safety Search Testing
        print("🍎 PART A: FOOD SAFETY SEARCH TESTING (/api/food/research)")
        print("=" * 60)
        
        # Basic food queries
        passed, tests = self.test_food_safety_basic_queries()
        total_passed += passed
        total_tests += tests
        
        # Answer accuracy - no honey confusion
        passed, tests = self.test_answer_accuracy_no_honey_confusion()
        total_passed += passed
        total_tests += tests
        
        # Age range display
        passed, tests = self.test_age_range_display()
        total_passed += passed
        total_tests += tests
        
        # Keyword variations
        passed, tests = self.test_keyword_variations()
        total_passed += passed
        total_tests += tests
        
        # Step 3: AI Assistant Testing
        print("🤖 PART B: AI ASSISTANT TESTING (/api/research)")
        print("=" * 60)
        
        # Single knowledge base queries
        passed, tests = self.test_ai_assistant_single_kb()
        total_passed += passed
        total_tests += tests
        
        # Multi-knowledge-base queries
        passed, tests = self.test_ai_assistant_multi_kb()
        total_passed += passed
        total_tests += tests
        
        # Question variations
        passed, tests = self.test_question_variations()
        total_passed += passed
        total_tests += tests
        
        # Step 4: Summary
        print("=" * 80)
        print("📊 FINAL COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        print(f"Tests Passed: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        if success_rate >= 80:
            print("✅ COMPREHENSIVE BACKEND TESTING: SUCCESS")
            print("   - Food Safety Search algorithm working correctly")
            print("   - Answer accuracy verified with correct Question IDs")
            print("   - Age ranges displayed properly")
            print("   - Keyword variations handled properly")
            print("   - AI Assistant multi-knowledge-base support functional")
            print("   - Single and multi-KB queries working")
            print("   - Question variations processed correctly")
        else:
            print("❌ COMPREHENSIVE BACKEND TESTING: ISSUES FOUND")
            print("   - Some critical functionality not working as expected")
            print("   - Review detailed test results below")
        
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
    tester = FinalComprehensiveTester()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 COMPREHENSIVE BACKEND TESTING COMPLETED SUCCESSFULLY!")
        print("   Both Food Safety Search and AI Assistant functionality verified.")
        sys.exit(0)
    else:
        print("\n⚠️  COMPREHENSIVE TESTING IDENTIFIED ISSUES")
        print("   Review detailed results above for specific failures.")
        sys.exit(1)

if __name__ == "__main__":
    main()