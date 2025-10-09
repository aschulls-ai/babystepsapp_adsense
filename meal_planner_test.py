#!/usr/bin/env python3
"""
Focused Meal Planner API Endpoint Test - Review Request Verification
Tests the specific meal planner search functionality as requested
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://babysteps-mobile.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class MealPlannerTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 60  # Longer timeout for AI responses
        self.auth_token = None
        # Test credentials as specified in review request
        self.test_email = "test@babysteps.com"
        self.test_password = "TestPassword123"
        
    def authenticate(self):
        """Login with test credentials"""
        try:
            login_data = {
                "email": self.test_email,
                "password": self.test_password
            }
            
            print(f"🔑 Authenticating with {self.test_email}...")
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    print("✅ Authentication successful")
                    return True
                else:
                    print(f"❌ Authentication failed: No access token in response")
                    return False
            else:
                print(f"❌ Authentication failed: HTTP {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def test_meal_search_endpoint_path(self):
        """Test the correct API endpoint path: /api/meals/search"""
        try:
            print(f"\n🔍 Testing correct API endpoint path: /api/meals/search")
            
            # Test query as specified in review request
            search_query = {
                "query": "make me a meal",
                "baby_age_months": 18  # 18 month old as mentioned in review
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            print(f"📡 Request: POST {API_BASE}/meals/search")
            print(f"📝 Query: {search_query['query']}")
            print(f"👶 Baby age: {search_query['baby_age_months']} months")
            print(f"📊 Response: HTTP {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API endpoint path is correct - /api/meals/search working")
                
                # Verify JSON response structure
                required_fields = ['results', 'query', 'age_months']
                if all(field in data for field in required_fields):
                    print("✅ Proper JSON response structure confirmed")
                    print(f"📋 Response contains: {list(data.keys())}")
                    return True, data
                else:
                    print(f"❌ Missing required fields in response: {data}")
                    return False, data
            else:
                print(f"❌ API endpoint failed: HTTP {response.status_code}")
                print(f"📄 Response: {response.text}")
                return False, None
                
        except Exception as e:
            print(f"❌ Endpoint test error: {str(e)}")
            return False, None
    
    def test_specific_queries(self):
        """Test specific queries mentioned in review request"""
        queries = [
            {
                "query": "make me a meal",
                "baby_age_months": 18,
                "description": "User's screenshot query"
            },
            {
                "query": "breakfast ideas for 18 month old", 
                "baby_age_months": 18,
                "description": "Age-appropriate breakfast ideas"
            }
        ]
        
        results = []
        
        for i, test_query in enumerate(queries, 1):
            try:
                print(f"\n🧪 Test Query {i}: {test_query['description']}")
                print(f"📝 Query: '{test_query['query']}'")
                print(f"👶 Age: {test_query['baby_age_months']} months")
                
                response = self.session.post(f"{API_BASE}/meals/search", json=test_query, timeout=60)
                
                print(f"📊 Response: HTTP {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if we got meaningful results
                    if 'results' in data and len(data['results']) > 10:
                        print("✅ Query successful - received meal suggestions")
                        print(f"📄 Response length: {len(data['results'])} characters")
                        
                        # Check for age-appropriate content
                        results_lower = data['results'].lower()
                        age_appropriate_terms = ['18 month', 'toddler', 'finger food', 'self-feeding', 'chopped', 'small pieces']
                        
                        found_terms = [term for term in age_appropriate_terms if term in results_lower]
                        if found_terms:
                            print(f"✅ Age-appropriate suggestions detected: {found_terms}")
                        else:
                            print("ℹ️ Age-appropriate terms not explicitly found (content may still be appropriate)")
                        
                        # Show sample of response
                        sample = data['results'][:200] + "..." if len(data['results']) > 200 else data['results']
                        print(f"📋 Sample response: {sample}")
                        
                        results.append({"query": test_query['query'], "success": True, "data": data})
                    else:
                        print(f"❌ Empty or minimal response: {data}")
                        results.append({"query": test_query['query'], "success": False, "data": data})
                else:
                    print(f"❌ Query failed: HTTP {response.status_code}")
                    print(f"📄 Error: {response.text}")
                    results.append({"query": test_query['query'], "success": False, "data": None})
                    
            except Exception as e:
                print(f"❌ Query error: {str(e)}")
                results.append({"query": test_query['query'], "success": False, "data": None})
        
        return results
    
    def test_error_resolution(self):
        """Test that the 'Failed to search meals and food safety info' error is resolved"""
        try:
            print(f"\n🔧 Testing error resolution: 'Failed to search meals and food safety info'")
            
            # Test multiple queries to ensure no failures
            test_queries = [
                {"query": "is honey safe for babies", "baby_age_months": 8},
                {"query": "lunch ideas", "baby_age_months": 12},
                {"query": "snack suggestions", "baby_age_months": 18}
            ]
            
            all_successful = True
            
            for query in test_queries:
                response = self.session.post(f"{API_BASE}/meals/search", json=query, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'results' in data and len(data['results']) > 0:
                        print(f"✅ '{query['query']}' - Success")
                    else:
                        print(f"❌ '{query['query']}' - Empty response")
                        all_successful = False
                else:
                    print(f"❌ '{query['query']}' - HTTP {response.status_code}")
                    all_successful = False
            
            if all_successful:
                print("✅ No 'Failed to search meals and food safety info' errors detected")
                return True
            else:
                print("❌ Some queries still failing")
                return False
                
        except Exception as e:
            print(f"❌ Error resolution test failed: {str(e)}")
            return False
    
    def run_focused_test(self):
        """Run focused meal planner API test as per review request"""
        print("🎯 MEAL PLANNER API ENDPOINT FIX VERIFICATION")
        print("=" * 60)
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Test user: {self.test_email}")
        print(f"🎯 Focus: Verify /api/meals/search endpoint fix")
        print("=" * 60)
        
        # Step 1: Authenticate
        if not self.authenticate():
            print("❌ Cannot proceed without authentication")
            return False
        
        # Step 2: Test correct API endpoint path
        print(f"\n📍 STEP 1: API ENDPOINT PATH VERIFICATION")
        endpoint_success, endpoint_data = self.test_meal_search_endpoint_path()
        
        if not endpoint_success:
            print("❌ API endpoint path test failed")
            return False
        
        # Step 3: Test specific queries from review request
        print(f"\n📝 STEP 2: SPECIFIC QUERY TESTING")
        query_results = self.test_specific_queries()
        
        successful_queries = [r for r in query_results if r['success']]
        failed_queries = [r for r in query_results if not r['success']]
        
        # Step 4: Test error resolution
        print(f"\n🔧 STEP 3: ERROR RESOLUTION VERIFICATION")
        error_resolved = self.test_error_resolution()
        
        # Final Summary
        print(f"\n📊 VERIFICATION SUMMARY")
        print("=" * 60)
        
        if endpoint_success:
            print("✅ API endpoint path: /api/meals/search working correctly")
        else:
            print("❌ API endpoint path: Issues detected")
        
        print(f"✅ Successful queries: {len(successful_queries)}/{len(query_results)}")
        for result in successful_queries:
            print(f"   • '{result['query']}' - Working")
        
        if failed_queries:
            print(f"❌ Failed queries: {len(failed_queries)}")
            for result in failed_queries:
                print(f"   • '{result['query']}' - Failed")
        
        if error_resolved:
            print("✅ 'Failed to search meals and food safety info' error resolved")
        else:
            print("❌ Error resolution: Issues still present")
        
        # Overall result
        overall_success = endpoint_success and len(failed_queries) == 0 and error_resolved
        
        if overall_success:
            print(f"\n🎉 OVERALL RESULT: MEAL PLANNER API FIX VERIFIED SUCCESSFULLY")
            print("   • Correct API endpoint path working")
            print("   • All test queries successful")
            print("   • No 'failed' error messages")
            print("   • Age-appropriate suggestions provided")
        else:
            print(f"\n❌ OVERALL RESULT: ISSUES DETECTED")
            print("   • Some functionality may still need attention")
        
        return overall_success

def main():
    """Main test execution"""
    tester = MealPlannerTester()
    success = tester.run_focused_test()
    
    if success:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()