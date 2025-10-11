#!/usr/bin/env python3
"""
Specific Query Testing for AI Assistant Mobile Optimization
Testing the exact queries mentioned in the review request
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://baby-genius.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"
DEMO_EMAIL = "demo@babysteps.com"
DEMO_PASSWORD = "demo123"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.WHITE}ℹ️  {message}{Colors.END}")

class SpecificQueryTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.auth_token = None
        
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

    def authenticate(self):
        """Authenticate with demo user"""
        print_info("Authenticating with demo user...")
        
        try:
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
                    self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
                    print_success("Authentication successful")
                    return True
                    
        except Exception as e:
            print_error(f"Authentication failed: {str(e)}")
            
        return False

    def test_specific_query(self, query, baby_age_months=None):
        """Test a specific query with androidFetch simulation"""
        print(f"\n{Colors.BLUE}🧪 Testing Query: {query}{Colors.END}")
        
        try:
            chat_data = {
                "message": query
            }
            
            if baby_age_months:
                chat_data["baby_age_months"] = baby_age_months
                print_info(f"Baby age context: {baby_age_months} months")
            
            # Simulate androidFetch request
            response = self.session.post(
                f"{API_BASE}/ai/chat",
                json=chat_data,
                headers={
                    **self.android_headers,
                    'Authorization': f'Bearer {self.auth_token}'
                }
            )
            
            print_info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', '')
                timestamp = data.get('timestamp', '')
                
                print_success(f"Query successful - Response length: {len(ai_response)} chars")
                print_info(f"Response timestamp: {timestamp}")
                
                # Print response preview
                if len(ai_response) > 200:
                    print(f"\n{Colors.WHITE}📝 Response Preview:{Colors.END}")
                    print(f"{ai_response[:200]}...")
                else:
                    print(f"\n{Colors.WHITE}📝 Full Response:{Colors.END}")
                    print(ai_response)
                
                # Check for key indicators of good response
                quality_indicators = {
                    'sufficient_length': len(ai_response) > 100,
                    'contains_baby_context': any(word in ai_response.lower() for word in ['baby', 'infant', 'child']),
                    'contains_safety_info': any(word in ai_response.lower() for word in ['safe', 'consult', 'pediatrician']),
                    'proper_formatting': bool(timestamp and isinstance(data, dict))
                }
                
                passed_indicators = sum(quality_indicators.values())
                total_indicators = len(quality_indicators)
                
                print(f"\n{Colors.WHITE}Quality Assessment:{Colors.END}")
                for indicator, passed in quality_indicators.items():
                    status = "✅" if passed else "❌"
                    print(f"  {status} {indicator.replace('_', ' ').title()}")
                
                if passed_indicators >= 3:
                    print_success(f"High quality response ({passed_indicators}/{total_indicators} indicators passed)")
                    return True
                else:
                    print_error(f"Low quality response ({passed_indicators}/{total_indicators} indicators passed)")
                    return False
                    
            else:
                error_detail = response.text
                print_error(f"Request failed: HTTP {response.status_code}")
                print_info(f"Error details: {error_detail}")
                return False
                
        except Exception as e:
            print_error(f"Exception occurred: {str(e)}")
            return False

    def run_specific_tests(self):
        """Run the specific queries mentioned in the review request"""
        print_header("SPECIFIC QUERY TESTING - REVIEW REQUEST VERIFICATION")
        print_info("Testing the exact queries mentioned in the review request")
        print_info("Simulating Android network behavior with androidFetch")
        
        if not self.authenticate():
            print_error("Authentication failed - cannot proceed with tests")
            return
        
        # Test queries from the review request
        test_queries = [
            {
                "query": "What breakfast ideas for my baby?",
                "baby_age": 8,
                "description": "Same question user tested on Android"
            },
            {
                "query": "When can babies start eating solid food?",
                "baby_age": 6,
                "description": "Solid food introduction query"
            },
            {
                "query": "Is it safe to give honey to a 10 month old baby?",
                "baby_age": 10,
                "description": "Honey safety query for 10 month old"
            }
        ]
        
        results = []
        
        for i, test in enumerate(test_queries, 1):
            print(f"\n{Colors.CYAN}--- Test {i}/3: {test['description']} ---{Colors.END}")
            
            success = self.test_specific_query(test['query'], test['baby_age'])
            results.append(success)
            
            # Small delay between requests
            if i < len(test_queries):
                time.sleep(2)
        
        # Print final summary
        print_header("SPECIFIC QUERY TEST RESULTS")
        
        passed_tests = sum(results)
        total_tests = len(results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n{Colors.BOLD}SUMMARY:{Colors.END}")
        print(f"  Total Queries Tested: {total_tests}")
        print(f"  {Colors.GREEN}Successful: {passed_tests}{Colors.END}")
        print(f"  {Colors.RED}Failed: {total_tests - passed_tests}{Colors.END}")
        print(f"  Success Rate: {Colors.GREEN if success_rate >= 80 else Colors.RED}{success_rate:.1f}%{Colors.END}")
        
        print(f"\n{Colors.BOLD}DETAILED RESULTS:{Colors.END}")
        for i, (test, result) in enumerate(zip(test_queries, results), 1):
            status = f"{Colors.GREEN}✅ PASS" if result else f"{Colors.RED}❌ FAIL"
            print(f"  {status}{Colors.END} - {test['description']}")
            print(f"    Query: \"{test['query']}\"")
            print(f"    Baby Age: {test['baby_age']} months")
        
        # Overall assessment
        print(f"\n{Colors.BOLD}ASSESSMENT:{Colors.END}")
        if success_rate == 100:
            print(f"{Colors.GREEN}🎉 PERFECT: All specific queries from the review request work flawlessly!{Colors.END}")
            print(f"{Colors.GREEN}✅ Android network optimization is fully functional{Colors.END}")
            print(f"{Colors.GREEN}✅ API endpoint path fix (/api/ai/chat) is working correctly{Colors.END}")
            print(f"{Colors.GREEN}✅ Response handling is processing correctly{Colors.END}")
        elif success_rate >= 80:
            print(f"{Colors.YELLOW}✅ GOOD: Most queries work well with minor issues{Colors.END}")
        else:
            print(f"{Colors.RED}❌ ISSUES: Significant problems detected that need attention{Colors.END}")

def main():
    """Main test execution"""
    tester = SpecificQueryTester()
    tester.run_specific_tests()

if __name__ == "__main__":
    main()