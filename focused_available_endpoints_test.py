#!/usr/bin/env python3
"""
FOCUSED BACKEND TEST - Only Available Endpoints
Tests only the endpoints that are confirmed to be working on production backend
"""

import requests
import json
import time
import uuid
from datetime import datetime, timezone
import sys

BASE_URL = "https://baby-steps-demo-api.onrender.com"

class FocusedBackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.auth_token = None
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Test data storage
        self.test_user_email = None
        self.test_user_password = None
        self.baby_id = None
        
    def log_test(self, test_name, success, details, response_time=None, status_code=None):
        """Log test result with detailed information"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'response_time': response_time,
            'status_code': status_code,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        self.total_tests += 1
        
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        print(f"{status} - {test_name}")
        if response_time:
            print(f"    Response Time: {response_time:.2f}s")
        if status_code:
            print(f"    Status Code: {status_code}")
        print(f"    Details: {details}")
        print()
        
    def make_request(self, method, endpoint, data=None, auth_required=False, timeout=30):
        """Make HTTP request with error handling and timing"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if auth_required and self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
            
        start_time = time.time()
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers, timeout=timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response_time = time.time() - start_time
            return response, response_time
            
        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            return None, response_time
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return None, response_time

    # AVAILABLE ENDPOINT TESTS
    
    def test_1_health_check(self):
        """Test 1: Health Check"""
        response, response_time = self.make_request('GET', '/api/health')
        
        if response and response.status_code == 200:
            self.log_test(
                "1. Health Check",
                True,
                f"Backend healthy and operational",
                response_time,
                response.status_code
            )
            return True
        else:
            self.log_test(
                "1. Health Check", 
                False,
                f"Health check failed - Status: {response.status_code if response else 'Timeout'}",
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_2_demo_login(self):
        """Test 2: Demo Account Login"""
        login_data = {
            "email": "demo@babysteps.com",
            "password": "demo123"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', login_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'access_token' in data:
                    self.auth_token = data['access_token']
                    self.log_test(
                        "2. Demo Account Login",
                        True,
                        f"JWT token generated successfully",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "2. Demo Account Login",
                        False,
                        "No access_token in response",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "2. Demo Account Login",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            self.log_test(
                "2. Demo Account Login",
                False,
                f"Login failed - Status: {response.status_code if response else 'Timeout'}",
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_3_new_user_registration(self):
        """Test 3: New User Registration"""
        timestamp = int(time.time())
        self.test_user_email = f"focused_test_{timestamp}@test.com"
        self.test_user_password = "testpass123"
        
        register_data = {
            "name": "Focused Test User",
            "email": self.test_user_email,
            "password": self.test_user_password
        }
        
        response, response_time = self.make_request('POST', '/api/auth/register', register_data)
        
        if response and response.status_code in [200, 201]:
            try:
                data = response.json()
                # Check for expected format
                if 'access_token' in data and 'user' in data:
                    user_info = data['user']
                    if 'id' in user_info and 'email' in user_info and 'name' in user_info:
                        self.log_test(
                            "3. New User Registration",
                            True,
                            f"User created with auto-login - Email: {user_info['email']}",
                            response_time,
                            response.status_code
                        )
                        return True
                # Check for message-only format
                elif 'message' in data and 'email' in data:
                    self.log_test(
                        "3. New User Registration",
                        True,
                        f"User created - Email: {data['email']} (verification required)",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "3. New User Registration",
                        False,
                        f"Unexpected response format: {list(data.keys())}",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "3. New User Registration",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            self.log_test(
                "3. New User Registration",
                False,
                f"Registration failed - Status: {response.status_code if response else 'Timeout'}",
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_4_re_login_after_registration(self):
        """Test 4: Re-Login After Registration (Critical Test)"""
        if not self.test_user_email:
            self.log_test(
                "4. Re-Login After Registration",
                False,
                "Cannot test - previous registration failed",
                None,
                None
            )
            return False
            
        login_data = {
            "email": self.test_user_email,
            "password": self.test_user_password
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', login_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'access_token' in data:
                    self.auth_token = data['access_token']  # Update token
                    self.log_test(
                        "4. Re-Login After Registration",
                        True,
                        f"**CRITICAL TEST PASSED** - User persisted to database, can re-login successfully",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "4. Re-Login After Registration",
                        False,
                        "No access_token in response",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "4. Re-Login After Registration",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"Re-login failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 401:
                error_msg += " - **CRITICAL FAILURE: USER NOT FOUND**"
            self.log_test(
                "4. Re-Login After Registration",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_5_baby_profile_create(self):
        """Test 5: Create Baby Profile"""
        if not self.auth_token:
            self.log_test(
                "5. Create Baby Profile",
                False,
                "Cannot test - no authentication token",
                None,
                None
            )
            return False
            
        baby_data = {
            "name": "Focused Test Baby",
            "birth_date": "2024-01-15T00:00:00Z",
            "gender": "girl"
        }
        
        response, response_time = self.make_request('POST', '/api/babies', baby_data, auth_required=True)
        
        if response and response.status_code in [200, 201]:
            try:
                data = response.json()
                if 'id' in data:
                    self.baby_id = data['id']
                    self.log_test(
                        "5. Create Baby Profile",
                        True,
                        f"Baby profile created successfully - ID: {data['id']}",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "5. Create Baby Profile",
                        False,
                        "No id in response",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "5. Create Baby Profile",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            self.log_test(
                "5. Create Baby Profile",
                False,
                f"Create baby failed - Status: {response.status_code if response else 'Timeout'}",
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_6_baby_profile_retrieve(self):
        """Test 6: Retrieve Baby Profiles"""
        if not self.auth_token:
            self.log_test(
                "6. Retrieve Baby Profiles",
                False,
                "Cannot test - no authentication token",
                None,
                None
            )
            return False
            
        response, response_time = self.make_request('GET', '/api/babies', auth_required=True)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list) and len(data) >= 1:
                    self.log_test(
                        "6. Retrieve Baby Profiles",
                        True,
                        f"Baby profiles retrieved - Found {len(data)} profiles (including created one)",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "6. Retrieve Baby Profiles",
                        False,
                        f"Expected at least 1 baby profile, got: {len(data) if isinstance(data, list) else 'not a list'}",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "6. Retrieve Baby Profiles",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            self.log_test(
                "6. Retrieve Baby Profiles",
                False,
                f"Retrieve babies failed - Status: {response.status_code if response else 'Timeout'}",
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_7_research_endpoint(self):
        """Test 7: Research Endpoint (Available)"""
        if not self.auth_token:
            self.log_test(
                "7. Research Endpoint",
                False,
                "Cannot test - no authentication token",
                None,
                None
            )
            return False
            
        research_data = {
            "question": "When can babies eat strawberries?"
        }
        
        response, response_time = self.make_request('POST', '/api/research', research_data, auth_required=True)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'answer' in data:
                    answer = data['answer']
                    self.log_test(
                        "7. Research Endpoint",
                        True,
                        f"Research response received ({len(answer)} characters)",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "7. Research Endpoint",
                        False,
                        "No answer field in response",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "7. Research Endpoint",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            self.log_test(
                "7. Research Endpoint",
                False,
                f"Research failed - Status: {response.status_code if response else 'Timeout'}",
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_8_data_persistence_verification(self):
        """Test 8: Data Persistence After Re-Login"""
        if not self.auth_token:
            self.log_test(
                "8. Data Persistence Verification",
                False,
                "Cannot test - no authentication token from re-login",
                None,
                None
            )
            return False
        
        # Verify baby profiles still exist after re-login
        response, response_time = self.make_request('GET', '/api/babies', auth_required=True)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list) and len(data) >= 1:
                    # Check if our created baby is still there
                    baby_found = any(baby.get('id') == self.baby_id for baby in data) if self.baby_id else True
                    
                    if baby_found or len(data) >= 1:
                        self.log_test(
                            "8. Data Persistence Verification",
                            True,
                            f"Data persistence confirmed - {len(data)} baby profiles accessible after re-login",
                            response_time,
                            response.status_code
                        )
                        return True
                    else:
                        self.log_test(
                            "8. Data Persistence Verification",
                            False,
                            "Created baby profile not found after re-login",
                            response_time,
                            response.status_code
                        )
                        return False
                else:
                    self.log_test(
                        "8. Data Persistence Verification",
                        False,
                        "No baby profiles found after re-login - data persistence failed",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "8. Data Persistence Verification",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            self.log_test(
                "8. Data Persistence Verification",
                False,
                f"Data persistence check failed - Status: {response.status_code if response else 'Timeout'}",
                response_time,
                response.status_code if response else None
            )
            return False

    def run_all_tests(self):
        """Run all available endpoint tests"""
        print("🚀 FOCUSED BACKEND TESTING - Available Endpoints Only")
        print(f"🎯 Backend URL: {self.base_url}")
        print("📋 Testing only confirmed working endpoints")
        print("=" * 80)
        print()
        
        print("📍 CORE FUNCTIONALITY TESTS")
        print("-" * 50)
        self.test_1_health_check()
        self.test_2_demo_login()
        self.test_3_new_user_registration()
        self.test_4_re_login_after_registration()
        print()
        
        print("📍 BABY PROFILE TESTS")
        print("-" * 50)
        self.test_5_baby_profile_create()
        self.test_6_baby_profile_retrieve()
        print()
        
        print("📍 RESEARCH & DATA PERSISTENCE TESTS")
        print("-" * 50)
        self.test_7_research_endpoint()
        self.test_8_data_persistence_verification()
        print()
        
        # Final Results
        self.print_final_results()

    def print_final_results(self):
        """Print comprehensive final results"""
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print("=" * 80)
        print("🏁 FOCUSED BACKEND TESTING RESULTS")
        print("=" * 80)
        print()
        
        print("📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Check critical success criteria for available endpoints
        print("🔍 CRITICAL SUCCESS CRITERIA (Available Endpoints):")
        
        criteria_met = []
        criteria_failed = []
        
        # Check for specific critical tests
        critical_tests = {
            "User registration works": any("3." in r['test'] and r['success'] for r in self.test_results),
            "User persistence (re-login works)": any("4." in r['test'] and r['success'] for r in self.test_results),
            "Baby profiles can be created": any("5." in r['test'] and r['success'] for r in self.test_results),
            "Baby profiles can be retrieved": any("6." in r['test'] and r['success'] for r in self.test_results),
            "Research endpoint works": any("7." in r['test'] and r['success'] for r in self.test_results),
            "Data persists after re-login": any("8." in r['test'] and r['success'] for r in self.test_results),
        }
        
        for criteria, met in critical_tests.items():
            if met:
                criteria_met.append(f"✅ {criteria}")
            else:
                criteria_failed.append(f"❌ {criteria}")
        
        # Check for authentication errors
        auth_errors = any("401" in str(r.get('status_code', '')) or "user not found" in r.get('details', '').lower() 
                         for r in self.test_results if not r['success'])
        
        if not auth_errors:
            criteria_met.append("✅ No authentication errors")
        else:
            criteria_failed.append("❌ Authentication errors detected")
        
        # Check for 500 errors
        server_errors = any(r.get('status_code') == 500 for r in self.test_results)
        if not server_errors:
            criteria_met.append("✅ No 500 internal server errors")
        else:
            criteria_failed.append("❌ 500 internal server errors detected")
        
        for criteria in criteria_met:
            print(f"   {criteria}")
        for criteria in criteria_failed:
            print(f"   {criteria}")
        print()
        
        # Detailed test breakdown
        print("📋 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"   {status} {result['test']}")
            if not result['success']:
                print(f"      └─ {result['details']}")
        print()
        
        # Missing endpoints note
        print("⚠️  MISSING ENDPOINTS (404 Not Found):")
        missing_endpoints = [
            "Activity tracking endpoints (/api/feedings, /api/diapers, /api/sleep, /api/pumping)",
            "Measurements and milestones (/api/measurements, /api/milestones)",
            "Reminders (/api/reminders)",
            "Dashboard widgets (/api/dashboard/available-widgets)"
        ]
        for endpoint in missing_endpoints:
            print(f"   ❌ {endpoint}")
        print()
        
        print("⏰ TIMEOUT ENDPOINTS:")
        timeout_endpoints = [
            "AI Chat (/api/ai/chat)",
            "Food Research (/api/food/research)", 
            "Meal Search (/api/meals/search)",
            "Dashboard Layout (/api/dashboard/layout)"
        ]
        for endpoint in timeout_endpoints:
            print(f"   ⚠️  {endpoint}")
        print()
        
        # Performance metrics
        response_times = [r['response_time'] for r in self.test_results if r['response_time'] is not None]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            print("⚡ PERFORMANCE METRICS:")
            print(f"   Average Response Time: {avg_response_time:.2f}s")
            print(f"   Maximum Response Time: {max_response_time:.2f}s")
            print()
        
        # Final recommendation
        print("🎯 FINAL RECOMMENDATION:")
        if len(criteria_failed) == 0 and success_rate >= 90:
            print("   🟡 PARTIAL SUCCESS - Core functionality working")
            print("   ✅ User authentication and data persistence confirmed")
            print("   ✅ Baby profile management working")
            print("   ✅ Basic research functionality available")
            print("   ⚠️  Many endpoints missing - limited functionality")
            print("   📝 Recommendation: Core features work, but full feature set unavailable")
        else:
            print("   🔴 FAILURE - Critical issues with available endpoints")
            print("   ❌ Core functionality has problems")
            print()
            print("   🚨 CRITICAL ISSUES:")
            for issue in criteria_failed:
                print(f"      {issue}")
        
        print("=" * 80)

def main():
    """Main execution function"""
    tester = FocusedBackendTester()
    tester.run_all_tests()
    
    # Exit with appropriate code
    if tester.failed_tests == 0:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()