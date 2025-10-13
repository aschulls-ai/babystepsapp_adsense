#!/usr/bin/env python3
"""
Test PRODUCTION Render backend - https://baby-steps-demo-api.onrender.com
This tests the ACTUAL production deployment, not the local preview
"""
import requests
import json
import time

# PRODUCTION RENDER URL
BASE_URL = "https://baby-steps-demo-api.onrender.com"

print("=" * 80)
print("PRODUCTION RENDER BACKEND TEST")
print(f"Target: {BASE_URL}")
print("=" * 80)

# Step 1: Health check
print("\n1. Health Check...")
try:
    response = requests.get(f"{BASE_URL}/api/health", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Backend is healthy")
    else:
        print(f"   ❌ Backend health check failed")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 2: Login
print("\n2. Login (demo account)...")
try:
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": "demo@babysteps.com", "password": "demo123"},
        timeout=10
    )
    print(f"   Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        print(f"   ✅ Login successful")
    else:
        print(f"   ❌ Login failed: {login_response.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Step 3: Test all 6 activity types
activity_tests = [
    {
        "name": "Feeding",
        "data": {
            "type": "feeding",
            "baby_id": "demo-baby-456",
            "notes": "Bottle feeding test",
            "feeding_type": "bottle",
            "amount": 4.5
        }
    },
    {
        "name": "Diaper",
        "data": {
            "type": "diaper",
            "baby_id": "demo-baby-456",
            "notes": "Diaper change test",
            "diaper_type": "wet"
        }
    },
    {
        "name": "Sleep",
        "data": {
            "type": "sleep",
            "baby_id": "demo-baby-456",
            "notes": "Nap time test",
            "duration": 90
        }
    },
    {
        "name": "Pumping",
        "data": {
            "type": "pumping",
            "baby_id": "demo-baby-456",
            "notes": "Pumping session test",
            "amount": 3.0,
            "duration": 15
        }
    },
    {
        "name": "Measurements",
        "data": {
            "type": "measurements",
            "baby_id": "demo-baby-456",
            "notes": "Monthly checkup test",
            "weight": 15.5,
            "height": 24.0,
            "head_circumference": 16.5
        }
    },
    {
        "name": "Milestones",
        "data": {
            "type": "milestones",
            "baby_id": "demo-baby-456",
            "title": "First smile",
            "description": "Baby smiled for the first time!",
            "category": "social",
            "notes": "Milestone test"
        }
    }
]

print("\n3. Testing Activity Creation (POST /api/activities)...")
results = {"success": 0, "failed_500": 0, "failed_other": 0}

for test in activity_tests:
    print(f"\n   Testing {test['name']}...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/activities",
            json=test["data"],
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"      ✅ SUCCESS - ID: {result.get('id', 'N/A')[:20]}...")
            results["success"] += 1
        elif response.status_code == 500:
            print(f"      ❌ HTTP 500 - ActivityRequest validation issue")
            print(f"      Response: {response.text[:100]}")
            results["failed_500"] += 1
        else:
            print(f"      ⚠️ HTTP {response.status_code}")
            print(f"      Response: {response.text[:100]}")
            results["failed_other"] += 1
            
    except Exception as e:
        print(f"      ❌ Error: {e}")
        results["failed_other"] += 1

# Step 4: Test GET activities
print("\n4. Testing Activity Retrieval (GET /api/activities)...")
try:
    response = requests.get(
        f"{BASE_URL}/api/activities",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        activities = response.json()
        print(f"   ✅ Retrieved {len(activities)} activities")
    else:
        print(f"   ⚠️ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total Activity Types Tested: 6")
print(f"✅ Successful: {results['success']}/6")
print(f"❌ Failed (500 errors): {results['failed_500']}/6")
print(f"⚠️ Failed (other): {results['failed_other']}/6")

if results["failed_500"] > 0:
    print("\n⚠️ DIAGNOSIS:")
    print("   500 errors indicate ActivityRequest model validation issue")
    print("   The Pydantic model needs to accept optional activity-specific fields")
    print("   Fix has been applied to /app/public-server/app.py")
    print("   ⚠️ CODE NEEDS TO BE DEPLOYED TO RENDER")
    
if results["success"] == 6:
    print("\n🎉 ALL TESTS PASSED - Production backend fully functional!")
else:
    print(f"\n❌ PRODUCTION DEPLOYMENT ISSUE - {results['failed_500'] + results['failed_other']}/6 tests failed")

print("=" * 80)
