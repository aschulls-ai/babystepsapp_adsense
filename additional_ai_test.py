#!/usr/bin/env python3
"""
Additional AI Assistant testing for specific baby care scenarios
"""

import requests
import json

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com/api"
TEST_USER_EMAIL = "demo@babysteps.com"
TEST_USER_PASSWORD = "demo123"

def test_specific_queries():
    """Test specific baby care queries"""
    
    # Authenticate first
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
    
    if response.status_code != 200:
        print("❌ Authentication failed")
        return
    
    token_data = response.json()
    auth_token = token_data.get("access_token")
    session.headers.update({
        "Authorization": f"Bearer {auth_token}"
    })
    
    print("✅ Authenticated successfully")
    print()
    
    # Test queries from the review request
    test_queries = [
        {
            "message": "How often should I feed my 6 month old baby?",
            "baby_age_months": 6
        },
        {
            "message": "When can babies start eating solid food?",
            "baby_age_months": 4
        },
        {
            "message": "Is it safe to give honey to a 10 month old baby?",
            "baby_age_months": 10
        },
        {
            "message": "What are good finger foods for a 9 month old?",
            "baby_age_months": 9
        }
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"🤖 Query {i}: {query['message']}")
        
        try:
            response = session.post(
                f"{BACKEND_URL}/ai/chat",
                json=query,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("response", "")
                print(f"✅ Response ({len(ai_response)} chars):")
                print(f"   {ai_response[:200]}...")
                print()
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                print()
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            print()

if __name__ == "__main__":
    test_specific_queries()