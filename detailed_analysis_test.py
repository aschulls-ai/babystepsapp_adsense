#!/usr/bin/env python3
"""
Detailed analysis of the pizza vs eggs false positive issue
"""

import requests
import json

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

def authenticate():
    """Authenticate with demo user credentials"""
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
        return session
    return None

def analyze_pizza_query(session):
    """Analyze the pizza query in detail"""
    print("🔍 DETAILED ANALYSIS: Pizza Query")
    print("="*50)
    
    query_data = {
        "question": "Can babies eat pizza?",
        "baby_age_months": 8
    }
    
    response = session.post(
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
        
        print(f"📝 Full Answer:")
        print(answer)
        print(f"\n🔒 Safety Level: {safety_level}")
        print(f"📚 Sources: {sources}")
        
        # Check if this is actually matching to eggs content or just listing eggs as available
        print(f"\n🔍 Analysis:")
        print(f"   - Contains 'Food Safety Information Not Available': {'✅' if 'Food Safety Information Not Available' in answer else '❌'}")
        print(f"   - Contains 'Available in our database': {'✅' if 'Available in our database:' in answer else '❌'}")
        print(f"   - Contains egg-specific safety info: {'❌' if 'Eggs can be introduced around 6 months' not in answer else '✅ PROBLEM!'}")
        print(f"   - Sources indicate no match found: {'✅' if 'No entry found' in str(sources) else '❌'}")
        
        # The key question: Is this returning egg-specific information or just listing eggs as available?
        if "Eggs can be introduced around 6 months" in answer:
            print("\n❌ CRITICAL ISSUE: Pizza query is returning egg-specific safety information!")
            print("   This indicates the false positive matching issue is NOT fixed.")
            return False
        elif "• Eggs (6+ months)" in answer:
            print("\n✅ CORRECT BEHAVIOR: Pizza query returns 'not available' and lists eggs as an available food in database.")
            print("   This is NOT a false positive - it's correctly showing what foods ARE available.")
            return True
        else:
            print("\n⚠️  UNCLEAR: Need to investigate further.")
            return False
    
    return False

def compare_with_eggs_query(session):
    """Compare pizza query with actual eggs query"""
    print("\n🔍 COMPARISON: Pizza vs Eggs Query")
    print("="*50)
    
    queries = [
        {"name": "Pizza Query", "question": "Can babies eat pizza?"},
        {"name": "Eggs Query", "question": "When can babies eat eggs?"}
    ]
    
    for query_info in queries:
        print(f"\n📋 {query_info['name']}: '{query_info['question']}'")
        
        query_data = {
            "question": query_info["question"],
            "baby_age_months": 8
        }
        
        response = session.post(
            f"{BACKEND_URL}/food/research",
            json=query_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            
            print(f"   📝 Answer (first 150 chars): {answer[:150]}...")
            print(f"   📚 Sources: {sources}")
            
            # Check for specific indicators
            has_specific_egg_info = "Eggs can be introduced around 6 months" in answer
            has_not_available_msg = "Food Safety Information Not Available" in answer
            has_json_id = any("Knowledge Base Question ID:" in source for source in sources)
            
            print(f"   🥚 Has specific egg info: {'✅' if has_specific_egg_info else '❌'}")
            print(f"   ❓ Has 'not available' msg: {'✅' if has_not_available_msg else '❌'}")
            print(f"   🆔 Has JSON Question ID: {'✅' if has_json_id else '❌'}")

def main():
    """Main analysis"""
    print("🧪 DETAILED ANALYSIS: Pizza vs Eggs False Positive Issue")
    print("Investigating whether pizza is incorrectly matching to eggs")
    
    session = authenticate()
    if not session:
        print("❌ Authentication failed")
        return
    
    # Analyze pizza query
    pizza_correct = analyze_pizza_query(session)
    
    # Compare queries
    compare_with_eggs_query(session)
    
    print("\n" + "="*80)
    print("📊 CONCLUSION")
    print("="*80)
    
    if pizza_correct:
        print("🎉 SUCCESS: The false positive issue appears to be FIXED!")
        print("✅ Pizza query correctly returns 'Food Safety Information Not Available'")
        print("✅ Pizza query does NOT return egg-specific safety information")
        print("✅ The mention of 'Eggs' is only in the available foods list, which is correct behavior")
        print("\n💡 The original issue was pizza matching to egg-specific content.")
        print("   Now pizza correctly shows 'not available' and lists what IS available.")
    else:
        print("❌ ISSUE: The false positive problem may still exist")
        print("⚠️  Pizza query is returning egg-specific information instead of 'not available'")

if __name__ == "__main__":
    main()