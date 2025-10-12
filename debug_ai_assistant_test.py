#!/usr/bin/env python3
"""
Debug AI Assistant Matching Algorithm
Investigate specific issues found in the matching algorithm
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

class DebugTester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        
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
    
    def debug_query(self, question, expected_behavior):
        """Debug a specific query to understand the response"""
        print(f"\n🔍 DEBUGGING QUERY: '{question}'")
        print(f"   Expected: {expected_behavior}")
        
        try:
            query_data = {"question": question}
            
            response = self.session.post(
                f"{BACKEND_URL}/research",
                json=query_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ HTTP Error: {response.status_code} - {response.text}")
                return
            
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            
            print(f"📝 Response Length: {len(answer)} characters")
            print(f"📚 Sources: {sources}")
            print(f"📄 Answer Preview: {answer[:300]}...")
            
            # Analyze response characteristics
            has_ai_assistant_source = any("AI Assistant" in str(source) for source in sources)
            has_food_safety_source = any("Food Safety" in str(source) for source in sources)
            has_not_available = "Information Not Available" in answer or "not available" in answer.lower()
            has_combined_sections = "General Parenting Guidance" in answer and "Food Safety Information" in answer
            
            print(f"🔍 Analysis:")
            print(f"   - Has AI Assistant source: {has_ai_assistant_source}")
            print(f"   - Has Food Safety source: {has_food_safety_source}")
            print(f"   - Has 'not available': {has_not_available}")
            print(f"   - Has combined sections: {has_combined_sections}")
            
        except Exception as e:
            print(f"❌ Request error: {str(e)}")
    
    def run_debug_tests(self):
        """Run debug tests for failed cases"""
        print("=" * 80)
        print("🐛 AI ASSISTANT MATCHING ALGORITHM DEBUG")
        print("=" * 80)
        
        if not self.authenticate():
            return False
        
        # Debug the failed test cases
        failed_cases = [
            {
                "question": "What are normal development milestones?",
                "expected": "Should match ai_assistant.json for parenting guidance"
            },
            {
                "question": "Is honey safe for babies?",
                "expected": "Should match food_research.json, not AI Assistant"
            },
            {
                "question": "When can babies eat eggs?",
                "expected": "Should match food_research.json, not AI Assistant"
            },
            {
                "question": "Are strawberries safe for 6 month old?",
                "expected": "Should match food_research.json, not AI Assistant"
            },
            {
                "question": "What baby food can I eat while dieting?",
                "expected": "Should return 'Information Not Available' - adult diet question"
            }
        ]
        
        for case in failed_cases:
            self.debug_query(case["question"], case["expected"])
        
        print("\n" + "=" * 80)
        print("🔍 DEBUG ANALYSIS COMPLETE")
        print("=" * 80)

def main():
    """Main debug execution"""
    tester = DebugTester()
    tester.run_debug_tests()

if __name__ == "__main__":
    main()