#!/usr/bin/env python3
"""
Detailed CORS and AI Response Testing
Focus on the specific requirements from the review request
"""

import requests
import json
import time

BACKEND_URL = "https://baby-steps-demo-api.onrender.com"
API_BASE = f"{BACKEND_URL}/api"

def test_specific_ai_queries():
    """Test the exact AI queries mentioned in the review request"""
    print("🤖 TESTING SPECIFIC AI QUERIES FROM REVIEW REQUEST")
    print("=" * 60)
    
    # First login to get auth token
    login_data = {
        "email": "demo@babysteps.com",
        "password": "demo123"
    }
    
    session = requests.Session()
    response = session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return
    
    auth_data = response.json()
    auth_token = auth_data.get('access_token')
    session.headers.update({'Authorization': f"Bearer {auth_token}"})
    
    print(f"✅ Authenticated successfully")
    
    # Test 1: AI Chat - "When can babies eat strawberries?"
    print("\n1. Testing AI Chat Query:")
    chat_query = {
        "message": "When can babies eat strawberries?",
        "baby_age_months": 6
    }
    
    start_time = time.time()
    response = session.post(f"{API_BASE}/ai/chat", json=chat_query, timeout=120)
    response_time = time.time() - start_time
    
    print(f"   Query: {chat_query['message']}")
    print(f"   Status: {response.status_code}")
    print(f"   Response Time: {response_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        ai_response = data.get('response', '')
        print(f"   Response Length: {len(ai_response)} characters")
        print(f"   Response Preview: {ai_response[:200]}...")
        
        # Check if it's a real response
        if 'temporarily unavailable' in ai_response.lower() or len(ai_response) < 50:
            print("   ❌ Appears to be fallback response")
        else:
            print("   ✅ Real AI response detected")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
    
    # Test 2: Food Research - "Are strawberries safe for 6 month old?"
    print("\n2. Testing Food Research Query:")
    food_query = {
        "question": "Are strawberries safe for 6 month old?",
        "baby_age_months": 6
    }
    
    start_time = time.time()
    response = session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
    response_time = time.time() - start_time
    
    print(f"   Query: {food_query['question']}")
    print(f"   Status: {response.status_code}")
    print(f"   Response Time: {response_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get('answer', '')
        safety_level = data.get('safety_level', '')
        print(f"   Safety Level: {safety_level}")
        print(f"   Answer Length: {len(answer)} characters")
        print(f"   Answer Preview: {answer[:200]}...")
        
        if 'temporarily unavailable' in answer.lower():
            print("   ❌ Appears to be fallback response")
        else:
            print("   ✅ Real food safety assessment")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
    
    # Test 3: Meal Search - "breakfast ideas for 8 month old"
    print("\n3. Testing Meal Search Query:")
    meal_query = {
        "query": "breakfast ideas for 8 month old",
        "baby_age_months": 8
    }
    
    start_time = time.time()
    response = session.post(f"{API_BASE}/meals/search", json=meal_query, timeout=120)
    response_time = time.time() - start_time
    
    print(f"   Query: {meal_query['query']}")
    print(f"   Status: {response.status_code}")
    print(f"   Response Time: {response_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', '')
        
        if isinstance(results, list):
            print(f"   Results Type: List with {len(results)} items")
            if len(results) > 0:
                print(f"   First Result Preview: {str(results[0])[:200]}...")
        elif isinstance(results, str):
            print(f"   Results Type: String with {len(results)} characters")
            print(f"   Results Preview: {results[:200]}...")
        
        if 'temporarily unavailable' in str(results).lower():
            print("   ❌ Appears to be fallback response")
        else:
            print("   ✅ Real meal suggestions")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")

def test_cors_detailed():
    """Test CORS configuration in detail"""
    print("\n🌐 DETAILED CORS TESTING")
    print("=" * 60)
    
    # Test OPTIONS preflight for different endpoints
    endpoints = ['/health', '/auth/login', '/babies', '/ai/chat', '/food/research', '/meals/search']
    
    for endpoint in endpoints:
        print(f"\nTesting CORS for {endpoint}:")
        
        # OPTIONS request
        response = requests.options(
            f"{API_BASE}{endpoint}",
            headers={
                'Origin': 'https://baby-steps-demo.vercel.app',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type, Authorization'
            },
            timeout=10
        )
        
        print(f"   OPTIONS Status: {response.status_code}")
        
        # Check CORS headers
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
        }
        
        print(f"   Allow-Origin: {cors_headers['Access-Control-Allow-Origin']}")
        print(f"   Allow-Methods: {cors_headers['Access-Control-Allow-Methods']}")
        print(f"   Allow-Headers: {cors_headers['Access-Control-Allow-Headers']}")
        print(f"   Allow-Credentials: {cors_headers['Access-Control-Allow-Credentials']}")
        
        # Verify critical CORS requirements
        if cors_headers['Access-Control-Allow-Origin'] == '*':
            print("   ✅ CORS Allow-Origin: * (correct)")
        else:
            print(f"   ❌ CORS Allow-Origin: Expected '*', got '{cors_headers['Access-Control-Allow-Origin']}'")
        
        credentials = cors_headers['Access-Control-Allow-Credentials']
        if credentials is None or credentials.lower() == 'false':
            print("   ✅ CORS Credentials: Not set or False (correct)")
        else:
            print(f"   ❌ CORS Credentials: Should be unset or False, got '{credentials}'")

def check_emergent_llm_key():
    """Check if EMERGENT_LLM_KEY is properly loaded"""
    print("\n🔑 CHECKING EMERGENT_LLM_KEY LOADING")
    print("=" * 60)
    
    # Test health endpoint for any AI integration indicators
    response = requests.get(f"{API_BASE}/health", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Health Response: {json.dumps(data, indent=2)}")
        
        # Look for AI integration status
        if 'ai_integration' in str(data).lower() or 'emergent' in str(data).lower():
            print("✅ AI integration status found in health response")
        else:
            print("ℹ️  No explicit AI integration status in health response")
            print("   Will verify through actual AI endpoint responses")

if __name__ == "__main__":
    check_emergent_llm_key()
    test_cors_detailed()
    test_specific_ai_queries()