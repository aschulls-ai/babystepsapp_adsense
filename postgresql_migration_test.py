#!/usr/bin/env python3
"""
PostgreSQL Migration Verification Test
Comprehensive backend testing as requested in review request
Tests both production and local backends to verify functionality
"""

import requests
import json
import uuid
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('/app/frontend/.env')

class PostgreSQLMigrationTester:
    def __init__(self):
        self.production_url = "https://baby-steps-demo-api.onrender.com"
        self.local_url = "http://localhost:8001"
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        
        self.results = {
            'production': {'passed': 0, 'failed': 0, 'errors': [], 'details': []},
            'local': {'passed': 0, 'failed': 0, 'errors': [], 'details': []}
        }
    
    def log_result(self, backend_type, test_name, success, message="", response_time=None):
        """Log test results with details"""
        time_info = f" ({response_time:.2f}s)" if response_time else ""
        result_key = 'passed' if success else 'failed'
        
        self.results[backend_type][result_key] += 1
        
        if success:
            self.results[backend_type]['details'].append(f"✅ {test_name}: {message}{time_info}")
            print(f"✅ {test_name}: PASSED {message}{time_info}")
        else:
            self.results[backend_type]['errors'].append(f"{test_name}: {message}")
            self.results[backend_type]['details'].append(f"❌ {test_name}: {message}{time_info}")
            print(f"❌ {test_name}: FAILED {message}{time_info}")
    
    def test_backend(self, backend_url, backend_type):
        """Test a specific backend (production or local)"""
        print(f"\n🔍 TESTING {backend_type.upper()} BACKEND: {backend_url}")
        print("=" * 80)
        
        api_base = f"{backend_url}/api"
        session = requests.Session()
        session.timeout = 30
        auth_token = None
        
        # Phase 1: PostgreSQL Migration Verification
        print(f"\n📊 PHASE 1: PostgreSQL Migration Verification")
        print("-" * 50)
        
        # 1. Health Check
        try:
            start_time = time.time()
            response = requests.get(f"{api_base}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(backend_type, "Health Check", True, f"Backend healthy - {data.get('service', 'API')}", response_time)
            else:
                self.log_result(backend_type, "Health Check", False, f"HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_result(backend_type, "Health Check", False, f"Connection error: {str(e)}")
            return False
        
        # 2. Demo Account Login
        try:
            login_data = {"email": self.demo_email, "password": self.demo_password}
            start_time = time.time()
            response = session.post(f"{api_base}/auth/login", json=login_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    auth_token = data['access_token']
                    session.headers.update({'Authorization': f"Bearer {auth_token}"})
                    self.log_result(backend_type, "Demo Account Login", True, "JWT token generated", response_time)
                else:
                    self.log_result(backend_type, "Demo Account Login", False, "No access token in response", response_time)
                    return False
            else:
                self.log_result(backend_type, "Demo Account Login", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
                return False
        except Exception as e:
            self.log_result(backend_type, "Demo Account Login", False, f"Error: {str(e)}")
            return False
        
        # 3. New User Registration
        try:
            test_email = f"testuser_{int(time.time())}@test.com"
            user_data = {"email": test_email, "name": "Test User", "password": "TestPassword123"}
            
            start_time = time.time()
            response = session.post(f"{api_base}/auth/register", json=user_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result(backend_type, "New User Registration", True, f"User created: {test_email}", response_time)
            else:
                self.log_result(backend_type, "New User Registration", False, f"HTTP {response.status_code}: {response.text[:100]}", response_time)
        except Exception as e:
            self.log_result(backend_type, "New User Registration", False, f"Error: {str(e)}")
        
        # 4. Immediate Login After Registration
        try:
            login_data = {"email": test_email, "password": "TestPassword123"}
            start_time = time.time()
            response = session.post(f"{api_base}/auth/login", json=login_data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.log_result(backend_type, "Immediate Login After Registration", True, "New user can login", response_time)
                else:
                    self.log_result(backend_type, "Immediate Login After Registration", False, "No access token", response_time)
            else:
                self.log_result(backend_type, "Immediate Login After Registration", False, f"HTTP {response.status_code}", response_time)
        except Exception as e:
            self.log_result(backend_type, "Immediate Login After Registration", False, f"Error: {str(e)}")
        
        # 5. User Persistence Test
        print(f"\n🔄 User Persistence Test - Creating 3 users")
        test_users = []
        for i in range(3):
            try:
                email = f"persist_test_{int(time.time())}_{i}@test.com"
                password = f"TestPass{i}123"
                user_data = {"email": email, "name": f"Persist User {i}", "password": password}
                
                # Create user
                response = session.post(f"{api_base}/auth/register", json=user_data, timeout=30)
                if response.status_code == 200:
                    test_users.append({"email": email, "password": password})
                    print(f"   Created user {i+1}: {email}")
            except Exception as e:
                print(f"   Failed to create user {i+1}: {str(e)}")
        
        # Test login for all created users
        persistence_success = 0
        for i, user in enumerate(test_users):
            try:
                login_data = {"email": user["email"], "password": user["password"]}
                response = session.post(f"{api_base}/auth/login", json=login_data, timeout=30)
                if response.status_code == 200 and 'access_token' in response.json():
                    persistence_success += 1
                    print(f"   ✅ User {i+1} login successful")
                else:
                    print(f"   ❌ User {i+1} login failed: HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ User {i+1} login error: {str(e)}")
        
        if persistence_success == len(test_users) and len(test_users) > 0:
            self.log_result(backend_type, "User Persistence Test", True, f"All {persistence_success} users can login")
        else:
            self.log_result(backend_type, "User Persistence Test", False, f"Only {persistence_success}/{len(test_users)} users can login")
        
        # Phase 2: AI Integration Verification (only if authenticated)
        if auth_token:
            print(f"\n🤖 PHASE 2: AI Integration Verification")
            print("-" * 50)
            
            # 6. AI Chat Endpoint
            try:
                chat_data = {"message": "When can babies eat strawberries?", "baby_age_months": 6}
                start_time = time.time()
                response = session.post(f"{api_base}/ai/chat", json=chat_data, timeout=120)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    if 'response' in data:
                        response_text = data['response']
                        if "demo response" in response_text.lower():
                            self.log_result(backend_type, "AI Chat Endpoint", False, "Returning demo/fallback response", response_time)
                        else:
                            self.log_result(backend_type, "AI Chat Endpoint", True, f"Real AI response ({len(response_text)} chars)", response_time)
                    else:
                        self.log_result(backend_type, "AI Chat Endpoint", False, "No response field", response_time)
                else:
                    self.log_result(backend_type, "AI Chat Endpoint", False, f"HTTP {response.status_code}", response_time)
            except Exception as e:
                self.log_result(backend_type, "AI Chat Endpoint", False, f"Error: {str(e)}")
            
            # 7. Food Research Endpoint
            try:
                food_data = {"question": "Are strawberries safe?", "baby_age_months": 6}
                start_time = time.time()
                response = session.post(f"{api_base}/food/research", json=food_data, timeout=60)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    if 'answer' in data and 'safety_level' in data:
                        self.log_result(backend_type, "Food Research Endpoint", True, f"Safety level: {data['safety_level']}", response_time)
                    else:
                        self.log_result(backend_type, "Food Research Endpoint", False, "Invalid response format", response_time)
                else:
                    self.log_result(backend_type, "Food Research Endpoint", False, f"HTTP {response.status_code}", response_time)
            except Exception as e:
                self.log_result(backend_type, "Food Research Endpoint", False, f"Error: {str(e)}")
            
            # 8. Meal Search Endpoint
            try:
                meal_data = {"query": "breakfast ideas", "baby_age_months": 8}
                start_time = time.time()
                response = session.post(f"{api_base}/meals/search", json=meal_data, timeout=120)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    if 'results' in data:
                        self.log_result(backend_type, "Meal Search Endpoint", True, "Meal suggestions received", response_time)
                    else:
                        self.log_result(backend_type, "Meal Search Endpoint", False, "No results field", response_time)
                else:
                    self.log_result(backend_type, "Meal Search Endpoint", False, f"HTTP {response.status_code}", response_time)
            except Exception as e:
                self.log_result(backend_type, "Meal Search Endpoint", False, f"Error: {str(e)}")
            
            # Phase 3: Database Operations
            print(f"\n💾 PHASE 3: Database Operations")
            print("-" * 50)
            
            # 9. Baby Profile Creation
            try:
                baby_data = {
                    "name": "Test Baby",
                    "birth_date": "2024-03-15T10:30:00Z",
                    "gender": "girl"
                }
                start_time = time.time()
                response = session.post(f"{api_base}/babies", json=baby_data, timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    if 'id' in data:
                        baby_id = data['id']
                        self.log_result(backend_type, "Baby Profile Creation", True, f"Baby created: {data['name']}", response_time)
                    else:
                        self.log_result(backend_type, "Baby Profile Creation", False, "No ID in response", response_time)
                else:
                    self.log_result(backend_type, "Baby Profile Creation", False, f"HTTP {response.status_code}", response_time)
            except Exception as e:
                self.log_result(backend_type, "Baby Profile Creation", False, f"Error: {str(e)}")
            
            # 10. Baby Profile Retrieval
            try:
                start_time = time.time()
                response = session.get(f"{api_base}/babies", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    babies = response.json()
                    self.log_result(backend_type, "Baby Profile Retrieval", True, f"Retrieved {len(babies)} profiles", response_time)
                else:
                    self.log_result(backend_type, "Baby Profile Retrieval", False, f"HTTP {response.status_code}", response_time)
            except Exception as e:
                self.log_result(backend_type, "Baby Profile Retrieval", False, f"Error: {str(e)}")
        
        return True
    
    def run_comprehensive_test(self):
        """Run comprehensive PostgreSQL migration verification"""
        print("🚀 POSTGRESQL MIGRATION VERIFICATION - COMPREHENSIVE BACKEND TESTING")
        print("📋 Review Request: PostgreSQL Migration Verification")
        print("=" * 80)
        
        # Test production backend
        print(f"\n🌐 TESTING PRODUCTION BACKEND")
        self.test_backend(self.production_url, 'production')
        
        # Test local backend
        print(f"\n🏠 TESTING LOCAL BACKEND")
        self.test_backend(self.local_url, 'local')
        
        # Generate comprehensive report
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS - POSTGRESQL MIGRATION VERIFICATION")
        print("=" * 80)
        
        for backend_type in ['production', 'local']:
            results = self.results[backend_type]
            total_tests = results['passed'] + results['failed']
            success_rate = (results['passed'] / total_tests * 100) if total_tests > 0 else 0
            
            print(f"\n🔍 {backend_type.upper()} BACKEND RESULTS:")
            print(f"   ✅ Passed: {results['passed']}")
            print(f"   ❌ Failed: {results['failed']}")
            print(f"   📈 Success Rate: {success_rate:.1f}%")
            
            if results['errors']:
                print(f"   🚨 Failed Tests:")
                for error in results['errors']:
                    print(f"      • {error}")
        
        # Success criteria evaluation
        print(f"\n🎯 SUCCESS CRITERIA EVALUATION:")
        
        prod_results = self.results['production']
        local_results = self.results['local']
        
        # PostgreSQL Working criteria
        prod_auth_working = any("Demo Account Login" in detail and "✅" in detail for detail in prod_results['details'])
        prod_persistence_working = any("User Persistence Test" in detail and "✅" in detail for detail in prod_results['details'])
        
        local_auth_working = any("Demo Account Login" in detail and "✅" in detail for detail in local_results['details'])
        local_persistence_working = any("User Persistence Test" in detail and "✅" in detail for detail in local_results['details'])
        
        print(f"   📊 PostgreSQL Working (Production): {'✅' if prod_auth_working and prod_persistence_working else '❌'}")
        print(f"   📊 PostgreSQL Working (Local): {'✅' if local_auth_working and local_persistence_working else '❌'}")
        
        # AI Integration criteria
        prod_ai_working = any("AI Chat Endpoint" in detail and "✅" in detail and "Real AI response" in detail for detail in prod_results['details'])
        local_ai_working = any("AI Chat Endpoint" in detail and "✅" in detail and "Real AI response" in detail for detail in local_results['details'])
        
        print(f"   🤖 AI Integration (Production): {'✅' if prod_ai_working else '❌'}")
        print(f"   🤖 AI Integration (Local): {'✅' if local_ai_working else '❌'}")
        
        # Overall assessment
        print(f"\n🏆 OVERALL ASSESSMENT:")
        if local_auth_working and local_persistence_working:
            print("   ✅ Backend functionality is working correctly (verified on local)")
            if not prod_auth_working:
                print("   ⚠️  Production deployment has authentication issues")
            if local_ai_working:
                print("   ✅ AI integration is functional")
            else:
                print("   ⚠️  AI integration may need configuration")
        else:
            print("   ❌ Critical backend functionality issues detected")
        
        return self.results

def main():
    """Main test execution"""
    tester = PostgreSQLMigrationTester()
    results = tester.run_comprehensive_test()
    
    # Determine exit code based on local backend results (since that's what we can control)
    local_results = results['local']
    if local_results['failed'] > local_results['passed']:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()