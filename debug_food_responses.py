#!/usr/bin/env python3
"""
Debug script to see actual food research responses
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

def test_food_responses():
    session = requests.Session()
    session.timeout = 30
    
    # Login first
    login_data = {
        "email": "demo@babysteps.com",
        "password": "demo123"
    }
    
    response = session.post(f"{API_BASE}/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        auth_token = data['access_token']
        session.headers.update({'Authorization': f"Bearer {auth_token}"})
        print("✅ Authentication successful")
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        return
    
    # Test queries
    queries = [
        "When can babies eat eggs?",
        "Is avocado safe for babies?", 
        "Can babies eat strawberries?",
        "Is honey safe for babies?",
        "Can babies eat pizza?"
    ]
    
    for query in queries:
        print(f"\n🔍 Testing: '{query}'")
        print("=" * 60)
        
        food_query = {
            "question": query,
            "baby_age_months": 8
        }
        
        try:
            response = session.post(f"{API_BASE}/food/research", json=food_query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                safety_level = data.get('safety_level', 'unknown')
                sources = data.get('sources', [])
                
                print(f"Status: {response.status_code}")
                print(f"Safety Level: {safety_level}")
                print(f"Sources: {sources}")
                print(f"Answer Length: {len(answer)} characters")
                print(f"Answer Preview: {answer[:300]}...")
                
                # Check for key indicators
                if 'honey' in answer.lower():
                    print("⚠️  Contains honey mention")
                if 'knowledge base question id' in answer.lower():
                    print("✅ Contains Knowledge Base Question ID")
                if 'not available' in answer.lower():
                    print("✅ Contains 'not available' message")
                    
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_food_responses()