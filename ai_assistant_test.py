#!/usr/bin/env python3
"""
Backend Testing Suite for AI Assistant Mobile Network Optimization
Testing the updated AI Assistant functionality with androidFetch integration
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Configuration
BACKEND_URL = "https://openai-parent.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
DEMO_EMAIL = "demo@babysteps.com"
DEMO_PASSWORD = "demo123"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}")

def print_test(test_name):
    print(f"\n{Colors.BLUE}🧪 Testing: {test_name}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.WHITE}ℹ️  {message}{Colors.END}")

class AIAssistantTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.auth_token = None
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        
        # Android-specific headers to simulate androidFetch behavior
        self.android_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        self.session.headers.update(self.android_headers)

    def record_test(self, test_name, passed, details=""):
        self.test_results['total_tests'] += 1
        if passed:
            self.test_results['passed_tests'] += 1
            print_success(f"{test_name} - PASSED")
        else:
            self.test_results['failed_tests'] += 1
            print_error(f"{test_name} - FAILED: {details}")
        
        self.test_results['test_details'].append({
            'test': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

    def test_authentication(self):
        """Test authentication with demo user credentials"""
        print_test("Authentication with Demo User")
        
        try:
            # Test login endpoint
            login_data = {
                "email": DEMO_EMAIL,
                "password": DEMO_PASSWORD
            }
            
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=login_data,
                headers=self.android_headers
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                
                if self.auth_token:
                    # Set authorization header for future requests
                    self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
                    self.record_test("Demo User Authentication", True, f"Token received: {self.auth_token[:20]}...")
                    print_info(f"Authentication successful - Token: {self.auth_token[:20]}...")
                    return True
                else:
                    self.record_test("Demo User Authentication", False, "No access token in response")
                    return False
            else:
                error_detail = response.text
                self.record_test("Demo User Authentication", False, f"HTTP {response.status_code}: {error_detail}")
                return False
                
        except Exception as e:
            self.record_test("Demo User Authentication", False, f"Exception: {str(e)}")
            return False

    def test_ai_chat_endpoint_basic(self):
        """Test basic AI chat endpoint functionality"""
        print_test("AI Chat Endpoint - Basic Functionality")
        
        if not self.auth_token:
            self.record_test("AI Chat Basic", False, "No authentication token available")
            return False
        
        try:
            # Test basic AI chat request
            chat_data = {
                "message": "What breakfast ideas for my baby?",
                "baby_age_months": 8
            }
            
            response = self.session.post(
                f"{API_BASE}/ai/chat",
                json=chat_data,
                headers={
                    **self.android_headers,
                    'Authorization': f'Bearer {self.auth_token}'
                }
            )
            
            print_info(f"Request URL: {API_BASE}/ai/chat")
            print_info(f"Request data: {json.dumps(chat_data, indent=2)}")
            print_info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', '')
                timestamp = data.get('timestamp', '')
                
                if ai_response and len(ai_response) > 50:
                    self.record_test("AI Chat Basic", True, f"Response length: {len(ai_response)} chars")
                    print_info(f"AI Response preview: {ai_response[:100]}...")
                    print_info(f"Response timestamp: {timestamp}")
                    return True
                else:
                    self.record_test("AI Chat Basic", False, f"Response too short or empty: {len(ai_response)} chars")
                    return False
            else:
                error_detail = response.text
                self.record_test("AI Chat Basic", False, f"HTTP {response.status_code}: {error_detail}")
                return False
                
        except Exception as e:
            self.record_test("AI Chat Basic", False, f"Exception: {str(e)}")
            return False

    def test_android_network_compatibility(self):
        """Test Android network compatibility with various scenarios"""
        print_test("Android Network Compatibility")
        
        if not self.auth_token:
            self.record_test("Android Network Compatibility", False, "No authentication token available")
            return False
        
        # Test different Android-specific scenarios
        test_scenarios = [
            {
                "name": "Standard Android Request",
                "headers": {
                    **self.android_headers,
                    'Authorization': f'Bearer {self.auth_token}'
                },
                "message": "When can babies start eating solid food?"
            },
            {
                "name": "Android with Cache Control",
                "headers": {
                    **self.android_headers,
                    'Authorization': f'Bearer {self.auth_token}',
                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                },
                "message": "Is it safe to give honey to a 10 month old baby?"
            },
            {
                "name": "Android with CORS Headers",
                "headers": {
                    **self.android_headers,
                    'Authorization': f'Bearer {self.auth_token}',
                    'Origin': 'https://openai-parent.preview.emergentagent.com'
                },
                "message": "What are good finger foods for a 9 month old?"
            }
        ]
        
        passed_scenarios = 0
        total_scenarios = len(test_scenarios)
        
        for scenario in test_scenarios:
            try:
                print_info(f"Testing scenario: {scenario['name']}")
                
                chat_data = {
                    "message": scenario["message"],
                    "baby_age_months": 9
                }
                
                response = self.session.post(
                    f"{API_BASE}/ai/chat",
                    json=chat_data,
                    headers=scenario["headers"]
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get('response', '')
                    
                    if ai_response and len(ai_response) > 50:
                        passed_scenarios += 1
                        print_success(f"{scenario['name']} - Response received ({len(ai_response)} chars)")
                    else:
                        print_error(f"{scenario['name']} - Empty or short response")
                else:
                    print_error(f"{scenario['name']} - HTTP {response.status_code}")
                    
            except Exception as e:
                print_error(f"{scenario['name']} - Exception: {str(e)}")
        
        success_rate = (passed_scenarios / total_scenarios) * 100
        if success_rate >= 80:
            self.record_test("Android Network Compatibility", True, f"{passed_scenarios}/{total_scenarios} scenarios passed ({success_rate:.1f}%)")
            return True
        else:
            self.record_test("Android Network Compatibility", False, f"Only {passed_scenarios}/{total_scenarios} scenarios passed ({success_rate:.1f}%)")
            return False

    def test_response_handling(self):
        """Test AI response handling and processing"""
        print_test("AI Response Processing and Handling")
        
        if not self.auth_token:
            self.record_test("Response Handling", False, "No authentication token available")
            return False
        
        test_queries = [
            {
                "message": "What breakfast ideas for my baby?",
                "baby_age_months": 8,
                "expected_keywords": ["breakfast", "baby", "food", "months"]
            },
            {
                "message": "When can babies start eating solid food?",
                "baby_age_months": 6,
                "expected_keywords": ["solid", "food", "months", "baby"]
            },
            {
                "message": "Is it safe to give honey to a 10 month old baby?",
                "baby_age_months": 10,
                "expected_keywords": ["honey", "safe", "baby", "months"]
            }
        ]
        
        passed_queries = 0
        total_queries = len(test_queries)
        
        for i, query in enumerate(test_queries, 1):
            try:
                print_info(f"Testing query {i}/{total_queries}: {query['message']}")
                
                response = self.session.post(
                    f"{API_BASE}/ai/chat",
                    json={
                        "message": query["message"],
                        "baby_age_months": query["baby_age_months"]
                    },
                    headers={
                        **self.android_headers,
                        'Authorization': f'Bearer {self.auth_token}'
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get('response', '')
                    timestamp = data.get('timestamp', '')
                    
                    # Check response quality
                    response_checks = {
                        'has_content': len(ai_response) > 100,
                        'has_timestamp': bool(timestamp),
                        'contains_keywords': any(keyword.lower() in ai_response.lower() for keyword in query['expected_keywords']),
                        'proper_format': isinstance(data, dict) and 'response' in data
                    }
                    
                    passed_checks = sum(response_checks.values())
                    total_checks = len(response_checks)
                    
                    if passed_checks >= 3:  # At least 3 out of 4 checks should pass
                        passed_queries += 1
                        print_success(f"Query {i} - {passed_checks}/{total_checks} checks passed")
                        print_info(f"Response length: {len(ai_response)} chars")
                    else:
                        print_error(f"Query {i} - Only {passed_checks}/{total_checks} checks passed")
                        print_info(f"Failed checks: {[k for k, v in response_checks.items() if not v]}")
                else:
                    print_error(f"Query {i} - HTTP {response.status_code}: {response.text}")
                    
                # Small delay between requests
                time.sleep(1)
                
            except Exception as e:
                print_error(f"Query {i} - Exception: {str(e)}")
        
        success_rate = (passed_queries / total_queries) * 100
        if success_rate >= 80:
            self.record_test("Response Handling", True, f"{passed_queries}/{total_queries} queries processed successfully ({success_rate:.1f}%)")
            return True
        else:
            self.record_test("Response Handling", False, f"Only {passed_queries}/{total_queries} queries processed successfully ({success_rate:.1f}%)")
            return False

    def test_error_handling(self):
        """Test error handling scenarios"""
        print_test("Error Handling Scenarios")
        
        error_scenarios = [
            {
                "name": "Missing Authentication",
                "headers": self.android_headers,  # No auth token
                "data": {"message": "Test message"},
                "expected_status": [401, 403]
            },
            {
                "name": "Empty Message",
                "headers": {**self.android_headers, 'Authorization': f'Bearer {self.auth_token}'},
                "data": {"message": ""},
                "expected_status": [400, 422]
            },
            {
                "name": "Missing Message Field",
                "headers": {**self.android_headers, 'Authorization': f'Bearer {self.auth_token}'},
                "data": {"baby_age_months": 8},
                "expected_status": [400, 422]
            },
            {
                "name": "Invalid JSON",
                "headers": {**self.android_headers, 'Authorization': f'Bearer {self.auth_token}'},
                "data": "invalid json",
                "expected_status": [400, 422]
            }
        ]
        
        passed_scenarios = 0
        total_scenarios = len(error_scenarios)
        
        for scenario in error_scenarios:
            try:
                print_info(f"Testing error scenario: {scenario['name']}")
                
                if isinstance(scenario['data'], str):
                    # Send invalid JSON
                    response = requests.post(
                        f"{API_BASE}/ai/chat",
                        data=scenario['data'],
                        headers=scenario['headers'],
                        timeout=30
                    )
                else:
                    response = requests.post(
                        f"{API_BASE}/ai/chat",
                        json=scenario['data'],
                        headers=scenario['headers'],
                        timeout=30
                    )
                
                if response.status_code in scenario['expected_status']:
                    passed_scenarios += 1
                    print_success(f"{scenario['name']} - Correctly returned {response.status_code}")
                else:
                    print_error(f"{scenario['name']} - Expected {scenario['expected_status']}, got {response.status_code}")
                    
            except Exception as e:
                print_error(f"{scenario['name']} - Exception: {str(e)}")
        
        success_rate = (passed_scenarios / total_scenarios) * 100
        if success_rate >= 75:
            self.record_test("Error Handling", True, f"{passed_scenarios}/{total_scenarios} error scenarios handled correctly ({success_rate:.1f}%)")
            return True
        else:
            self.record_test("Error Handling", False, f"Only {passed_scenarios}/{total_scenarios} error scenarios handled correctly ({success_rate:.1f}%)")
            return False

    def test_endpoint_path_fix(self):
        """Test that the endpoint path fix (/api/ai/chat) is working correctly"""
        print_test("API Endpoint Path Fix Verification")
        
        if not self.auth_token:
            self.record_test("Endpoint Path Fix", False, "No authentication token available")
            return False
        
        # Test the correct endpoint path
        correct_path_tests = [
            {
                "path": "/api/ai/chat",
                "should_work": True,
                "description": "Correct path with /api prefix"
            },
            {
                "path": "/ai/chat",
                "should_work": False,
                "description": "Old path without /api prefix (should fail)"
            }
        ]
        
        results = []
        
        for test in correct_path_tests:
            try:
                print_info(f"Testing path: {test['path']} - {test['description']}")
                
                response = self.session.post(
                    f"{BACKEND_URL}{test['path']}",
                    json={
                        "message": "Test endpoint path",
                        "baby_age_months": 8
                    },
                    headers={
                        **self.android_headers,
                        'Authorization': f'Bearer {self.auth_token}'
                    }
                )
                
                if test['should_work']:
                    if response.status_code == 200:
                        results.append(True)
                        print_success(f"Correct path works - {response.status_code}")
                    else:
                        results.append(False)
                        print_error(f"Correct path failed - {response.status_code}")
                else:
                    if response.status_code in [404, 405]:
                        results.append(True)
                        print_success(f"Old path correctly fails - {response.status_code}")
                    else:
                        results.append(False)
                        print_warning(f"Old path unexpectedly works - {response.status_code}")
                        
            except Exception as e:
                if test['should_work']:
                    results.append(False)
                    print_error(f"Exception on correct path: {str(e)}")
                else:
                    results.append(True)
                    print_success(f"Old path correctly fails with exception")
        
        if all(results):
            self.record_test("Endpoint Path Fix", True, "API endpoint path fix verified - /api/ai/chat works correctly")
            return True
        else:
            self.record_test("Endpoint Path Fix", False, "API endpoint path issues detected")
            return False

    def run_all_tests(self):
        """Run all AI Assistant tests"""
        print_header("AI ASSISTANT MOBILE NETWORK OPTIMIZATION TESTING")
        print_info(f"Backend URL: {BACKEND_URL}")
        print_info(f"Testing with demo user: {DEMO_EMAIL}")
        print_info(f"Simulating Android network behavior with androidFetch compatibility")
        
        # Run tests in sequence
        tests = [
            self.test_authentication,
            self.test_endpoint_path_fix,
            self.test_ai_chat_endpoint_basic,
            self.test_android_network_compatibility,
            self.test_response_handling,
            self.test_error_handling
        ]
        
        for test_func in tests:
            try:
                test_func()
                time.sleep(1)  # Small delay between tests
            except Exception as e:
                print_error(f"Test {test_func.__name__} failed with exception: {str(e)}")
                self.record_test(test_func.__name__, False, f"Exception: {str(e)}")
        
        # Print final results
        self.print_final_results()

    def print_final_results(self):
        """Print comprehensive test results"""
        print_header("AI ASSISTANT TESTING RESULTS")
        
        total = self.test_results['total_tests']
        passed = self.test_results['passed_tests']
        failed = self.test_results['failed_tests']
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}SUMMARY:{Colors.END}")
        print(f"  Total Tests: {total}")
        print(f"  {Colors.GREEN}Passed: {passed}{Colors.END}")
        print(f"  {Colors.RED}Failed: {failed}{Colors.END}")
        print(f"  Success Rate: {Colors.GREEN if success_rate >= 80 else Colors.RED}{success_rate:.1f}%{Colors.END}")
        
        print(f"\n{Colors.BOLD}DETAILED RESULTS:{Colors.END}")
        for result in self.test_results['test_details']:
            status = f"{Colors.GREEN}✅ PASS" if result['passed'] else f"{Colors.RED}❌ FAIL"
            print(f"  {status}{Colors.END} - {result['test']}")
            if result['details']:
                print(f"    Details: {result['details']}")
        
        # Overall assessment
        print(f"\n{Colors.BOLD}ASSESSMENT:{Colors.END}")
        if success_rate >= 90:
            print(f"{Colors.GREEN}🎉 EXCELLENT: AI Assistant mobile optimization is working perfectly!{Colors.END}")
        elif success_rate >= 80:
            print(f"{Colors.YELLOW}✅ GOOD: AI Assistant mobile optimization is working well with minor issues.{Colors.END}")
        elif success_rate >= 60:
            print(f"{Colors.YELLOW}⚠️  MODERATE: AI Assistant has some issues that need attention.{Colors.END}")
        else:
            print(f"{Colors.RED}❌ CRITICAL: AI Assistant has significant issues that need immediate attention.{Colors.END}")

def main():
    """Main test execution"""
    tester = AIAssistantTester()
    tester.run_all_tests()
    
    # Return exit code based on results
    success_rate = (tester.test_results['passed_tests'] / tester.test_results['total_tests'] * 100) if tester.test_results['total_tests'] > 0 else 0
    return 0 if success_rate >= 80 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)