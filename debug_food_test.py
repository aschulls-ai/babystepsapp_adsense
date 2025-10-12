#!/usr/bin/env python3
"""
DEBUG FOOD MATCHING ALGORITHM
Investigating specific food matching issues
"""

import requests
import json

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

def authenticate():
    """Authenticate and get token"""
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

def debug_food_query(session, query):
    """Debug a specific food query"""
    print(f"\n🔍 DEBUGGING QUERY: '{query}'")
    print("-" * 50)
    
    query_data = {
        "question": query,
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
        age_recommendation = result.get("age_recommendation", "")
        
        print(f"Status: SUCCESS (200)")
        print(f"Safety Level: {safety_level}")
        print(f"Age Recommendation: {age_recommendation}")
        print(f"Sources: {sources}")
        print(f"Answer Length: {len(answer)} characters")
        print(f"Answer Preview: {answer[:200]}...")
        
        # Extract Question ID
        question_id = "Unknown"
        for source in sources:
            if "Knowledge Base Question ID:" in source:
                question_id = source.split("Knowledge Base Question ID: ")[1].split(",")[0]
                break
        print(f"Question ID: {question_id}")
        
    else:
        print(f"Status: FAILED ({response.status_code})")
        print(f"Error: {response.text}")

def main():
    print("🐛 DEBUG FOOD MATCHING ALGORITHM")
    print("=" * 50)
    
    session = authenticate()
    if not session:
        print("❌ Authentication failed")
        return
    
    # Debug the failing queries
    failing_queries = [
        "can my baby eat strawberries",
        "eggs", 
        "can babies eat eggs",
        "peanuts"
    ]
    
    for query in failing_queries:
        debug_food_query(session, query)
    
    print("\n" + "=" * 50)
    print("🔍 DEBUG COMPLETE")

if __name__ == "__main__":
    main()