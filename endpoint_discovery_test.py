#!/usr/bin/env python3
"""
Endpoint Discovery Test - Find what endpoints actually work
"""

import requests
import json

BASE_URL = "https://baby-steps-demo-api.onrender.com"

def test_endpoint(endpoint, method='GET', data=None, token=None):
    """Test a specific endpoint"""
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers, timeout=10)
        
        return response.status_code, response.text[:200]
    except:
        return None, "TIMEOUT/ERROR"

def main():
    print("🔍 ENDPOINT DISCOVERY TEST")
    print("=" * 50)
    
    # Get token first
    login_data = {"email": "demo@babysteps.com", "password": "demo123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
    token = None
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"✅ Got token: {token[:20]}...")
    else:
        print("❌ Login failed")
        return
    
    # Test various endpoints
    endpoints_to_test = [
        # Core endpoints
        ("/", "GET", None),
        ("/api/health", "GET", None),
        
        # Auth endpoints
        ("/api/auth/login", "POST", {"email": "demo@babysteps.com", "password": "demo123"}),
        
        # Baby endpoints
        ("/api/babies", "GET", None),
        
        # Activity endpoints (individual)
        ("/api/feedings", "GET", None),
        ("/api/diapers", "GET", None),
        ("/api/sleep", "GET", None),
        ("/api/pumping", "GET", None),
        ("/api/measurements", "GET", None),
        ("/api/milestones", "GET", None),
        ("/api/reminders", "GET", None),
        
        # Unified activity endpoint (if exists)
        ("/api/activities", "GET", None),
        
        # AI endpoints
        ("/api/ai/chat", "POST", {"message": "test", "baby_age_months": 6}),
        ("/api/food/research", "POST", {"question": "test", "baby_age_months": 6}),
        ("/api/meals/search", "POST", {"query": "test", "baby_age_months": 6}),
        
        # Dashboard endpoints
        ("/api/dashboard/layout", "GET", None),
        ("/api/dashboard/available-widgets", "GET", None),
        
        # Research endpoints
        ("/api/research", "POST", {"question": "test"}),
    ]
    
    print("\n📍 TESTING ENDPOINTS")
    print("-" * 30)
    
    working_endpoints = []
    not_found_endpoints = []
    error_endpoints = []
    
    for endpoint, method, data in endpoints_to_test:
        use_token = endpoint.startswith('/api/') and endpoint not in ['/api/auth/login', '/api/health']
        status_code, response_text = test_endpoint(endpoint, method, data, token if use_token else None)
        
        if status_code == 200:
            working_endpoints.append(f"{method} {endpoint}")
            print(f"✅ {method} {endpoint}: {status_code}")
        elif status_code == 404:
            not_found_endpoints.append(f"{method} {endpoint}")
            print(f"❌ {method} {endpoint}: 404 NOT FOUND")
        elif status_code is None:
            error_endpoints.append(f"{method} {endpoint}")
            print(f"⚠️  {method} {endpoint}: TIMEOUT/ERROR")
        else:
            error_endpoints.append(f"{method} {endpoint}")
            print(f"⚠️  {method} {endpoint}: {status_code}")
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"✅ Working endpoints: {len(working_endpoints)}")
    for ep in working_endpoints:
        print(f"   {ep}")
    
    print(f"\n❌ Not found (404): {len(not_found_endpoints)}")
    for ep in not_found_endpoints:
        print(f"   {ep}")
    
    print(f"\n⚠️  Errors/Timeouts: {len(error_endpoints)}")
    for ep in error_endpoints:
        print(f"   {ep}")

if __name__ == "__main__":
    main()