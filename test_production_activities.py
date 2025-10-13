#!/usr/bin/env python3
"""
Test activity creation on production Render backend to identify 500 errors
"""
import requests
import json

BASE_URL = "https://baby-steps-demo-api.onrender.com"

def test_activities():
    print("=" * 80)
    print("PRODUCTION ACTIVITY ENDPOINTS VALIDATION TEST")
    print("=" * 80)
    
    # Login
    print("\n1. Login...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": "demo@babysteps.com", "password": "demo123"}
    )
    print(f"   Status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print(f"   ERROR: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test each activity type
    test_cases = [
        {
            "name": "Feeding Activity",
            "data": {
                "type": "feeding",
                "baby_id": "demo-baby-456",
                "notes": "Test feeding",
                "feeding_type": "bottle",
                "amount": 4.5
            }
        },
        {
            "name": "Diaper Activity",
            "data": {
                "type": "diaper",
                "baby_id": "demo-baby-456",
                "notes": "Diaper change",
                "diaper_type": "wet"
            }
        },
        {
            "name": "Sleep Activity",
            "data": {
                "type": "sleep",
                "baby_id": "demo-baby-456",
                "notes": "Nap time",
                "duration": 120
            }
        },
        {
            "name": "Pumping Activity",
            "data": {
                "type": "pumping",
                "baby_id": "demo-baby-456",
                "notes": "Pumping session",
                "amount": 3.0,
                "duration": 15
            }
        },
        {
            "name": "Measurements Activity",
            "data": {
                "type": "measurements",
                "baby_id": "demo-baby-456",
                "notes": "Monthly checkup",
                "weight": 15.5,
                "height": 24.0,
                "head_circumference": 16.5
            }
        },
        {
            "name": "Milestone Activity",
            "data": {
                "type": "milestones",
                "baby_id": "demo-baby-456",
                "title": "First smile",
                "description": "Baby smiled for the first time!",
                "category": "social",
                "notes": "Milestone achieved"
            }
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test['name']}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/activities",
                json=test["data"],
                headers=headers,
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200 or response.status_code == 201:
                result_data = response.json()
                print(f"   ✅ SUCCESS - Activity ID: {result_data.get('id', 'N/A')}")
                results.append({"test": test["name"], "status": "PASS", "code": response.status_code})
            elif response.status_code == 500:
                print(f"   ❌ 500 ERROR - Server error")
                print(f"   Response: {response.text[:200]}")
                results.append({"test": test["name"], "status": "FAIL (500)", "code": 500, "error": response.text[:200]})
            else:
                print(f"   ⚠️ UNEXPECTED STATUS")
                print(f"   Response: {response.text[:200]}")
                results.append({"test": test["name"], "status": "FAIL", "code": response.status_code, "error": response.text[:200]})
                
        except requests.exceptions.Timeout:
            print(f"   ❌ TIMEOUT")
            results.append({"test": test["name"], "status": "TIMEOUT", "code": None})
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append({"test": test["name"], "status": "ERROR", "code": None, "error": str(e)})
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_500_count = sum(1 for r in results if r["status"] == "FAIL (500)")
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {pass_count}/{len(results)}")
    print(f"500 Errors: {fail_500_count}/{len(results)}")
    
    if fail_500_count > 0:
        print("\n⚠️ ACTIVITIES WITH 500 ERRORS:")
        for r in results:
            if r["status"] == "FAIL (500)":
                print(f"   - {r['test']}")
                if "error" in r:
                    print(f"     Error: {r['error']}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_activities()
