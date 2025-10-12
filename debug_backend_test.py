#!/usr/bin/env python3
"""
Debug Backend Test - Check specific endpoint issues
"""

import requests
import json
import time
from datetime import datetime, timezone

BASE_URL = "https://baby-steps-demo-api.onrender.com"

def test_login():
    """Test login with demo account"""
    login_data = {
        "email": "demo@babysteps.com",
        "password": "demo123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=30)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token')
    return None

def test_endpoint(endpoint, method='GET', data=None, token=None):
    """Test a specific endpoint"""
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers, timeout=30)
        elif method == 'PUT':
            response = requests.put(f"{BASE_URL}{endpoint}", json=data, headers=headers, timeout=30)
        
        print(f"{method} {endpoint}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text[:200]}")
        else:
            try:
                result = response.json()
                if isinstance(result, list):
                    print(f"  Result: List with {len(result)} items")
                elif isinstance(result, dict):
                    print(f"  Result: Dict with keys: {list(result.keys())}")
                else:
                    print(f"  Result: {type(result)}")
            except:
                print(f"  Result: {response.text[:100]}")
        return response
    except requests.exceptions.Timeout:
        print(f"{method} {endpoint}: TIMEOUT")
        return None
    except Exception as e:
        print(f"{method} {endpoint}: ERROR - {str(e)}")
        return None

def main():
    print("🔍 DEBUG BACKEND TEST")
    print("=" * 50)
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Login failed - cannot continue")
        return
    
    print(f"✅ Login successful, token: {token[:20]}...")
    print()
    
    # Test baby endpoints
    print("📍 BABY ENDPOINTS")
    test_endpoint("/api/babies", "GET", token=token)
    
    baby_data = {
        "name": "Debug Test Baby",
        "birth_date": "2024-01-15T00:00:00Z",
        "gender": "boy"
    }
    baby_response = test_endpoint("/api/babies", "POST", baby_data, token=token)
    
    baby_id = None
    if baby_response and baby_response.status_code == 200:
        try:
            baby_result = baby_response.json()
            baby_id = baby_result.get('id')
            print(f"  Created baby ID: {baby_id}")
        except:
            pass
    
    print()
    
    # Test activity endpoints
    print("📍 ACTIVITY ENDPOINTS")
    
    if baby_id:
        # Test feeding
        feeding_data = {
            "baby_id": baby_id,
            "type": "bottle",
            "amount": 8.0,
            "notes": "Debug test feeding"
        }
        test_endpoint("/api/feedings", "POST", feeding_data, token=token)
        test_endpoint("/api/feedings", "GET", token=token)
        
        # Test diaper
        diaper_data = {
            "baby_id": baby_id,
            "type": "wet",
            "notes": "Debug test diaper"
        }
        test_endpoint("/api/diapers", "POST", diaper_data, token=token)
        test_endpoint("/api/diapers", "GET", token=token)
        
        # Test sleep
        current_time = datetime.now(timezone.utc)
        sleep_data = {
            "baby_id": baby_id,
            "start_time": current_time.isoformat(),
            "notes": "Debug test sleep"
        }
        test_endpoint("/api/sleep", "POST", sleep_data, token=token)
        test_endpoint("/api/sleep", "GET", token=token)
        
        # Test pumping
        pumping_data = {
            "baby_id": baby_id,
            "amount": 4.0,
            "duration": 20,
            "notes": "Debug test pumping"
        }
        test_endpoint("/api/pumping", "POST", pumping_data, token=token)
        test_endpoint("/api/pumping", "GET", token=token)
    else:
        print("❌ No baby ID - cannot test activity endpoints")

if __name__ == "__main__":
    main()