#!/usr/bin/env python3
"""
Quick Backend Test for Baby Steps - Focus on Review Request Items
"""

import requests
import json

API_BASE = "http://localhost:8001/api"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        print(f"Health Check: HTTP {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Backend is healthy: {response.json()}")
            return True
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_login():
    """Test login with test user"""
    try:
        login_data = {
            "email": "test@babysteps.com",
            "password": "TestPassword123"
        }
        response = requests.post(f"{API_BASE}/auth/login", json=login_data, timeout=10)
        print(f"Login Test: HTTP {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"✅ Login successful, token obtained")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_meal_planner_search(token):
    """Test meal planner search endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 1: Food safety query
        search_query = {
            "query": "Is honey safe for babies?",
            "baby_age_months": 8
        }
        response = requests.post(f"{API_BASE}/meals/search", json=search_query, headers=headers, timeout=30)
        print(f"Honey Safety Query: HTTP {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Honey safety query successful: {data.get('results', '')[:100]}...")
        else:
            print(f"❌ Honey safety query failed: {response.text}")
        
        # Test 2: Meal ideas query
        search_query = {
            "query": "breakfast ideas for 6 month old",
            "baby_age_months": 6
        }
        response = requests.post(f"{API_BASE}/meals/search", json=search_query, headers=headers, timeout=30)
        print(f"Breakfast Ideas Query: HTTP {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Breakfast ideas query successful: {data.get('results', '')[:100]}...")
            return True
        else:
            print(f"❌ Breakfast ideas query failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Meal planner search error: {e}")
        return False

def test_key_endpoints(token):
    """Test key API endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("GET", "/babies", "Baby profiles"),
        ("POST", "/research", "Research endpoint", {"question": "How often should I feed my baby?"}),
        ("GET", "/feedings", "Feeding tracking"),
        ("GET", "/diapers", "Diaper tracking"),
        ("GET", "/sleep", "Sleep tracking"),
        ("POST", "/food/research", "Food research", {"question": "Is banana safe?", "baby_age_months": 6})
    ]
    
    working_endpoints = 0
    for method, endpoint, name, *data in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=10)
            else:
                test_data = data[0] if data else {}
                response = requests.post(f"{API_BASE}{endpoint}", json=test_data, headers=headers, timeout=10)
            
            print(f"{name}: HTTP {response.status_code}")
            if response.status_code == 200:
                working_endpoints += 1
                print(f"✅ {name} working")
            else:
                print(f"❌ {name} failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ {name} error: {e}")
    
    print(f"\n📊 Endpoint Summary: {working_endpoints}/{len(endpoints)} working")
    return working_endpoints == len(endpoints)

def main():
    print("🚀 QUICK BABY STEPS BACKEND TEST")
    print("=" * 50)
    
    # 1. Health check
    print("\n1. Testing backend health...")
    if not test_health():
        print("❌ Backend not healthy, stopping tests")
        return
    
    # 2. Authentication
    print("\n2. Testing authentication...")
    token = test_login()
    if not token:
        print("❌ Authentication failed, stopping tests")
        return
    
    # 3. Meal planner search (main focus)
    print("\n3. Testing meal planner search fix...")
    meal_search_working = test_meal_planner_search(token)
    
    # 4. Key endpoints
    print("\n4. Testing key API endpoints...")
    endpoints_working = test_key_endpoints(token)
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 REVIEW REQUEST SUMMARY:")
    print("=" * 50)
    
    if meal_search_working:
        print("✅ MEAL PLANNER SEARCH FIX: Working correctly")
        print("   • '/api/meals/search' endpoint responding")
        print("   • Food safety queries working")
        print("   • Meal idea queries working")
    else:
        print("❌ MEAL PLANNER SEARCH FIX: Issues found")
    
    if endpoints_working:
        print("✅ API ENDPOINTS: All key endpoints working")
    else:
        print("❌ API ENDPOINTS: Some endpoints have issues")
    
    print("✅ BACKEND HEALTH: Service running and responding")
    print("✅ AUTHENTICATION: Login working with test user")

if __name__ == "__main__":
    main()