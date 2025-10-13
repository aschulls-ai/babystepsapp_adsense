#!/usr/bin/env python3
"""
Verification script to test Render backend after database migration
Tests all critical endpoints to confirm migration success
"""
import requests
import json
import sys

# Production backend URL
BASE_URL = "https://baby-steps-demo-api.onrender.com"

# Demo credentials
DEMO_EMAIL = "demo@babysteps.com"
DEMO_PASSWORD = "demo123"

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            print("   ✅ Health check passed")
            return True
        else:
            print(f"   ❌ Health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False

def test_login():
    """Test login and get JWT token"""
    print("\n2. Testing Authentication...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": DEMO_EMAIL, "password": DEMO_PASSWORD},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print("   ✅ Login successful, JWT token obtained")
                return token
            else:
                print("   ❌ Login response missing access_token")
                return None
        else:
            print(f"   ❌ Login failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return None

def test_create_activity(token):
    """Test creating an activity with feeding_type field"""
    print("\n3. Testing Activity Creation (Feeding with feeding_type)...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    activity_data = {
        "type": "feeding",
        "baby_id": "demo-baby-456",
        "notes": "Migration test - feeding with type",
        "feeding_type": "breast",
        "amount": 5.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/activities",
            json=activity_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("   ✅ Activity created successfully (HTTP 200/201)")
            print("   ✅ No UndefinedColumn error - migration successful!")
            return True
        elif response.status_code == 500:
            print("   ❌ Activity creation failed with HTTP 500")
            print(f"   Response: {response.text}")
            print("   ⚠️  This suggests the migration hasn't been applied yet")
            return False
        else:
            print(f"   ❌ Activity creation failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Activity creation error: {e}")
        return False

def test_create_activity_with_measurements(token):
    """Test creating an activity with measurement fields"""
    print("\n4. Testing Activity Creation (Measurements with weight/height)...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    activity_data = {
        "type": "measurement",
        "baby_id": "demo-baby-456",
        "notes": "Migration test - measurements",
        "weight": 15.5,
        "height": 28.0,
        "head_circumference": 17.5
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/activities",
            json=activity_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("   ✅ Measurement activity created successfully")
            return True
        else:
            print(f"   ❌ Measurement creation failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Measurement creation error: {e}")
        return False

def test_retrieve_activities(token):
    """Test retrieving activities"""
    print("\n5. Testing Activity Retrieval...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/activities?baby_id=demo-baby-456",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            activities = response.json()
            print(f"   ✅ Retrieved {len(activities)} activities successfully")
            return True
        else:
            print(f"   ❌ Activity retrieval failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Activity retrieval error: {e}")
        return False

def test_baby_profile_image(token):
    """Test baby profile with profile_image field"""
    print("\n6. Testing Baby Profile Creation (with profile_image)...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    baby_data = {
        "name": "Test Baby Migration",
        "birth_date": "2024-09-01",
        "gender": "girl",
        "profile_image": "https://example.com/baby.jpg"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/babies",
            json=baby_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("   ✅ Baby profile created with profile_image field")
            return True
        elif response.status_code == 500:
            print("   ❌ Baby profile creation failed with HTTP 500")
            print("   ⚠️  profile_image column may be missing")
            return False
        else:
            print(f"   ❌ Baby profile creation failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Baby profile creation error: {e}")
        return False

def main():
    """Run all verification tests"""
    print_header("RENDER BACKEND MIGRATION VERIFICATION")
    print(f"\n🔗 Testing backend: {BASE_URL}")
    print(f"👤 Using demo account: {DEMO_EMAIL}")
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health()))
    
    # Test 2: Login
    token = test_login()
    results.append(("Authentication", token is not None))
    
    if not token:
        print("\n❌ Cannot proceed without authentication token")
        print("   Please check if the backend service is running properly")
        sys.exit(1)
    
    # Test 3: Create activity with feeding_type (critical migration test)
    results.append(("Activity with feeding_type", test_create_activity(token)))
    
    # Test 4: Create activity with measurements
    results.append(("Activity with measurements", test_create_activity_with_measurements(token)))
    
    # Test 5: Retrieve activities
    results.append(("Activity Retrieval", test_retrieve_activities(token)))
    
    # Test 6: Baby profile with profile_image
    results.append(("Baby profile_image", test_baby_profile_image(token)))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed\n")
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("\n🎉 MIGRATION VERIFICATION SUCCESSFUL!")
        print("✅ All required database columns are present")
        print("✅ Activity endpoints working correctly")
        print("✅ No UndefinedColumn errors detected")
        print("✅ Backend is ready for production use")
        print("\n📝 Next steps:")
        print("   1. Run comprehensive backend testing")
        print("   2. Test the mobile app end-to-end")
        print("   3. Monitor Render logs for any issues")
        return 0
    else:
        print("\n⚠️  MIGRATION VERIFICATION FAILED")
        print(f"❌ {total - passed} test(s) failed")
        print("\n📝 Troubleshooting:")
        print("   1. Check if migration script was executed successfully")
        print("   2. Verify Render logs for error messages")
        print("   3. Confirm DATABASE_URL is properly configured")
        print("   4. Try restarting the Render service")
        print("   5. Re-run the migration script if needed (safe to run multiple times)")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
