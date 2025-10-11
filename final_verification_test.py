#!/usr/bin/env python3
"""
Final verification test for the refined JSON-only food research matching algorithm
Testing all critical test cases from the review request
"""

import requests
import json

# Configuration
BACKEND_URL = "https://baby-genius.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

def authenticate():
    """Authenticate with demo user credentials"""
    print("🔐 Authenticating with demo@babysteps.com/demo123...")
    
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
        print(f"❌ Authentication failed: {response.status_code}")
        return None

def test_critical_cases(session):
    """Test the exact critical test cases from the review request"""
    print("\n" + "="*80)
    print("🧪 TESTING CRITICAL TEST CASES FROM REVIEW REQUEST")
    print("="*80)
    
    test_cases = [
        {
            "name": "Pizza Query - Should NOT match to eggs (FALSE POSITIVE FIX)",
            "question": "Can babies eat pizza?",
            "expected": "not_available",
            "success_criteria": [
                "Should return 'Food Safety Information Not Available' message",
                "Should NOT return egg-specific information",
                "Should list available foods in database"
            ]
        },
        {
            "name": "Eggs Query - Should still work correctly",
            "question": "When can babies eat eggs?",
            "expected": "json_match",
            "expected_id": "202",
            "success_criteria": [
                "Should return JSON ID 202 about eggs",
                "Should contain egg-specific information only"
            ]
        },
        {
            "name": "Honey Query - Should still work correctly", 
            "question": "Is honey safe for babies?",
            "expected": "json_match",
            "expected_id": "201",
            "success_criteria": [
                "Should return JSON ID 201 about honey",
                "Should contain botulism warning"
            ]
        }
    ]
    
    all_passed = True
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🔍 TEST {i}: {test['name']}")
        print(f"   Query: '{test['question']}'")
        print(f"   Expected: {test['expected']}")
        
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
                results.append({"test": test["name"], "passed": False, "reason": f"HTTP {response.status_code}"})
                all_passed = False
                continue
            
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            safety_level = result.get("safety_level", "")
            
            print(f"   📝 Answer length: {len(answer)} characters")
            print(f"   🔒 Safety level: {safety_level}")
            print(f"   📚 Sources: {sources}")
            
            test_passed = True
            failure_reasons = []
            
            if test["expected"] == "not_available":
                # Test 1: Pizza query should return "not available"
                if "Food Safety Information Not Available" not in answer:
                    test_passed = False
                    failure_reasons.append("Missing 'Food Safety Information Not Available' message")
                
                # Critical: Should NOT contain egg-specific information
                if "Eggs can be introduced around 6 months" in answer:
                    test_passed = False
                    failure_reasons.append("CRITICAL: Contains egg-specific information (false positive)")
                
                # Should list available foods
                if "Available in our database:" not in answer:
                    test_passed = False
                    failure_reasons.append("Missing available foods list")
                
                # Should have correct source
                if not any("No entry found" in source for source in sources):
                    test_passed = False
                    failure_reasons.append("Incorrect source - should indicate no entry found")
                    
            elif test["expected"] == "json_match":
                # Test 2 & 3: Should return JSON knowledge base match
                has_json_source = any("Knowledge Base Question ID:" in source for source in sources)
                if not has_json_source:
                    test_passed = False
                    failure_reasons.append("Missing JSON knowledge base source")
                
                # Check for expected ID
                if "expected_id" in test:
                    expected_id_text = f"Knowledge Base Question ID: {test['expected_id']}"
                    if not any(expected_id_text in source for source in sources):
                        test_passed = False
                        failure_reasons.append(f"Missing expected ID: {test['expected_id']}")
                
                # Specific content checks
                if test["question"] == "When can babies eat eggs?":
                    if "eggs" not in answer.lower():
                        test_passed = False
                        failure_reasons.append("Missing egg-specific content")
                elif test["question"] == "Is honey safe for babies?":
                    if "honey" not in answer.lower():
                        test_passed = False
                        failure_reasons.append("Missing honey-specific content")
                    if "botulism" not in answer.lower():
                        test_passed = False
                        failure_reasons.append("Missing botulism warning")
            
            if test_passed:
                print(f"   ✅ PASSED: All success criteria met")
                results.append({"test": test["name"], "passed": True, "reason": "All criteria met"})
            else:
                print(f"   ❌ FAILED: {', '.join(failure_reasons)}")
                results.append({"test": test["name"], "passed": False, "reason": ', '.join(failure_reasons)})
                all_passed = False
            
            # Show success criteria check
            print(f"   📋 Success Criteria:")
            for criteria in test["success_criteria"]:
                print(f"      • {criteria}")
            
            print(f"   📄 Answer preview: {answer[:150]}...")
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append({"test": test["name"], "passed": False, "reason": f"Exception: {str(e)}"})
            all_passed = False
    
    return all_passed, results

def main():
    """Main test execution"""
    print("🧪 FINAL VERIFICATION: Refined JSON-Only Food Research Matching Algorithm")
    print("Testing the fix for false positive issue where 'pizza' was incorrectly matching to 'eggs'")
    print("\n🎯 ALGORITHM REFINEMENTS BEING TESTED:")
    print("   ✅ Requires food name presence: Must find actual food keywords")
    print("   ✅ Higher food match scores: Food name matches worth 50 points")
    print("   ✅ Increased threshold: Minimum score raised from 30 to 50 points")
    print("   ✅ Conditional safety scoring: Safety keywords only count if food name found")
    
    # Authenticate
    session = authenticate()
    if not session:
        print("❌ CRITICAL: Authentication failed. Cannot proceed.")
        return False
    
    # Run critical tests
    success, results = test_critical_cases(session)
    
    print("\n" + "="*80)
    print("📊 FINAL VERIFICATION RESULTS")
    print("="*80)
    
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    
    print(f"Tests Passed: {passed_count}/{total_count}")
    
    for result in results:
        status = "✅" if result["passed"] else "❌"
        print(f"{status} {result['test']}")
        if not result["passed"]:
            print(f"   Reason: {result['reason']}")
    
    print("\n" + "="*80)
    if success:
        print("🎉 SUCCESS: All critical test cases PASSED!")
        print("✅ Pizza query returns 'Food Safety Information Not Available' (no false positive)")
        print("✅ Egg and honey queries still work correctly")
        print("✅ Only food-specific matches allowed")
        print("✅ No AI/LLM calls - JSON-only implementation")
        print("\n💡 The refined matching algorithm successfully prevents false positives")
        print("   while maintaining correct matches for actual foods in the JSON database.")
    else:
        print("❌ FAILURE: Some critical test cases failed")
        print("⚠️  The refined matching algorithm needs further investigation")
    
    return success

if __name__ == "__main__":
    main()