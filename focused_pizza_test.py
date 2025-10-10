#!/usr/bin/env python3
"""
Focused test for the refined JSON-only food research matching algorithm
Testing the specific critical test cases mentioned in the review request
"""

import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "https://parental-copilot.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

def authenticate():
    """Authenticate with demo user credentials"""
    print("🔐 Authenticating with demo@babysteps.com...")
    
    session = requests.Session()
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = session.post(
        f"{BACKEND_URL}/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    if response.status_code == 200:
        token_data = response.json()
        auth_token = token_data.get("access_token")
        session.headers.update({
            "Authorization": f"Bearer {auth_token}"
        })
        print("✅ Authentication successful")
        return session
    else:
        print(f"❌ Authentication failed: {response.status_code} - {response.text}")
        return None

def test_critical_cases(session):
    """Test the critical test cases from the review request"""
    print("\n" + "="*80)
    print("🧪 TESTING CRITICAL CASES FROM REVIEW REQUEST")
    print("="*80)
    
    critical_tests = [
        {
            "name": "Pizza Query (Should NOT match to eggs)",
            "question": "Can babies eat pizza?",
            "expected_result": "not_available",
            "should_not_contain": ["eggs", "egg"]
        },
        {
            "name": "Eggs Query (Should work correctly)",
            "question": "When can babies eat eggs?", 
            "expected_result": "json_match",
            "expected_id": "202",
            "should_contain": ["eggs", "egg"]
        },
        {
            "name": "Honey Query (Should work correctly)",
            "question": "Is honey safe for babies?",
            "expected_result": "json_match", 
            "expected_id": "201",
            "should_contain": ["honey"]
        }
    ]
    
    all_passed = True
    
    for test in critical_tests:
        print(f"\n🔍 TESTING: {test['name']}")
        print(f"   Query: '{test['question']}'")
        
        try:
            query_data = {
                "question": test["question"],
                "baby_age_months": 8
            }
            
            response = session.post(
                f"{BACKEND_URL}/food/research",
                json=query_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   ❌ HTTP Error: {response.status_code}")
                all_passed = False
                continue
            
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            safety_level = result.get("safety_level", "")
            
            print(f"   📝 Answer length: {len(answer)} characters")
            print(f"   🔒 Safety level: {safety_level}")
            print(f"   📚 Sources: {sources}")
            
            # Test based on expected result type
            if test["expected_result"] == "not_available":
                # Should return "not available" message
                if "Food Safety Information Not Available" in answer:
                    print("   ✅ Correctly returned 'not available' message")
                    
                    # Check that it doesn't contain forbidden content
                    if "should_not_contain" in test:
                        contains_forbidden = any(forbidden.lower() in answer.lower() 
                                               for forbidden in test["should_not_contain"])
                        if contains_forbidden:
                            print(f"   ❌ CRITICAL: Contains forbidden content: {test['should_not_contain']}")
                            print(f"   📄 Answer excerpt: {answer[:300]}...")
                            all_passed = False
                        else:
                            print(f"   ✅ Does NOT contain forbidden content: {test['should_not_contain']}")
                    
                    # Check for available foods list
                    if "Available in our database:" in answer:
                        print("   ✅ Contains available foods list")
                    else:
                        print("   ⚠️  Missing available foods list")
                        
                else:
                    print("   ❌ FAILED: Expected 'not available' message not found")
                    print(f"   📄 Answer excerpt: {answer[:300]}...")
                    all_passed = False
                    
            elif test["expected_result"] == "json_match":
                # Should return JSON knowledge base match
                has_json_source = any("Knowledge Base Question ID:" in source for source in sources)
                if has_json_source:
                    print("   ✅ Has JSON knowledge base source")
                    
                    # Check for expected ID
                    if "expected_id" in test:
                        expected_id_text = f"Knowledge Base Question ID: {test['expected_id']}"
                        if any(expected_id_text in source for source in sources):
                            print(f"   ✅ Contains expected ID: {test['expected_id']}")
                        else:
                            print(f"   ❌ Missing expected ID: {test['expected_id']}")
                            all_passed = False
                    
                    # Check for expected content
                    if "should_contain" in test:
                        contains_expected = any(expected.lower() in answer.lower() 
                                              for expected in test["should_contain"])
                        if contains_expected:
                            print(f"   ✅ Contains expected content: {test['should_contain']}")
                        else:
                            print(f"   ❌ Missing expected content: {test['should_contain']}")
                            print(f"   📄 Answer excerpt: {answer[:300]}...")
                            all_passed = False
                            
                else:
                    print("   ❌ FAILED: No JSON knowledge base source found")
                    print(f"   📚 Sources: {sources}")
                    all_passed = False
            
            print(f"   📄 Full answer preview: {answer[:200]}...")
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    """Main test execution"""
    print("🧪 FOCUSED TEST: Refined JSON-Only Food Research Matching Algorithm")
    print("Testing the fix for false positive issue where 'pizza' was matching to 'eggs'")
    
    # Authenticate
    session = authenticate()
    if not session:
        print("❌ CRITICAL: Authentication failed. Cannot proceed.")
        return False
    
    # Run critical tests
    success = test_critical_cases(session)
    
    print("\n" + "="*80)
    print("📊 FINAL RESULTS")
    print("="*80)
    
    if success:
        print("🎉 SUCCESS: All critical test cases passed!")
        print("✅ Pizza query correctly returns 'not available' (no false positive)")
        print("✅ Egg query correctly returns JSON ID 202")
        print("✅ Honey query correctly returns JSON ID 201")
        print("✅ Refined matching algorithm working correctly")
    else:
        print("❌ FAILURE: Some critical test cases failed")
        print("⚠️  The refined matching algorithm needs further investigation")
    
    return success

if __name__ == "__main__":
    main()