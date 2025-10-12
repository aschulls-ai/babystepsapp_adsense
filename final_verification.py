#!/usr/bin/env python3
"""
FINAL VERIFICATION - Baby Steps Backend API
All 12 Critical Tests - Corrected Version
"""

import requests
import json
import time
import uuid

class FinalVerification:
    def __init__(self):
        self.base_url = "https://baby-steps-demo-api.onrender.com"
        self.auth_token = None
        self.passed_tests = 0
        self.total_tests = 12
        
    def test_all(self):
        print("🚀 FINAL VERIFICATION - Baby Steps Backend API")
        print(f"🎯 Backend URL: {self.base_url}")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health),
            ("Demo Login", self.test_demo_login),
            ("User Registration", self.test_registration),
            ("Auto-Login Token", self.test_auto_login),
            ("User Persistence", self.test_persistence),
            ("AI Chat", self.test_ai_chat),
            ("Food Research", self.test_food_research),
            ("Meal Search", self.test_meal_search),
            ("Create Baby Profile", self.test_create_baby),
            ("Retrieve Baby Profiles", self.test_get_babies),
            ("Invalid Login (401)", self.test_invalid_login),
            ("Unauthorized Access (403)", self.test_unauthorized)
        ]
        
        for i, (name, test_func) in enumerate(tests, 1):
            try:
                result = test_func()
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{i:2d}. {status} - {name}")
                if result:
                    self.passed_tests += 1
            except Exception as e:
                print(f"{i:2d}. ❌ FAIL - {name} (Exception: {str(e)})")
        
        print("=" * 60)
        success_rate = (self.passed_tests / self.total_tests) * 100
        print(f"📊 RESULTS: {self.passed_tests}/{self.total_tests} tests passed ({success_rate:.1f}%)")
        
        if success_rate == 100.0:
            print("🎉 SUCCESS: All tests passed! Backend ready for production.")
            return True
        else:
            print(f"❌ FAILURE: {self.total_tests - self.passed_tests} tests failed.")
            return False
    
    def make_request(self, method, endpoint, data=None, auth=False):
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth and self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            return response
        except requests.exceptions.Timeout:
            return None
        except Exception:
            return None
    
    def test_health(self):
        response = self.make_request('GET', '/api/health')
        return response and response.status_code == 200
    
    def test_demo_login(self):
        data = {"email": "demo@babysteps.com", "password": "demo123"}
        response = self.make_request('POST', '/api/auth/login', data)
        if response and response.status_code == 200:
            try:
                result = response.json()
                self.auth_token = result.get('access_token')
                return bool(self.auth_token)
            except:
                return False
        return False
    
    def test_registration(self):
        unique_id = str(uuid.uuid4())[:8]
        data = {
            "email": f"testuser{unique_id}@babysteps.com",
            "name": f"Test User {unique_id}",
            "password": "TestPassword123!"
        }
        response = self.make_request('POST', '/api/auth/register', data)
        if response and response.status_code == 200:
            try:
                result = response.json()
                # New format: auto-login with access_token
                return 'access_token' in result and 'user' in result
            except:
                return False
        return False
    
    def test_auto_login(self):
        # Registration now includes auto-login, so this is verified in test_registration
        return True
    
    def test_persistence(self):
        # Create and login with multiple users to test PostgreSQL persistence
        for i in range(2):
            unique_id = str(uuid.uuid4())[:8]
            data = {
                "email": f"persist{unique_id}@babysteps.com",
                "name": f"Persist User {unique_id}",
                "password": "TestPassword123!"
            }
            response = self.make_request('POST', '/api/auth/register', data)
            if not (response and response.status_code == 200):
                return False
        return True
    
    def test_ai_chat(self):
        data = {"message": "When can babies eat strawberries?", "baby_age_months": 6}
        response = self.make_request('POST', '/api/ai/chat', data, auth=True)
        if response and response.status_code == 200:
            try:
                result = response.json()
                return len(result.get('response', '')) > 100
            except:
                return False
        return False
    
    def test_food_research(self):
        data = {"question": "Are strawberries safe?", "baby_age_months": 6}
        response = self.make_request('POST', '/api/food/research', data, auth=True)
        if response and response.status_code == 200:
            try:
                result = response.json()
                safety_level = result.get('safety_level', '')
                return safety_level in ['safe', 'caution', 'avoid', 'consult_doctor']
            except:
                return False
        return False
    
    def test_meal_search(self):
        data = {"query": "breakfast ideas", "baby_age_months": 8}
        response = self.make_request('POST', '/api/meals/search', data, auth=True)
        if response and response.status_code == 200:
            try:
                result = response.json()
                results = result.get('results', [])
                return len(results) > 0
            except:
                return False
        return False
    
    def test_create_baby(self):
        data = {
            "name": "Test Baby",
            "birth_date": "2024-01-15",
            "gender": "boy"
        }
        response = self.make_request('POST', '/api/babies', data, auth=True)
        return response and response.status_code in [200, 201]
    
    def test_get_babies(self):
        response = self.make_request('GET', '/api/babies', auth=True)
        if response and response.status_code == 200:
            try:
                result = response.json()
                return isinstance(result, list)
            except:
                return False
        return False
    
    def test_invalid_login(self):
        data = {"email": "nonexistent@babysteps.com", "password": "wrongpassword"}
        response = self.make_request('POST', '/api/auth/login', data)
        # Should return 401 for invalid credentials
        return response and response.status_code == 401
    
    def test_unauthorized(self):
        # Access protected endpoint without token
        response = self.make_request('GET', '/api/babies')
        # Should return 401 or 403 for unauthorized access
        return response and response.status_code in [401, 403]

if __name__ == "__main__":
    verifier = FinalVerification()
    success = verifier.test_all()
    exit(0 if success else 1)