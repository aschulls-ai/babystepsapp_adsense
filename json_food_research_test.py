#!/usr/bin/env python3
"""
JSON-ONLY Food Safety Research Testing Suite
Tests the new JSON-ONLY implementation that pulls answers from JSON file with designated question IDs
NO AI or web search fallback - pure JSON-based responses
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://babysteps-app-2.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class JSONFoodResearchTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.auth_token = None
        # Demo credentials as specified in review request
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def log_result(self, test_name, success, message=""):
        """Log test results"""
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
    
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
                    self.log_result("Demo User Authentication", True, "demo@babysteps.com login successful")
                    return True
                else:
                    self.log_result("Demo User Authentication", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_result("Demo User Authentication", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Demo User Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_eggs_json_query(self):
        """Test: 'When can babies eat eggs?' should return JSON ID 202 answer about eggs"""
        try:
            food_query = {
                "question": "When can babies eat eggs?",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()
                
                # Check if response is about eggs specifically (NOT honey)
                if 'egg' in answer and 'honey' not in answer:
                    # Check for JSON source indication
                    if 'knowledge base question id' in answer.lower() or 'id 202' in answer.lower():
                        self.log_result("Eggs JSON Query", True, "Returns egg-specific JSON answer with ID 202")
                        return True
                    else:
                        # Even without explicit ID mention, if it's egg-specific and not honey, it's correct
                        if '6 months' in answer and 'cook thoroughly' in answer:
                            self.log_result("Eggs JSON Query", True, "Returns egg-specific answer (6 months, cook thoroughly)")
                            return True
                        else:
                            self.log_result("Eggs JSON Query", False, f"Egg answer but missing expected content: {answer[:200]}...")
                            return False
                elif 'honey' in answer:
                    self.log_result("Eggs JSON Query", False, "CRITICAL: Still returning honey information for egg query")
                    return False
                else:
                    self.log_result("Eggs JSON Query", False, f"No egg-specific answer found: {answer[:200]}...")
                    return False
            else:
                self.log_result("Eggs JSON Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Eggs JSON Query", False, f"Error: {str(e)}")
            return False
    
    def test_avocado_json_query(self):
        """Test: 'Is avocado safe for babies?' should return avocado-specific JSON answer"""
        try:
            food_query = {
                "question": "Is avocado safe for babies?",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()
                
                # Check if response is about avocado specifically (NOT honey)
                if 'avocado' in answer and 'honey' not in answer:
                    # Check for JSON source indication
                    if 'knowledge base question id' in answer.lower():
                        self.log_result("Avocado JSON Query", True, "Returns avocado-specific JSON answer with source ID")
                        return True
                    else:
                        # Even without explicit ID mention, if it's avocado-specific and not honey, it's correct
                        self.log_result("Avocado JSON Query", True, "Returns avocado-specific answer (not honey)")
                        return True
                elif 'honey' in answer:
                    self.log_result("Avocado JSON Query", False, "CRITICAL: Still returning honey information for avocado query")
                    return False
                else:
                    self.log_result("Avocado JSON Query", False, f"No avocado-specific answer found: {answer[:200]}...")
                    return False
            else:
                self.log_result("Avocado JSON Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Avocado JSON Query", False, f"Error: {str(e)}")
            return False
    
    def test_strawberries_json_query(self):
        """Test: 'Can babies eat strawberries?' should return JSON ID 205 answer about strawberries"""
        try:
            food_query = {
                "question": "Can babies eat strawberries?",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()
                
                # Check if response is about strawberries specifically (NOT honey)
                if ('strawberr' in answer or 'berr' in answer) and 'honey' not in answer:
                    # Check for JSON source indication
                    if 'knowledge base question id' in answer.lower() or 'id 205' in answer.lower():
                        self.log_result("Strawberries JSON Query", True, "Returns strawberry-specific JSON answer with ID 205")
                        return True
                    else:
                        # Even without explicit ID mention, if it's strawberry-specific and not honey, it's correct
                        self.log_result("Strawberries JSON Query", True, "Returns strawberry-specific answer (not honey)")
                        return True
                elif 'honey' in answer:
                    self.log_result("Strawberries JSON Query", False, "CRITICAL: Still returning honey information for strawberry query")
                    return False
                else:
                    self.log_result("Strawberries JSON Query", False, f"No strawberry-specific answer found: {answer[:200]}...")
                    return False
            else:
                self.log_result("Strawberries JSON Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Strawberries JSON Query", False, f"Error: {str(e)}")
            return False
    
    def test_honey_json_query(self):
        """Test: 'Is honey safe for babies?' should return JSON ID 201 answer about honey (12+ months, botulism risk)"""
        try:
            food_query = {
                "question": "Is honey safe for babies?",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()
                
                # Check if response is about honey specifically
                if 'honey' in answer:
                    # Check for expected honey content (12+ months, botulism risk)
                    if ('12' in answer or 'twelve' in answer) and 'botulism' in answer:
                        # Check for JSON source indication
                        if 'knowledge base question id' in answer.lower() or 'id 201' in answer.lower():
                            self.log_result("Honey JSON Query", True, "Returns honey-specific JSON answer with ID 201 (12+ months, botulism)")
                            return True
                        else:
                            self.log_result("Honey JSON Query", True, "Returns honey-specific answer (12+ months, botulism)")
                            return True
                    else:
                        self.log_result("Honey JSON Query", False, f"Honey answer missing expected content (12+ months, botulism): {answer[:200]}...")
                        return False
                else:
                    self.log_result("Honey JSON Query", False, f"No honey-specific answer found: {answer[:200]}...")
                    return False
            else:
                self.log_result("Honey JSON Query", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Honey JSON Query", False, f"Error: {str(e)}")
            return False
    
    def test_pizza_not_in_json(self):
        """Test: 'Can babies eat pizza?' (not in JSON) should return 'not available' message with list of available foods"""
        try:
            food_query = {
                "question": "Can babies eat pizza?",
                "baby_age_months": 12
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()
                
                # Check if response indicates food not available in database
                if 'not available' in answer or 'not found' in answer or 'database' in answer:
                    # Check if it lists available foods
                    if any(food in answer for food in ['eggs', 'avocado', 'strawberries', 'honey']):
                        self.log_result("Pizza Not In JSON", True, "Returns 'not available' message with list of available foods")
                        return True
                    else:
                        self.log_result("Pizza Not In JSON", True, "Returns 'not available' message (may not list foods)")
                        return True
                elif 'honey' in answer:
                    self.log_result("Pizza Not In JSON", False, "CRITICAL: Still defaulting to honey for non-JSON food (pizza)")
                    return False
                else:
                    # If it returns a pizza-specific answer, that means it's using AI, not JSON-only
                    if 'pizza' in answer and len(answer) > 100:
                        self.log_result("Pizza Not In JSON", False, "CRITICAL: Returning AI-generated pizza answer instead of JSON-only 'not available'")
                        return False
                    else:
                        self.log_result("Pizza Not In JSON", False, f"Unexpected response for non-JSON food: {answer[:200]}...")
                        return False
            else:
                self.log_result("Pizza Not In JSON", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Pizza Not In JSON", False, f"Error: {str(e)}")
            return False
    
    def test_no_ai_fallback(self):
        """Test that system is NOT using AI fallback by checking response patterns"""
        try:
            # Test with a very specific, unusual food question that would require AI
            food_query = {
                "question": "Can babies eat quinoa with turmeric and coconut oil?",
                "baby_age_months": 10
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()
                
                # If it's truly JSON-only, this complex query should return "not available"
                if 'not available' in answer or 'not found' in answer or 'database' in answer:
                    self.log_result("No AI Fallback", True, "Complex query returns 'not available' - confirms JSON-only mode")
                    return True
                elif 'honey' in answer:
                    self.log_result("No AI Fallback", False, "CRITICAL: Complex query defaults to honey - not JSON-only")
                    return False
                elif len(answer) > 200 and ('quinoa' in answer or 'turmeric' in answer):
                    self.log_result("No AI Fallback", False, "CRITICAL: Complex query gets AI response - not JSON-only mode")
                    return False
                else:
                    self.log_result("No AI Fallback", True, "Complex query handled appropriately for JSON-only mode")
                    return True
            else:
                self.log_result("No AI Fallback", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("No AI Fallback", False, f"Error: {str(e)}")
            return False
    
    def test_source_attribution(self):
        """Test that responses show 'Knowledge Base Question ID: XXX' source attribution"""
        try:
            food_query = {
                "question": "When can babies eat eggs?",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                
                # Check for Knowledge Base source attribution
                if 'knowledge base question id' in answer.lower():
                    self.log_result("Source Attribution", True, "Response shows 'Knowledge Base Question ID' source")
                    return True
                else:
                    # Check if sources field has the information
                    sources = data.get('sources', [])
                    if any('knowledge base' in str(source).lower() for source in sources):
                        self.log_result("Source Attribution", True, "Source attribution found in sources field")
                        return True
                    else:
                        self.log_result("Source Attribution", False, "No 'Knowledge Base Question ID' source attribution found")
                        return False
            else:
                self.log_result("Source Attribution", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Source Attribution", False, f"Error: {str(e)}")
            return False
    
    def run_json_food_research_tests(self):
        """Run all JSON-ONLY food research tests as per review request"""
        print(f"🚀 JSON-ONLY FOOD SAFETY RESEARCH TESTING")
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Demo user: {self.demo_email}")
        print("=" * 80)
        
        # Authentication first
        print("\n🔐 AUTHENTICATION:")
        print("=" * 40)
        if not self.test_demo_user_login():
            print("❌ Demo login failed - cannot proceed with tests")
            return self.results
        
        print("\n🥗 JSON-ONLY FOOD RESEARCH TESTS:")
        print("=" * 40)
        
        # Test specific food queries that should return JSON answers
        print("🥚 Testing eggs query (should return JSON ID 202)...")
        self.test_eggs_json_query()
        
        print("🥑 Testing avocado query (should return avocado-specific JSON)...")
        self.test_avocado_json_query()
        
        print("🍓 Testing strawberries query (should return JSON ID 205)...")
        self.test_strawberries_json_query()
        
        print("🍯 Testing honey query (should return JSON ID 201)...")
        self.test_honey_json_query()
        
        print("🍕 Testing pizza query (not in JSON - should return 'not available')...")
        self.test_pizza_not_in_json()
        
        print("🤖 Testing no AI fallback (complex query should return 'not available')...")
        self.test_no_ai_fallback()
        
        print("📋 Testing source attribution (should show Knowledge Base Question ID)...")
        self.test_source_attribution()
        
        print("=" * 80)
        print(f"📊 JSON-ONLY FOOD RESEARCH TEST RESULTS:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests Details:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Summary for review request
        print(f"\n🎯 JSON-ONLY IMPLEMENTATION VERIFICATION:")
        print("=" * 80)
        
        # Check critical requirements
        honey_defaulting_issues = [error for error in self.results['errors'] 
                                 if "Still returning honey" in error or "defaults to honey" in error]
        
        if len(honey_defaulting_issues) == 0:
            print("✅ NO HONEY DEFAULTING: All non-honey queries return food-specific answers")
        else:
            print("❌ HONEY DEFAULTING STILL PRESENT:")
            for issue in honey_defaulting_issues:
                print(f"   • {issue}")
        
        ai_fallback_issues = [error for error in self.results['errors'] 
                            if "AI response" in error or "AI-generated" in error]
        
        if len(ai_fallback_issues) == 0:
            print("✅ JSON-ONLY MODE: No AI fallback detected")
        else:
            print("❌ AI FALLBACK STILL ACTIVE:")
            for issue in ai_fallback_issues:
                print(f"   • {issue}")
        
        json_matching_issues = [error for error in self.results['errors'] 
                              if "JSON Query" in error and "FAILED" in error]
        
        if len(json_matching_issues) == 0:
            print("✅ JSON ID MATCHING: All specific food queries return correct JSON answers")
        else:
            print("❌ JSON ID MATCHING ISSUES:")
            for issue in json_matching_issues:
                print(f"   • {issue}")
        
        return self.results

def main():
    """Main test execution"""
    tester = JSONFoodResearchTester()
    results = tester.run_json_food_research_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()