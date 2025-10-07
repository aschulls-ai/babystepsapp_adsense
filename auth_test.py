#!/usr/bin/env python3
"""
Authentication System Test for Baby Steps - Focused on login issues
Tests the complete authentication flow as requested in the review
"""

import requests
import json
import uuid
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://parent-helper-21.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class AuthenticationTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.auth_token = None
        # Use test credentials from review request
        self.test_user_email = "test@babysteps.com"
        self.test_user_password = "TestPassword123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def log_result(self, test_name, success, message=""):
        """Log test results"""
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
    
    def test_backend_service_status(self):
        """Test if backend service is running and responding"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_result("Backend Service Status", True, f"Service: {data.get('service', 'Unknown')}")
                    return True
                else:
                    self.log_result("Backend Service Status", False, f"Unhealthy status: {data}")
                    return False
            else:
                self.log_result("Backend Service Status", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Backend Service Status", False, f"Connection error: {str(e)}")
            return False
    
    def test_health_endpoint(self):
        """Test /api/health endpoint specifically"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=30)
            if response.status_code == 200:
                data = response.json()
                required_fields = ['status', 'service', 'timestamp']
                if all(field in data for field in required_fields):
                    self.log_result("Health Endpoint", True, f"All required fields present")
                    return True
                else:
                    self.log_result("Health Endpoint", False, f"Missing fields in response: {data}")
                    return False
            else:
                self.log_result("Health Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Health Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_user_registration_or_exists(self):
        """Test user registration or verify user exists"""
        try:
            # First try to register the user
            user_data = {
                "email": self.test_user_email,
                "name": "Test User",
                "password": self.test_user_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/register", json=user_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.log_result("User Registration", True, f"New user registered: {data.get('message', '')}")
                return True
            elif response.status_code == 400:
                error_data = response.json()
                if "Email already registered" in error_data.get('detail', ''):
                    self.log_result("User Registration", True, "User already exists (expected for test user)")
                    return True
                else:
                    self.log_result("User Registration", False, f"Registration error: {error_data}")
                    return False
            else:
                self.log_result("User Registration", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_manual_verification(self):
        """Manually verify user for testing purposes"""
        try:
            verify_data = {
                "email": self.test_user_email
            }
            
            response = self.session.post(f"{API_BASE}/auth/manual-verify", json=verify_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.log_result("Manual User Verification", True, "User verified for testing")
                return True
            else:
                self.log_result("Manual User Verification", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Manual User Verification", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login endpoint - main focus of review request"""
        try:
            login_data = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("User Login", True, "Login successful, JWT token received")
                    return True
                else:
                    self.log_result("User Login", False, f"Invalid response format: {data}")
                    return False
            elif response.status_code == 401:
                error_data = response.json()
                if "verify your email" in error_data.get('detail', '').lower():
                    self.log_result("User Login", False, f"Email verification required: {error_data['detail']}")
                    return False
                else:
                    self.log_result("User Login", False, f"Authentication failed: {error_data['detail']}")
                    return False
            else:
                self.log_result("User Login", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_jwt_token_validation(self):
        """Test JWT token validation by making authenticated request"""
        if not self.auth_token:
            self.log_result("JWT Token Validation", False, "No token available to test")
            return False
        
        try:
            # Test token by accessing a protected endpoint
            response = self.session.get(f"{API_BASE}/babies", timeout=30)
            
            if response.status_code == 200:
                self.log_result("JWT Token Validation", True, "Token is valid and accepted")
                return True
            elif response.status_code == 401:
                self.log_result("JWT Token Validation", False, "Token rejected by server")
                return False
            else:
                self.log_result("JWT Token Validation", False, f"Unexpected response: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("JWT Token Validation", False, f"Error: {str(e)}")
            return False
    
    def test_protected_babies_endpoint(self):
        """Test /api/babies endpoint with authentication"""
        if not self.auth_token:
            self.log_result("Protected Babies Endpoint", False, "No authentication token available")
            return False
        
        try:
            response = self.session.get(f"{API_BASE}/babies", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Protected Babies Endpoint", True, f"Retrieved {len(data)} baby profiles")
                    return True
                else:
                    self.log_result("Protected Babies Endpoint", False, f"Invalid response format: {data}")
                    return False
            elif response.status_code == 401:
                self.log_result("Protected Babies Endpoint", False, "Authentication failed")
                return False
            else:
                self.log_result("Protected Babies Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Protected Babies Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_authentication_without_token(self):
        """Test that protected endpoints require authentication"""
        try:
            # Create a new session without auth token
            test_session = requests.Session()
            test_session.timeout = 30
            
            response = test_session.get(f"{API_BASE}/babies", timeout=30)
            
            if response.status_code == 401:
                self.log_result("Authentication Required", True, "Protected endpoints properly require authentication")
                return True
            else:
                self.log_result("Authentication Required", False, f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Authentication Required", False, f"Error: {str(e)}")
            return False
    
    def run_authentication_tests(self):
        """Run all authentication-focused tests"""
        print(f"🔐 Baby Steps Authentication System Test")
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Test user: {self.test_user_email}")
        print("=" * 60)
        
        # 1. Backend Service Status
        if not self.test_backend_service_status():
            print("❌ Backend service not responding - stopping tests")
            return self.results
        
        # 2. Health Check
        self.test_health_endpoint()
        
        # 3. User Registration (or verify exists)
        user_ready = self.test_user_registration_or_exists()
        
        # 4. Manual verification for testing
        if user_ready:
            verification_success = self.test_manual_verification()
            
            # 5. User Login - MAIN FOCUS
            if verification_success:
                login_success = self.test_user_login()
                
                if login_success:
                    # 6. JWT Token Validation
                    self.test_jwt_token_validation()
                    
                    # 7. Protected Endpoints
                    self.test_protected_babies_endpoint()
                else:
                    print("⚠️  Login failed - this is the main issue to investigate")
            else:
                print("⚠️  Manual verification failed - trying login anyway")
                self.test_user_login()
        
        # 8. Test authentication requirement
        self.test_authentication_without_token()
        
        print("=" * 60)
        print(f"📊 Authentication Test Results:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests Details:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Provide diagnosis
        print(f"\n🔍 Authentication System Diagnosis:")
        if self.results['failed'] == 0:
            print("✅ Authentication system is working correctly")
        else:
            print("❌ Issues found in authentication system:")
            if any("Login" in error for error in self.results['errors']):
                print("   - Login functionality has issues")
            if any("Token" in error for error in self.results['errors']):
                print("   - JWT token validation has issues")
            if any("Protected" in error for error in self.results['errors']):
                print("   - Protected endpoint access has issues")
        
        return self.results

def main():
    """Main test execution"""
    tester = AuthenticationTester()
    results = tester.run_authentication_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()