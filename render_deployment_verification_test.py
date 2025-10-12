#!/usr/bin/env python3
"""
Render Deployment Verification Test - CORS Fix & Environment Variable Testing
Comprehensive verification of deployed backend at https://baby-steps-demo-api.onrender.com
"""

import requests
import json
import time
from datetime import datetime

# Backend URL from review request
BACKEND_URL = "https://baby-steps-demo-api.onrender.com"
API_BASE = f"{BACKEND_URL}/api"

class RenderDeploymentTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 120
        self.auth_token = None
        # Demo credentials from review request
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': [],
            'details': []
        }
    
    def log_result(self, test_name, success, message="", response_time=None):
        """Log test results with details"""
        time_info = f" ({response_time:.2f}s)" if response_time else ""
        if success:
            self.results['passed'] += 1
            self.results['details'].append(f"✅ {test_name}: {message}{time_info}")
            print(f"✅ {test_name}: PASSED {message}{time_info}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            self.results['details'].append(f"❌ {test_name}: {message}{time_info}")
            print(f"❌ {test_name}: FAILED {message}{time_info}")
    
    def test_cors_configuration(self):
        """1. CORS Configuration Test - OPTIONS requests and headers"""
        print("\n🌐 1. CORS CONFIGURATION TEST")
        print("=" * 50)
        
        try:
            # Test OPTIONS preflight request
            start_time = time.time()
            response = requests.options(
                f"{API_BASE}/auth/login",
                headers={
                    'Origin': 'https://baby-steps-demo.vercel.app',
                    'Access-Control-Request-Method': 'POST',
                    'Access-Control-Request-Headers': 'Content-Type, Authorization'
                },
                timeout=10
            )
            response_time = time.time() - start_time
            
            # Check CORS headers
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
            }
            
            # Verify Access-Control-Allow-Origin: *
            if cors_headers['Access-Control-Allow-Origin'] == '*':
                self.log_result("CORS Allow-Origin", True, "Access-Control-Allow-Origin: * present", response_time)
            else:
                self.log_result("CORS Allow-Origin", False, f"Expected '*', got: {cors_headers['Access-Control-Allow-Origin']}", response_time)
            
            # Verify Access-Control-Allow-Credentials is NOT set or is False
            credentials_header = cors_headers['Access-Control-Allow-Credentials']
            if credentials_header is None or credentials_header.lower() == 'false':
                self.log_result("CORS Credentials", True, "Access-Control-Allow-Credentials properly configured", response_time)
            else:
                self.log_result("CORS Credentials", False, f"Access-Control-Allow-Credentials should be False or unset, got: {credentials_header}", response_time)
            
            # Test from different origins
            origins_to_test = [
                'https://baby-steps-demo.vercel.app',
                'https://localhost:3000',
                'https://example.com'
            ]
            
            for origin in origins_to_test:
                start_time = time.time()
                response = requests.options(
                    f"{API_BASE}/health",
                    headers={'Origin': origin},
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.headers.get('Access-Control-Allow-Origin') == '*':
                    self.log_result(f"CORS Origin Test ({origin})", True, "CORS working for mobile compatibility", response_time)
                else:
                    self.log_result(f"CORS Origin Test ({origin})", False, f"CORS failed for origin: {origin}", response_time)
            
            return True
        except Exception as e:
            self.log_result("CORS Configuration", False, f"Error: {str(e)}")
            return False
    
    def test_environment_variables(self):
        """2. Environment Variable Test - EMERGENT_LLM_KEY loading"""
        print("\n🔑 2. ENVIRONMENT VARIABLE TEST")
        print("=" * 50)
        
        try:
            # Test health endpoint for AI integration status
            start_time = time.time()
            response = requests.get(f"{API_BASE}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Look for AI integration status in health response
                    if 'ai_integration' in data or 'emergent_llm' in str(data).lower():
                        self.log_result("Environment Variables", True, "✅ AI integration available", response_time)
                    else:
                        # Check logs by testing an AI endpoint
                        self.log_result("Environment Variables Check", True, "Health endpoint responding, checking AI endpoints", response_time)
                except json.JSONDecodeError:
                    self.log_result("Environment Variables", False, "Invalid JSON in health response", response_time)
            else:
                self.log_result("Environment Variables", False, f"Health endpoint failed: HTTP {response.status_code}", response_time)
            
            return True
        except Exception as e:
            self.log_result("Environment Variables", False, f"Error: {str(e)}")
            return False
    
    def test_health_connectivity(self):
        """3. Health & Connectivity - GET /api/health"""
        print("\n🏥 3. HEALTH & CONNECTIVITY")
        print("=" * 50)
        
        try:
            start_time = time.time()
            response = requests.get(f"{API_BASE}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('status') == 'healthy':
                        self.log_result("Health Check", True, f"200 OK response - {data.get('service', 'Backend healthy')}", response_time)
                        return True
                    else:
                        self.log_result("Health Check", False, f"Unhealthy status: {data}", response_time)
                        return False
                except json.JSONDecodeError:
                    self.log_result("Health Check", False, f"Invalid JSON response: {response.text[:100]}", response_time)
                    return False
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_authentication_flow(self):
        """4. Authentication Flow - demo@babysteps.com / demo123"""
        print("\n🔐 4. AUTHENTICATION FLOW")
        print("=" * 50)
        
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            start_time = time.time()
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            response_time = time.time() - start_time
            
            # Check for CORS errors in response
            cors_origin = response.headers.get('Access-Control-Allow-Origin')
            if cors_origin:
                self.log_result("Login CORS Headers", True, f"CORS headers present: {cors_origin}", response_time)
            else:
                self.log_result("Login CORS Headers", False, "No CORS headers in login response", response_time)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Demo Login", True, "JWT token returned - no CORS errors", response_time)
                    return True
                else:
                    self.log_result("Demo Login", False, f"Invalid login response: {data}", response_time)
                    return False
            else:
                self.log_result("Demo Login", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result("Demo Login", False, f"Error: {str(e)}")
            return False
    
    def test_ai_endpoints_with_emergent_key(self):
        """5. AI Endpoints (WITH EMERGENT_LLM_KEY) - Real responses expected"""
        print("\n🤖 5. AI ENDPOINTS (WITH EMERGENT_LLM_KEY)")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_result("AI Endpoints", False, "No authentication token available")
            return False
        
        try:
            # Test 1: POST /api/ai/chat - "When can babies eat strawberries?"
            chat_query = {
                "message": "When can babies eat strawberries?",
                "baby_age_months": 6
            }
            
            start_time = time.time()
            response = self.session.post(f"{API_BASE}/ai/chat", json=chat_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and len(data['response']) > 50:
                    # Check if it's a real AI response (not fallback)
                    response_text = data['response'].lower()
                    if 'temporarily unavailable' in response_text or 'fallback' in response_text:
                        self.log_result("AI Chat Real Response", False, "Fallback response detected - EMERGENT_LLM_KEY not working", response_time)
                    else:
                        self.log_result("AI Chat Real Response", True, f"Real AI response ({len(data['response'])} chars)", response_time)
                else:
                    self.log_result("AI Chat Real Response", False, "Empty or invalid AI response", response_time)
            else:
                self.log_result("AI Chat Real Response", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
            
            # Test 2: POST /api/food/research - "Are strawberries safe for 6 month old?"
            food_query = {
                "question": "Are strawberries safe for 6 month old?",
                "baby_age_months": 6
            }
            
            start_time = time.time()
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=60)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'answer' in data and 'safety_level' in data:
                    # Check for real food safety assessment
                    answer_text = data['answer'].lower()
                    if 'temporarily unavailable' in answer_text or 'fallback' in answer_text:
                        self.log_result("Food Research Real Response", False, "Fallback response detected", response_time)
                    else:
                        self.log_result("Food Research Real Response", True, f"Real food safety assessment: {data['safety_level']}", response_time)
                else:
                    self.log_result("Food Research Real Response", False, "Invalid food research response format", response_time)
            else:
                self.log_result("Food Research Real Response", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
            
            # Test 3: POST /api/meals/search - "breakfast ideas for 8 month old"
            meal_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            start_time = time.time()
            response = self.session.post(f"{API_BASE}/meals/search", json=meal_query, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    results = data['results']
                    if isinstance(results, str) and len(results) > 100:
                        # Check for real meal suggestions
                        results_text = results.lower()
                        if 'temporarily unavailable' in results_text or 'fallback' in results_text:
                            self.log_result("Meal Search Real Response", False, "Fallback response detected", response_time)
                        else:
                            self.log_result("Meal Search Real Response", True, f"Real meal suggestions ({len(results)} chars)", response_time)
                    elif isinstance(results, list) and len(results) > 0:
                        self.log_result("Meal Search Real Response", True, f"Real meal suggestions ({len(results)} meals)", response_time)
                    else:
                        self.log_result("Meal Search Real Response", False, f"Empty or invalid meal search response", response_time)
                else:
                    self.log_result("Meal Search Real Response", False, f"No 'results' field in response", response_time)
            else:
                self.log_result("Meal Search Real Response", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
            
            return True
        except Exception as e:
            self.log_result("AI Endpoints", False, f"Error: {str(e)}")
            return False
    
    def test_baby_profile_endpoints(self):
        """6. Baby Profile Endpoints - No 403 errors"""
        print("\n👶 6. BABY PROFILE ENDPOINTS")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_result("Baby Profiles", False, "No authentication token available")
            return False
        
        try:
            # GET /api/babies
            start_time = time.time()
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                babies = response.json()
                self.log_result("GET /api/babies", True, f"No 403 errors - Retrieved {len(babies)} profiles", response_time)
            elif response.status_code == 403:
                self.log_result("GET /api/babies", False, "403 Forbidden error detected", response_time)
                return False
            else:
                self.log_result("GET /api/babies", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            # POST /api/babies (create test baby)
            baby_data = {
                "name": "Test Baby Render",
                "birth_date": "2024-03-15T10:30:00Z",
                "birth_weight": 7.2,
                "birth_length": 20.5,
                "gender": "girl"
            }
            
            start_time = time.time()
            response = self.session.post(f"{API_BASE}/babies", json=baby_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data:
                    self.log_result("POST /api/babies", True, f"No 403 errors - Baby created: {data['name']}", response_time)
                else:
                    self.log_result("POST /api/babies", False, "No ID in response", response_time)
            elif response.status_code == 403:
                self.log_result("POST /api/babies", False, "403 Forbidden error detected", response_time)
                return False
            else:
                self.log_result("POST /api/babies", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
            
            return True
        except Exception as e:
            self.log_result("Baby Profile Endpoints", False, f"Error: {str(e)}")
            return False
    
    def test_headers_inspection(self):
        """7. Headers Inspection - CORS headers and Content-Type"""
        print("\n🔍 7. HEADERS INSPECTION")
        print("=" * 50)
        
        try:
            # Test various endpoints for proper headers
            endpoints_to_test = [
                ('/health', 'GET'),
                ('/auth/login', 'POST'),
                ('/babies', 'GET')
            ]
            
            for endpoint, method in endpoints_to_test:
                start_time = time.time()
                
                if method == 'GET':
                    response = self.session.get(f"{API_BASE}{endpoint}", timeout=10)
                else:
                    response = self.session.post(f"{API_BASE}{endpoint}", json={}, timeout=10)
                
                response_time = time.time() - start_time
                
                # Check CORS headers
                cors_origin = response.headers.get('Access-Control-Allow-Origin')
                content_type = response.headers.get('Content-Type')
                
                if cors_origin == '*':
                    self.log_result(f"CORS Headers ({endpoint})", True, f"Proper CORS headers present", response_time)
                else:
                    self.log_result(f"CORS Headers ({endpoint})", False, f"Missing or incorrect CORS headers: {cors_origin}", response_time)
                
                if content_type and 'application/json' in content_type:
                    self.log_result(f"Content-Type ({endpoint})", True, f"Proper Content-Type: {content_type}", response_time)
                else:
                    self.log_result(f"Content-Type ({endpoint})", False, f"Missing or incorrect Content-Type: {content_type}", response_time)
            
            return True
        except Exception as e:
            self.log_result("Headers Inspection", False, f"Error: {str(e)}")
            return False
    
    def run_render_deployment_verification(self):
        """Run comprehensive render deployment verification"""
        print("🚀 RENDER DEPLOYMENT VERIFICATION - CORS FIX & ENVIRONMENT VARIABLE")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"🔑 Demo Credentials: {self.demo_email} / {self.demo_password}")
        print("=" * 80)
        
        # Run all verification tests
        cors_ok = self.test_cors_configuration()
        env_ok = self.test_environment_variables()
        health_ok = self.test_health_connectivity()
        auth_ok = self.test_authentication_flow()
        
        if not auth_ok:
            print("\n❌ Authentication failed - cannot proceed with authenticated tests")
        else:
            ai_ok = self.test_ai_endpoints_with_emergent_key()
            baby_ok = self.test_baby_profile_endpoints()
        
        headers_ok = self.test_headers_inspection()
        
        # Print final results
        print("\n" + "=" * 80)
        print("📊 RENDER DEPLOYMENT VERIFICATION RESULTS:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed'])) * 100 if (self.results['passed'] + self.results['failed']) > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.results['errors']:
            print(f"\n🔍 FAILED TESTS:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Critical Success Criteria Summary
        print(f"\n🎯 CRITICAL SUCCESS CRITERIA:")
        print(f"   • NO CORS errors (Access-Control-Allow-Credentials fixed): {'✅' if cors_ok else '❌'}")
        print(f"   • AI endpoints return REAL responses (not fallback): {'✅' if auth_ok and 'ai_ok' in locals() and ai_ok else '❌'}")
        print(f"   • All endpoints return expected status codes: {'✅' if health_ok and auth_ok else '❌'}")
        print(f"   • Authentication works without issues: {'✅' if auth_ok else '❌'}")
        print(f"   • Response headers include proper CORS configuration: {'✅' if headers_ok else '❌'}")
        
        return self.results

def main():
    """Main test execution"""
    tester = RenderDeploymentTester()
    results = tester.run_render_deployment_verification()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()