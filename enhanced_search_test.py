#!/usr/bin/env python3
"""
Enhanced Knowledge Base Search Testing Suite for Baby Steps
Tests the specific improvements mentioned in the review request:
1. Removed unnecessary text (no more "source" info or "always consult pediatrician" text)
2. Enhanced food matching (better keyword extraction for foods)
3. Improved question variations (handle different ways of asking same questions)
4. Expanded food aliases (more comprehensive food matching)
"""

import requests
import json
import time
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://baby-steps-demo-api.onrender.com')
API_BASE = f"{BACKEND_URL}/api"

class EnhancedSearchTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 60  # Longer timeout for AI responses
        self.auth_token = None
        # Demo user credentials for testing
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': [],
            'detailed_results': {}
        }
    
    def log_result(self, test_name, success, message="", details=None):
        """Log test results with detailed information"""
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
        
        if details:
            self.results['detailed_results'][test_name] = details
    
    def authenticate(self):
        """Authenticate with demo user"""
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    print(f"✅ Authentication successful with {self.demo_email}")
                    return True
                else:
                    print(f"❌ Authentication failed: Invalid response format")
                    return False
            else:
                print(f"❌ Authentication failed: HTTP {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def test_food_research_enhanced_matching(self):
        """Test enhanced food matching for Food Research engine"""
        print("\n🥗 TESTING FOOD RESEARCH - Enhanced Food Matching")
        print("=" * 60)
        
        # Test cases from review request - should NOT only return honey
        test_cases = [
            {
                "query": "Is avocado safe for babies",
                "expected_food": "avocado",
                "baby_age_months": 8,
                "description": "Should find avocado-specific answer"
            },
            {
                "query": "Can baby eat eggs",
                "expected_food": "egg",
                "baby_age_months": 10,
                "description": "Should find egg-specific answer"
            },
            {
                "query": "Are strawberries safe for 8 month old",
                "expected_food": "strawberry",
                "baby_age_months": 8,
                "description": "Should find berry/strawberry answer"
            },
            {
                "query": "When can babies have nuts",
                "expected_food": "nut",
                "baby_age_months": 12,
                "description": "Should find nut/peanut answer"
            },
            {
                "query": "Is honey safe for baby",
                "expected_food": "honey",
                "baby_age_months": 6,
                "description": "Should find honey answer"
            }
        ]
        
        passed_tests = 0
        total_tests = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}/{total_tests}: {test_case['description']}")
            print(f"Query: '{test_case['query']}'")
            
            try:
                food_query = {
                    "question": test_case['query'],
                    "baby_age_months": test_case['baby_age_months']
                }
                
                response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get('answer', '').lower()
                    safety_level = data.get('safety_level', '')
                    
                    # Check if response is about the expected food
                    expected_food = test_case['expected_food'].lower()
                    food_mentioned = expected_food in answer
                    
                    # Check for clean answer (no unnecessary text)
                    has_source_text = any(phrase in answer for phrase in [
                        'source:', 'sources:', 'according to', 'reference:'
                    ])
                    has_pediatrician_text = 'always consult' in answer and 'pediatrician' in answer
                    
                    # Evaluate results
                    if food_mentioned and not has_source_text and not has_pediatrician_text:
                        print(f"   ✅ Found {expected_food}-specific answer")
                        print(f"   ✅ Clean answer (no source/pediatrician text)")
                        print(f"   ✅ Safety level: {safety_level}")
                        passed_tests += 1
                    else:
                        issues = []
                        if not food_mentioned:
                            issues.append(f"Expected '{expected_food}' not found in answer")
                        if has_source_text:
                            issues.append("Contains source attribution text")
                        if has_pediatrician_text:
                            issues.append("Contains 'always consult pediatrician' text")
                        
                        print(f"   ❌ Issues: {'; '.join(issues)}")
                        print(f"   📝 Answer preview: {answer[:200]}...")
                    
                    # Store detailed results
                    self.results['detailed_results'][f"Food_Research_Test_{i}"] = {
                        'query': test_case['query'],
                        'expected_food': expected_food,
                        'food_mentioned': food_mentioned,
                        'has_source_text': has_source_text,
                        'has_pediatrician_text': has_pediatrician_text,
                        'safety_level': safety_level,
                        'answer_length': len(answer),
                        'answer_preview': answer[:300]
                    }
                    
                else:
                    print(f"   ❌ API Error: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            # Small delay between requests
            time.sleep(1)
        
        success_rate = (passed_tests / total_tests) * 100
        self.log_result(
            "Food Research Enhanced Matching", 
            passed_tests == total_tests,
            f"{passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)"
        )
        
        return passed_tests == total_tests
    
    def test_ai_assistant_question_variations(self):
        """Test AI Assistant handling of question variations"""
        print("\n🤖 TESTING AI ASSISTANT - Question Variations")
        print("=" * 60)
        
        # Test cases for different ways of asking same questions
        test_cases = [
            {
                "queries": [
                    "How much should baby sleep",
                    "Baby won't sleep",
                    "How many hours of sleep does baby need"
                ],
                "topic": "sleep",
                "description": "Should handle different sleep-related questions"
            },
            {
                "queries": [
                    "How often to feed newborn",
                    "When should I feed my baby",
                    "Baby feeding schedule"
                ],
                "topic": "feeding",
                "description": "Should handle different feeding questions"
            },
            {
                "queries": [
                    "When to burp baby",
                    "How to burp newborn",
                    "Baby burping techniques"
                ],
                "topic": "burping",
                "description": "Should handle different burping/feeding questions"
            }
        ]
        
        passed_tests = 0
        total_tests = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}/{total_tests}: {test_case['description']}")
            print(f"Topic: {test_case['topic']}")
            
            responses = []
            topic_mentioned_count = 0
            clean_answers_count = 0
            
            for j, query in enumerate(test_case['queries']):
                print(f"   Query {j+1}: '{query}'")
                
                try:
                    research_query = {"question": query}
                    response = self.session.post(f"{API_BASE}/research", json=research_query, timeout=60)
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get('answer', '').lower()
                        
                        # Check if topic is mentioned
                        topic_mentioned = test_case['topic'] in answer
                        if topic_mentioned:
                            topic_mentioned_count += 1
                            print(f"      ✅ {test_case['topic']} topic addressed")
                        else:
                            print(f"      ❌ {test_case['topic']} topic not clearly addressed")
                        
                        # Check for clean answer
                        has_source_text = any(phrase in answer for phrase in [
                            'source:', 'sources:', 'according to', 'reference:'
                        ])
                        has_pediatrician_text = 'always consult' in answer and 'pediatrician' in answer
                        
                        if not has_source_text and not has_pediatrician_text:
                            clean_answers_count += 1
                            print(f"      ✅ Clean answer (no unnecessary text)")
                        else:
                            print(f"      ❌ Contains unnecessary text")
                        
                        responses.append({
                            'query': query,
                            'answer_length': len(answer),
                            'topic_mentioned': topic_mentioned,
                            'clean_answer': not has_source_text and not has_pediatrician_text,
                            'answer_preview': answer[:200]
                        })
                        
                    else:
                        print(f"      ❌ API Error: HTTP {response.status_code}")
                        
                except Exception as e:
                    print(f"      ❌ Error: {str(e)}")
                
                time.sleep(1)
            
            # Evaluate test case
            if topic_mentioned_count >= 2 and clean_answers_count >= 2:
                print(f"   ✅ Test passed: {topic_mentioned_count}/3 queries addressed topic, {clean_answers_count}/3 clean answers")
                passed_tests += 1
            else:
                print(f"   ❌ Test failed: {topic_mentioned_count}/3 queries addressed topic, {clean_answers_count}/3 clean answers")
            
            # Store detailed results
            self.results['detailed_results'][f"AI_Assistant_Test_{i}"] = {
                'topic': test_case['topic'],
                'responses': responses,
                'topic_mentioned_count': topic_mentioned_count,
                'clean_answers_count': clean_answers_count
            }
        
        success_rate = (passed_tests / total_tests) * 100
        self.log_result(
            "AI Assistant Question Variations",
            passed_tests == total_tests,
            f"{passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)"
        )
        
        return passed_tests == total_tests
    
    def test_meal_planner_clean_format(self):
        """Test Meal Planner clean recipe format"""
        print("\n🍽️ TESTING MEAL PLANNER - Clean Recipe Format")
        print("=" * 60)
        
        test_cases = [
            {
                "query": "breakfast ideas for 6 month old",
                "baby_age_months": 6,
                "description": "Should return clean recipe without source text"
            },
            {
                "query": "lunch ideas for 9 month old",
                "baby_age_months": 9,
                "description": "Should return clean recipe format"
            },
            {
                "query": "dinner recipes for toddler",
                "baby_age_months": 15,
                "description": "Should return clean recipe format for toddler"
            }
        ]
        
        passed_tests = 0
        total_tests = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}/{total_tests}: {test_case['description']}")
            print(f"Query: '{test_case['query']}'")
            
            try:
                meal_query = {
                    "query": test_case['query'],
                    "baby_age_months": test_case['baby_age_months']
                }
                
                response = self.session.post(f"{API_BASE}/meals/search", json=meal_query, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', '').lower()
                    
                    # Check for clean format (no source attribution)
                    has_source_text = any(phrase in results for phrase in [
                        'source:', 'sources:', 'according to', 'reference:', 'cited from'
                    ])
                    
                    # Check for recipe content
                    has_recipe_content = any(word in results for word in [
                        'recipe', 'ingredients', 'instructions', 'prepare', 'cook', 'serve'
                    ])
                    
                    # Check for age-appropriate content
                    age_appropriate = str(test_case['baby_age_months']) in results or any(
                        age_term in results for age_term in ['month', 'baby', 'infant', 'toddler']
                    )
                    
                    # Evaluate results
                    if not has_source_text and has_recipe_content and age_appropriate:
                        print(f"   ✅ Clean recipe format (no source text)")
                        print(f"   ✅ Contains recipe content")
                        print(f"   ✅ Age-appropriate content")
                        passed_tests += 1
                    else:
                        issues = []
                        if has_source_text:
                            issues.append("Contains source attribution text")
                        if not has_recipe_content:
                            issues.append("Missing recipe content")
                        if not age_appropriate:
                            issues.append("Not age-appropriate")
                        
                        print(f"   ❌ Issues: {'; '.join(issues)}")
                    
                    print(f"   📝 Response length: {len(results)} characters")
                    print(f"   📝 Preview: {results[:200]}...")
                    
                    # Store detailed results
                    self.results['detailed_results'][f"Meal_Planner_Test_{i}"] = {
                        'query': test_case['query'],
                        'baby_age_months': test_case['baby_age_months'],
                        'has_source_text': has_source_text,
                        'has_recipe_content': has_recipe_content,
                        'age_appropriate': age_appropriate,
                        'response_length': len(results),
                        'response_preview': results[:300]
                    }
                    
                else:
                    print(f"   ❌ API Error: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            time.sleep(1)
        
        success_rate = (passed_tests / total_tests) * 100
        self.log_result(
            "Meal Planner Clean Format",
            passed_tests == total_tests,
            f"{passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)"
        )
        
        return passed_tests == total_tests
    
    def test_expanded_food_aliases(self):
        """Test expanded food aliases functionality"""
        print("\n🔄 TESTING EXPANDED FOOD ALIASES")
        print("=" * 60)
        
        # Test food aliases (nut=peanut, berry=strawberry, etc.)
        alias_tests = [
            {
                "query": "Are nuts safe for baby",
                "expected_foods": ["nut", "peanut"],
                "description": "nut should match peanut"
            },
            {
                "query": "Can baby have berries",
                "expected_foods": ["berry", "strawberry", "blueberry"],
                "description": "berry should match specific berries"
            },
            {
                "query": "Is fish safe for babies",
                "expected_foods": ["fish", "salmon", "tuna"],
                "description": "fish should match specific fish types"
            }
        ]
        
        passed_tests = 0
        total_tests = len(alias_tests)
        
        for i, test_case in enumerate(alias_tests, 1):
            print(f"\n🔍 Test {i}/{total_tests}: {test_case['description']}")
            print(f"Query: '{test_case['query']}'")
            
            try:
                food_query = {
                    "question": test_case['query'],
                    "baby_age_months": 10
                }
                
                response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get('answer', '').lower()
                    
                    # Check if any expected foods are mentioned
                    foods_mentioned = []
                    for food in test_case['expected_foods']:
                        if food.lower() in answer:
                            foods_mentioned.append(food)
                    
                    if foods_mentioned:
                        print(f"   ✅ Food aliases working: {', '.join(foods_mentioned)} mentioned")
                        passed_tests += 1
                    else:
                        print(f"   ❌ No expected foods mentioned: {test_case['expected_foods']}")
                        print(f"   📝 Answer preview: {answer[:200]}...")
                    
                    # Store detailed results
                    self.results['detailed_results'][f"Food_Aliases_Test_{i}"] = {
                        'query': test_case['query'],
                        'expected_foods': test_case['expected_foods'],
                        'foods_mentioned': foods_mentioned,
                        'answer_preview': answer[:300]
                    }
                    
                else:
                    print(f"   ❌ API Error: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            time.sleep(1)
        
        success_rate = (passed_tests / total_tests) * 100
        self.log_result(
            "Expanded Food Aliases",
            passed_tests == total_tests,
            f"{passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)"
        )
        
        return passed_tests == total_tests
    
    def run_comprehensive_enhanced_search_tests(self):
        """Run all enhanced search improvement tests"""
        print("🚀 ENHANCED KNOWLEDGE BASE SEARCH TESTING")
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Demo user: {self.demo_email}")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate():
            print("❌ Authentication failed - cannot proceed with tests")
            return self.results
        
        print("\n🎯 TESTING ENHANCED SEARCH IMPROVEMENTS")
        print("Key improvements being tested:")
        print("1. ✨ Removed unnecessary text (no source info or 'always consult pediatrician')")
        print("2. 🥗 Enhanced food matching (better keyword extraction)")
        print("3. ❓ Improved question variations (different ways of asking)")
        print("4. 🔄 Expanded food aliases (comprehensive food matching)")
        print("=" * 80)
        
        # Run all test suites
        test_results = []
        
        # Test 1: Food Research Enhanced Matching
        test_results.append(self.test_food_research_enhanced_matching())
        
        # Test 2: AI Assistant Question Variations
        test_results.append(self.test_ai_assistant_question_variations())
        
        # Test 3: Meal Planner Clean Format
        test_results.append(self.test_meal_planner_clean_format())
        
        # Test 4: Expanded Food Aliases
        test_results.append(self.test_expanded_food_aliases())
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 ENHANCED SEARCH TESTING SUMMARY")
        print("=" * 80)
        print(f"✅ Total Passed: {self.results['passed']}")
        print(f"❌ Total Failed: {self.results['failed']}")
        print(f"📈 Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Specific findings for review request
        print(f"\n🎯 REVIEW REQUEST FINDINGS:")
        print("=" * 80)
        
        all_tests_passed = all(test_results)
        
        if all_tests_passed:
            print("✅ ALL ENHANCED SEARCH IMPROVEMENTS VERIFIED:")
            print("   • Food Research returns different foods (not just honey)")
            print("   • AI Assistant handles question variations properly")
            print("   • Meal Planner shows clean recipe format")
            print("   • Expanded food aliases working correctly")
            print("   • Clean answers without source attribution")
            print("   • No unnecessary 'always consult pediatrician' text")
        else:
            print("❌ SOME ENHANCED SEARCH IMPROVEMENTS NEED ATTENTION:")
            failed_areas = []
            if not test_results[0]:
                failed_areas.append("Food Research enhanced matching")
            if not test_results[1]:
                failed_areas.append("AI Assistant question variations")
            if not test_results[2]:
                failed_areas.append("Meal Planner clean format")
            if not test_results[3]:
                failed_areas.append("Expanded food aliases")
            
            for area in failed_areas:
                print(f"   • {area}")
        
        return self.results

def main():
    """Main test execution"""
    tester = EnhancedSearchTester()
    results = tester.run_comprehensive_enhanced_search_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()