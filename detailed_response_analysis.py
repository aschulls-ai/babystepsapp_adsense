#!/usr/bin/env python3
"""
Detailed Response Analysis for Food Safety Research
Analyze the full responses to understand why honey is being mentioned
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://openai-parent.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def authenticate():
    """Authenticate with demo credentials"""
    session = requests.Session()
    session.timeout = 60
    
    login_data = {
        "email": "demo@babysteps.com",
        "password": "demo123"
    }
    
    response = session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        if 'access_token' in data:
            auth_token = data['access_token']
            session.headers.update({'Authorization': f"Bearer {auth_token}"})
            print(f"✅ Authentication successful")
            return session
        else:
            print(f"❌ Authentication failed: Invalid response format")
            return None
    else:
        print(f"❌ Authentication failed: HTTP {response.status_code} - {response.text}")
        return None

def analyze_food_response(session, food_name, query, baby_age_months=8):
    """Get and analyze a complete food safety response"""
    print(f"\n{'='*80}")
    print(f"ANALYZING: {food_name.upper()} QUERY")
    print(f"Query: '{query}'")
    print(f"Age: {baby_age_months} months")
    print(f"{'='*80}")
    
    food_query = {
        "question": query,
        "baby_age_months": baby_age_months
    }
    
    response = session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get('answer', '')
        safety_level = data.get('safety_level', 'unknown')
        age_recommendation = data.get('age_recommendation', 'N/A')
        sources = data.get('sources', [])
        
        print(f"Response Status: ✅ SUCCESS")
        print(f"Safety Level: {safety_level}")
        print(f"Age Recommendation: {age_recommendation}")
        print(f"Sources: {sources}")
        print(f"Response Length: {len(answer)} characters")
        print(f"\nFULL RESPONSE:")
        print("-" * 80)
        print(answer)
        print("-" * 80)
        
        # Analyze for honey mentions
        answer_lower = answer.lower()
        honey_positions = []
        search_start = 0
        while True:
            pos = answer_lower.find('honey', search_start)
            if pos == -1:
                break
            honey_positions.append(pos)
            search_start = pos + 1
        
        if honey_positions:
            print(f"\n🍯 HONEY MENTIONS FOUND: {len(honey_positions)} occurrences")
            for i, pos in enumerate(honey_positions):
                start = max(0, pos - 50)
                end = min(len(answer), pos + 50)
                context = answer[start:end]
                print(f"   {i+1}. Position {pos}: ...{context}...")
        else:
            print(f"\n✅ NO HONEY MENTIONS FOUND")
        
        # Check for food-specific keywords
        food_keywords = [food_name.lower()]
        if food_name.lower() == 'avocado':
            food_keywords.extend(['avocados'])
        elif food_name.lower() == 'eggs':
            food_keywords.extend(['egg'])
        elif food_name.lower() == 'strawberries':
            food_keywords.extend(['strawberry', 'berry', 'berries'])
        elif food_name.lower() == 'nuts':
            food_keywords.extend(['nut', 'peanut', 'peanuts'])
        elif food_name.lower() == 'carrots':
            food_keywords.extend(['carrot'])
        
        found_keywords = []
        for keyword in food_keywords:
            if keyword in answer_lower:
                found_keywords.append(keyword)
        
        print(f"\n🔍 FOOD-SPECIFIC KEYWORDS FOUND: {found_keywords}")
        
        return {
            'food_name': food_name,
            'query': query,
            'answer': answer,
            'safety_level': safety_level,
            'honey_mentions': len(honey_positions),
            'honey_positions': honey_positions,
            'food_keywords_found': found_keywords,
            'response_length': len(answer)
        }
    else:
        print(f"❌ Request failed: HTTP {response.status_code} - {response.text}")
        return None

def main():
    """Main analysis execution"""
    print("🔬 DETAILED FOOD SAFETY RESPONSE ANALYSIS")
    print("=" * 80)
    print("Investigating why honey is mentioned in food-specific queries")
    print(f"Backend URL: {API_BASE}")
    print("=" * 80)
    
    # Authenticate
    session = authenticate()
    if not session:
        print("❌ Cannot proceed without authentication")
        return
    
    # Test cases from the review request
    test_cases = [
        {
            "food_name": "Avocado",
            "query": "Is avocado safe for babies",
            "age_months": 8
        },
        {
            "food_name": "Eggs",
            "query": "Can baby eat eggs",
            "age_months": 8
        },
        {
            "food_name": "Strawberries",
            "query": "Are strawberries safe for 8 month old",
            "age_months": 8
        },
        {
            "food_name": "Nuts",
            "query": "When can babies have nuts",
            "age_months": 10
        },
        {
            "food_name": "Carrots",
            "query": "Are carrots safe for baby",
            "age_months": 8
        }
    ]
    
    results = []
    
    # Analyze each test case
    for test_case in test_cases:
        result = analyze_food_response(
            session,
            test_case["food_name"],
            test_case["query"],
            test_case["age_months"]
        )
        if result:
            results.append(result)
    
    # Summary analysis
    print(f"\n{'='*80}")
    print("SUMMARY ANALYSIS")
    print(f"{'='*80}")
    
    total_tests = len(results)
    honey_mentions_count = sum(1 for r in results if r['honey_mentions'] > 0)
    
    print(f"Total Tests: {total_tests}")
    print(f"Tests with Honey Mentions: {honey_mentions_count}")
    print(f"Tests without Honey Mentions: {total_tests - honey_mentions_count}")
    
    if honey_mentions_count > 0:
        print(f"\n🚨 CRITICAL ISSUE CONFIRMED:")
        print(f"   • {honey_mentions_count}/{total_tests} food queries mention honey")
        print(f"   • This confirms the user's report of 'only honey results'")
        
        print(f"\n📋 DETAILED BREAKDOWN:")
        for result in results:
            if result['honey_mentions'] > 0:
                print(f"   ❌ {result['food_name']}: {result['honey_mentions']} honey mentions")
            else:
                print(f"   ✅ {result['food_name']}: No honey mentions")
    else:
        print(f"\n✅ NO HONEY ISSUE DETECTED:")
        print(f"   • All food queries returned food-specific responses")
        print(f"   • No inappropriate honey mentions found")
    
    print(f"\n🔧 DEBUGGING RECOMMENDATIONS:")
    if honey_mentions_count > 0:
        print(f"   1. Check if AI system prompt includes honey warnings")
        print(f"   2. Verify food matching logic is working correctly")
        print(f"   3. Review if responses are being contaminated with honey information")
        print(f"   4. Test with different AI model or parameters")
    else:
        print(f"   1. Food safety research appears to be working correctly")
        print(f"   2. Enhanced food matching logic is functioning as expected")

if __name__ == "__main__":
    main()