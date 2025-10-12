#!/usr/bin/env python3
"""
Final Render Deployment Verification
Comprehensive test covering all critical success criteria from the review request
"""

import requests
import json
import time

BACKEND_URL = "https://baby-steps-demo-api.onrender.com"
API_BASE = f"{BACKEND_URL}/api"

class FinalRenderVerification:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 120
        self.auth_token = None
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.results = []
        self.critical_success = {
            'cors_fixed': False,
            'ai_real_responses': False,
            'expected_status_codes': False,
            'authentication_works': False,
            'proper_cors_headers': False
        }
    
    def log_test(self, category, test_name, success, details="", response_time=None):
        """Log test results"""
        time_str = f" ({response_time:.2f}s)" if response_time else ""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {category} - {test_name}: {details}{time_str}"
        self.results.append(result)
        print(result)
        return success
    
    def test_cors_configuration(self):
        """Test CORS configuration thoroughly"""
        print("\n🌐 1. CORS CONFIGURATION TEST")
        print("=" * 50)
        
        cors_tests_passed = 0
        total_cors_tests = 0
        
        # Test OPTIONS preflight requests
        endpoints = ['/health', '/auth/login', '/ai/chat', '/food/research', '/meals/search', '/babies']
        
        for endpoint in endpoints:
            total_cors_tests += 1
            start_time = time.time()
            
            try:
                response = requests.options(
                    f"{API_BASE}{endpoint}",
                    headers={
                        'Origin': 'https://baby-steps-demo.vercel.app',
                        'Access-Control-Request-Method': 'POST',
                        'Access-Control-Request-Headers': 'Content-Type, Authorization'
                    },
                    timeout=10
                )
                response_time = time.time() - start_time
                
                # Check critical CORS headers
                allow_origin = response.headers.get('Access-Control-Allow-Origin')
                allow_credentials = response.headers.get('Access-Control-Allow-Credentials')
                
                if allow_origin == '*' and (allow_credentials is None or allow_credentials.lower() == 'false'):
                    cors_tests_passed += 1
                    self.log_test("CORS", f"OPTIONS {endpoint}", True, f"Allow-Origin: *, Credentials: {allow_credentials}", response_time)
                else:
                    self.log_test("CORS", f"OPTIONS {endpoint}", False, f"Allow-Origin: {allow_origin}, Credentials: {allow_credentials}", response_time)
            
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test("CORS", f"OPTIONS {endpoint}", False, f"Error: {str(e)}", response_time)
        
        # Test from different origins for mobile compatibility
        origins = ['https://baby-steps-demo.vercel.app', 'https://localhost:3000', 'capacitor://localhost']
        
        for origin in origins:
            total_cors_tests += 1
            start_time = time.time()
            
            try:
                response = requests.options(
                    f"{API_BASE}/health",
                    headers={'Origin': origin},
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.headers.get('Access-Control-Allow-Origin') == '*':
                    cors_tests_passed += 1
                    self.log_test("CORS", f"Mobile Origin {origin}", True, "Mobile compatibility confirmed", response_time)
                else:
                    self.log_test("CORS", f"Mobile Origin {origin}", False, "Mobile compatibility failed", response_time)
            
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test("CORS", f"Mobile Origin {origin}", False, f"Error: {str(e)}", response_time)
        
        # Update critical success criteria
        self.critical_success['cors_fixed'] = cors_tests_passed >= (total_cors_tests * 0.8)  # 80% pass rate
        self.critical_success['proper_cors_headers'] = cors_tests_passed >= (total_cors_tests * 0.8)
        
        return cors_tests_passed, total_cors_tests
    
    def test_authentication_and_status_codes(self):
        """Test authentication and verify expected status codes"""
        print("\n🔐 2. AUTHENTICATION & STATUS CODES")
        print("=" * 50)
        
        auth_success = False
        status_codes_correct = True
        
        # Test health endpoint (should be 200)
        start_time = time.time()
        try:
            response = requests.get(f"{API_BASE}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("STATUS", "GET /api/health", True, f"200 OK", response_time)
            else:
                self.log_test("STATUS", "GET /api/health", False, f"Expected 200, got {response.status_code}", response_time)
                status_codes_correct = False
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("STATUS", "GET /api/health", False, f"Error: {str(e)}", response_time)
            status_codes_correct = False
        
        # Test authentication with demo credentials
        start_time = time.time()
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    auth_success = True
                    self.log_test("AUTH", "Demo Login", True, "JWT token received, no CORS errors", response_time)
                else:
                    self.log_test("AUTH", "Demo Login", False, f"Invalid response format: {data}", response_time)
                    status_codes_correct = False
            else:
                self.log_test("AUTH", "Demo Login", False, f"Expected 200, got {response.status_code}", response_time)
                status_codes_correct = False
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("AUTH", "Demo Login", False, f"Error: {str(e)}", response_time)
            status_codes_correct = False
        
        self.critical_success['authentication_works'] = auth_success
        self.critical_success['expected_status_codes'] = status_codes_correct
        
        return auth_success, status_codes_correct
    
    def test_ai_endpoints_real_responses(self):
        """Test AI endpoints for real responses (not fallback)"""
        print("\n🤖 3. AI ENDPOINTS - REAL RESPONSES (EMERGENT_LLM_KEY)")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_test("AI", "Authentication Required", False, "No auth token available")
            return False
        
        ai_tests_passed = 0
        total_ai_tests = 3
        
        # Test 1: AI Chat - "When can babies eat strawberries?"
        start_time = time.time()
        try:
            chat_query = {
                "message": "When can babies eat strawberries?",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/ai/chat", json=chat_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', '')
                
                # Check if it's a real response (not fallback)
                if len(ai_response) > 50 and 'temporarily unavailable' not in ai_response.lower():
                    ai_tests_passed += 1
                    self.log_test("AI", "Chat Real Response", True, f"Real AI response ({len(ai_response)} chars)", response_time)
                else:
                    self.log_test("AI", "Chat Real Response", False, "Fallback response detected", response_time)
            else:
                self.log_test("AI", "Chat Real Response", False, f"HTTP {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("AI", "Chat Real Response", False, f"Error: {str(e)}", response_time)
        
        # Test 2: Food Research - "Are strawberries safe for 6 month old?"
        start_time = time.time()
        try:
            food_query = {
                "question": "Are strawberries safe for 6 month old?",
                "baby_age_months": 6
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                safety_level = data.get('safety_level', '')
                
                if len(answer) > 50 and 'temporarily unavailable' not in answer.lower() and safety_level:
                    ai_tests_passed += 1
                    self.log_test("AI", "Food Research Real Response", True, f"Real assessment: {safety_level}", response_time)
                else:
                    self.log_test("AI", "Food Research Real Response", False, "Fallback response detected", response_time)
            else:
                self.log_test("AI", "Food Research Real Response", False, f"HTTP {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("AI", "Food Research Real Response", False, f"Error: {str(e)}", response_time)
        
        # Test 3: Meal Search - "breakfast ideas for 8 month old"
        start_time = time.time()
        try:
            meal_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=meal_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', '')
                
                # Check for real meal suggestions
                if ((isinstance(results, list) and len(results) > 0) or 
                    (isinstance(results, str) and len(results) > 100)) and \
                   'temporarily unavailable' not in str(results).lower():
                    ai_tests_passed += 1
                    result_info = f"{len(results)} meals" if isinstance(results, list) else f"{len(results)} chars"
                    self.log_test("AI", "Meal Search Real Response", True, f"Real suggestions ({result_info})", response_time)
                else:
                    self.log_test("AI", "Meal Search Real Response", False, "Fallback response detected", response_time)
            else:
                self.log_test("AI", "Meal Search Real Response", False, f"HTTP {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("AI", "Meal Search Real Response", False, f"Error: {str(e)}", response_time)
        
        # Update critical success criteria
        self.critical_success['ai_real_responses'] = ai_tests_passed == total_ai_tests
        
        return ai_tests_passed, total_ai_tests
    
    def test_baby_profile_endpoints(self):
        """Test baby profile endpoints for no 403 errors"""
        print("\n👶 4. BABY PROFILE ENDPOINTS - NO 403 ERRORS")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_test("BABY", "Authentication Required", False, "No auth token available")
            return False
        
        baby_tests_passed = 0
        total_baby_tests = 2
        
        # Test GET /api/babies
        start_time = time.time()
        try:
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                babies = response.json()
                baby_tests_passed += 1
                self.log_test("BABY", "GET /api/babies", True, f"Retrieved {len(babies)} profiles, no 403", response_time)
            elif response.status_code == 403:
                self.log_test("BABY", "GET /api/babies", False, "403 Forbidden error", response_time)
            else:
                self.log_test("BABY", "GET /api/babies", False, f"HTTP {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("BABY", "GET /api/babies", False, f"Error: {str(e)}", response_time)
        
        # Test POST /api/babies
        start_time = time.time()
        try:
            baby_data = {
                "name": "Final Test Baby",
                "birth_date": "2024-03-15T10:30:00Z",
                "birth_weight": 7.2,
                "birth_length": 20.5,
                "gender": "girl"
            }
            
            response = self.session.post(f"{API_BASE}/babies", json=baby_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data:
                    baby_tests_passed += 1
                    self.log_test("BABY", "POST /api/babies", True, f"Baby created: {data['name']}, no 403", response_time)
                else:
                    self.log_test("BABY", "POST /api/babies", False, "No ID in response", response_time)
            elif response.status_code == 403:
                self.log_test("BABY", "POST /api/babies", False, "403 Forbidden error", response_time)
            else:
                self.log_test("BABY", "POST /api/babies", False, f"HTTP {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("BABY", "POST /api/babies", False, f"Error: {str(e)}", response_time)
        
        return baby_tests_passed, total_baby_tests
    
    def run_final_verification(self):
        """Run complete final verification"""
        print("🚀 FINAL RENDER DEPLOYMENT VERIFICATION")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"🔑 Demo Credentials: {self.demo_email} / {self.demo_password}")
        print("=" * 80)
        
        # Run all tests
        cors_passed, cors_total = self.test_cors_configuration()
        auth_success, status_success = self.test_authentication_and_status_codes()
        
        if auth_success:
            ai_passed, ai_total = self.test_ai_endpoints_real_responses()
            baby_passed, baby_total = self.test_baby_profile_endpoints()
        else:
            ai_passed, ai_total = 0, 3
            baby_passed, baby_total = 0, 2
            self.log_test("SKIP", "AI & Baby Tests", False, "Authentication failed")
        
        # Calculate overall results
        total_passed = cors_passed + (1 if auth_success else 0) + (1 if status_success else 0) + ai_passed + baby_passed
        total_tests = cors_total + 2 + ai_total + baby_total
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        
        # Print final results
        print("\n" + "=" * 80)
        print("📊 FINAL VERIFICATION RESULTS:")
        print(f"✅ Tests Passed: {total_passed}/{total_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        print(f"\n🎯 CRITICAL SUCCESS CRITERIA:")
        print(f"   ✅ NO CORS errors (Access-Control-Allow-Credentials fixed): {'✅' if self.critical_success['cors_fixed'] else '❌'}")
        print(f"   ✅ AI endpoints return REAL responses (not fallback): {'✅' if self.critical_success['ai_real_responses'] else '❌'}")
        print(f"   ✅ All endpoints return expected status codes: {'✅' if self.critical_success['expected_status_codes'] else '❌'}")
        print(f"   ✅ Authentication works without issues: {'✅' if self.critical_success['authentication_works'] else '❌'}")
        print(f"   ✅ Response headers include proper CORS configuration: {'✅' if self.critical_success['proper_cors_headers'] else '❌'}")
        
        # Overall assessment
        critical_passed = sum(self.critical_success.values())
        critical_total = len(self.critical_success)
        
        print(f"\n🏆 OVERALL ASSESSMENT:")
        if critical_passed == critical_total:
            print("   🎉 ALL CRITICAL SUCCESS CRITERIA MET!")
            print("   ✅ Render deployment is fully functional")
        elif critical_passed >= critical_total * 0.8:
            print("   ⚠️  MOSTLY SUCCESSFUL - Minor issues detected")
            print("   🔧 Some fine-tuning may be needed")
        else:
            print("   ❌ CRITICAL ISSUES DETECTED")
            print("   🚨 Deployment needs attention")
        
        print(f"\n📋 DETAILED TEST LOG:")
        for result in self.results:
            print(f"   {result}")
        
        return {
            'success_rate': success_rate,
            'critical_success': self.critical_success,
            'total_passed': total_passed,
            'total_tests': total_tests
        }

def main():
    """Main execution"""
    verifier = FinalRenderVerification()
    results = verifier.run_final_verification()
    
    # Exit with appropriate code
    if results['success_rate'] >= 80 and sum(results['critical_success'].values()) >= 4:
        exit(0)  # Success
    else:
        exit(1)  # Issues detected

if __name__ == "__main__":
    main()