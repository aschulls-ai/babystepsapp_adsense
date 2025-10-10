#!/usr/bin/env python3
"""
URGENT FOOD SAFETY RESEARCH INVESTIGATION
Testing specific food queries to verify they return food-specific answers, NOT honey responses
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

class FoodSafetyInvestigator:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 60
        self.auth_token = None
        # Demo credentials as specified in review request
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'critical_issues': [],
            'detailed_responses': {}
        }
    
    def log_result(self, test_name, success, message="", response_text=""):
        """Log test results with detailed response tracking"""
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['critical_issues'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
        
        # Store detailed response for analysis
        if response_text:
            self.results['detailed_responses'][test_name] = response_text
    
    def authenticate(self):
        """Authenticate with demo credentials"""
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
    
    def test_food_safety_query(self, food_name, query, expected_food_keywords, baby_age_months=8):
        """Test a specific food safety query and verify it returns food-specific answers"""
        try:
            food_query = {
                "question": query,
                "baby_age_months": baby_age_months
            }
            
            print(f"\n🔍 Testing: '{query}'")
            print(f"   Expected keywords: {expected_food_keywords}")
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()
                safety_level = data.get('safety_level', 'unknown')
                
                print(f"   Response length: {len(answer)} characters")
                print(f"   Safety level: {safety_level}")
                print(f"   First 200 chars: {answer[:200]}...")
                
                # Check if response contains expected food keywords
                food_keywords_found = []
                for keyword in expected_food_keywords:
                    if keyword.lower() in answer:
                        food_keywords_found.append(keyword)
                
                # Check if response contains honey (which would indicate the bug)
                honey_mentioned = 'honey' in answer
                
                # Analyze the response
                if len(food_keywords_found) > 0:
                    if honey_mentioned and food_name.lower() != 'honey':
                        # This is the bug - food query returning honey information
                        self.log_result(
                            f"Food Safety - {food_name}",
                            False,
                            f"CRITICAL BUG: Query about {food_name} returned honey information. Found {food_name} keywords: {food_keywords_found}, but also mentioned honey",
                            answer
                        )
                        return False
                    else:
                        # Good - food-specific response
                        self.log_result(
                            f"Food Safety - {food_name}",
                            True,
                            f"Returned {food_name}-specific answer with keywords: {food_keywords_found}",
                            answer
                        )
                        return True
                else:
                    # No food-specific keywords found
                    if honey_mentioned:
                        self.log_result(
                            f"Food Safety - {food_name}",
                            False,
                            f"CRITICAL BUG: Query about {food_name} returned honey information instead of {food_name}-specific answer",
                            answer
                        )
                        return False
                    else:
                        self.log_result(
                            f"Food Safety - {food_name}",
                            False,
                            f"No {food_name}-specific keywords found in response. Response may be too generic.",
                            answer
                        )
                        return False
            else:
                self.log_result(
                    f"Food Safety - {food_name}",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    ""
                )
                return False
        except Exception as e:
            self.log_result(
                f"Food Safety - {food_name}",
                False,
                f"Error: {str(e)}",
                ""
            )
            return False
    
    def investigate_food_safety_issue(self):
        """Run the specific food safety queries mentioned in the review request"""
        print("🚨 URGENT FOOD SAFETY RESEARCH INVESTIGATION")
        print("=" * 80)
        print("Testing specific queries that should return food-specific answers, NOT honey")
        print(f"Backend URL: {API_BASE}")
        print(f"Demo user: {self.demo_email}")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate():
            print("❌ Cannot proceed without authentication")
            return self.results
        
        print("\n🔬 CRITICAL FOOD SAFETY QUERIES:")
        print("=" * 80)
        
        # Test the specific queries mentioned in the review request
        test_cases = [
            {
                "food_name": "Avocado",
                "query": "Is avocado safe for babies",
                "expected_keywords": ["avocado", "avocados"],
                "age_months": 8
            },
            {
                "food_name": "Eggs",
                "query": "Can baby eat eggs",
                "expected_keywords": ["egg", "eggs"],
                "age_months": 8
            },
            {
                "food_name": "Strawberries",
                "query": "Are strawberries safe for 8 month old",
                "expected_keywords": ["strawberry", "strawberries", "berry", "berries"],
                "age_months": 8
            },
            {
                "food_name": "Nuts",
                "query": "When can babies have nuts",
                "expected_keywords": ["nut", "nuts", "peanut", "peanuts"],
                "age_months": 10
            },
            {
                "food_name": "Carrots",
                "query": "Are carrots safe for baby",
                "expected_keywords": ["carrot", "carrots"],
                "age_months": 8
            }
        ]
        
        # Run each test case
        for test_case in test_cases:
            success = self.test_food_safety_query(
                test_case["food_name"],
                test_case["query"],
                test_case["expected_keywords"],
                test_case["age_months"]
            )
        
        # Also test honey to make sure it works correctly
        print("\n🍯 CONTROL TEST - HONEY QUERY:")
        print("=" * 40)
        self.test_food_safety_query(
            "Honey",
            "Is honey safe for babies",
            ["honey"],
            8
        )
        
        return self.results
    
    def analyze_results(self):
        """Analyze and report the investigation results"""
        print("\n" + "=" * 80)
        print("🔍 FOOD SAFETY INVESTIGATION ANALYSIS")
        print("=" * 80)
        
        print(f"✅ Tests Passed: {self.results['passed']}")
        print(f"❌ Tests Failed: {self.results['failed']}")
        
        if self.results['critical_issues']:
            print(f"\n🚨 CRITICAL ISSUES FOUND:")
            for issue in self.results['critical_issues']:
                print(f"   • {issue}")
        
        # Check for the specific "only honey" bug
        honey_bug_detected = False
        for issue in self.results['critical_issues']:
            if "returned honey information" in issue and "Query about" in issue:
                honey_bug_detected = True
                break
        
        print(f"\n🎯 ROOT CAUSE ANALYSIS:")
        print("=" * 40)
        
        if honey_bug_detected:
            print("❌ CONFIRMED: 'Only Honey' bug is present")
            print("   • Food-specific queries are returning honey information")
            print("   • Enhanced food matching logic is NOT working correctly")
            print("   • This matches the user's report exactly")
        else:
            print("✅ 'Only Honey' bug NOT detected")
            print("   • Food queries are returning food-specific information")
            print("   • Enhanced food matching appears to be working")
        
        print(f"\n📊 DEBUGGING INFORMATION:")
        print("=" * 40)
        
        # Show sample responses for debugging
        for test_name, response in self.results['detailed_responses'].items():
            print(f"\n{test_name}:")
            print(f"   Response: {response[:300]}...")
        
        return honey_bug_detected

def main():
    """Main investigation execution"""
    investigator = FoodSafetyInvestigator()
    results = investigator.investigate_food_safety_issue()
    honey_bug_detected = investigator.analyze_results()
    
    print(f"\n🏁 INVESTIGATION COMPLETE")
    print("=" * 80)
    
    if honey_bug_detected:
        print("❌ CRITICAL BUG CONFIRMED: Food safety research returning honey results for all foods")
        print("   RECOMMENDATION: Enhanced food matching logic needs immediate investigation")
        exit(1)
    elif results['failed'] > 0:
        print("⚠️  ISSUES FOUND: Some food queries not working as expected")
        print("   RECOMMENDATION: Review food matching implementation")
        exit(1)
    else:
        print("✅ ALL TESTS PASSED: Food safety research working correctly")
        exit(0)

if __name__ == "__main__":
    main()