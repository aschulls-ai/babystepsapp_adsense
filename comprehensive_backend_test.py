#!/usr/bin/env python3
"""
Comprehensive Backend Testing Suite for Baby Steps App
Tests all major backend functionality as requested in the review
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

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://babytrak-dev.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ComprehensiveBackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 60  # Longer timeout for AI endpoints
        self.auth_token = None
        # Test credentials
        self.test_email = "test@babysteps.com"
        self.test_password = "TestPassword123"
        self.test_name = "Test User"
        self.baby_id = None
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': [],
            'details': []
        }
    
    def log_result(self, test_name, success, message=""):
        """Log test results with details"""
        if success:
            self.results['passed'] += 1
            self.results['details'].append(f"✅ {test_name}: {message}")
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            self.results['details'].append(f"❌ {test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
    
    def test_health_check(self):
        """Test API health endpoint"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_result("Health Check", True, f"API healthy - {data.get('service', 'Baby Steps API')}")
                    return True
            self.log_result("Health Check", False, f"HTTP {response.status_code}")
            return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        try:
            user_data = {
                "email": self.test_email,
                "name": self.test_name,
                "password": self.test_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/register", json=user_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'email' in data:
                    self.log_result("User Registration", True, f"User registered: {data['email']}")
                    return True
            elif response.status_code == 400 and "already registered" in response.text:
                self.log_result("User Registration", True, "User already exists (acceptable)")
                return True
            
            self.log_result("User Registration", False, f"HTTP {response.status_code}: {response.text[:100]}")
            return False
        except Exception as e:
            self.log_result("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login and token generation"""
        try:
            login_data = {
                "email": self.test_email,
                "password": self.test_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and data.get('token_type') == 'bearer':
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("User Login", True, "JWT token generated successfully")
                    return True
            
            self.log_result("User Login", False, f"HTTP {response.status_code}: {response.text[:100]}")
            return False
        except Exception as e:
            self.log_result("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_token_validation(self):
        """Test JWT token validation"""
        try:
            # Test with valid token
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            if response.status_code != 200:
                self.log_result("Token Validation", False, f"Valid token rejected: HTTP {response.status_code}")
                return False
            
            # Test with invalid token
            original_token = self.auth_token
            self.session.headers.update({'Authorization': 'Bearer invalid_token_12345'})
            
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            if response.status_code not in [401, 403]:
                self.log_result("Token Validation", False, f"Invalid token accepted: HTTP {response.status_code}")
                return False
            
            # Restore valid token
            self.session.headers.update({'Authorization': f'Bearer {original_token}'})
            
            self.log_result("Token Validation", True, "JWT validation working correctly")
            return True
        except Exception as e:
            self.log_result("Token Validation", False, f"Error: {str(e)}")
            return False
    
    def test_baby_management_apis(self):
        """Test baby management CRUD operations"""
        try:
            # Test GET /api/babies (list all babies)
            response = self.session.get(f"{API_BASE}/babies", timeout=10)
            if response.status_code != 200:
                self.log_result("Baby Management - List", False, f"GET /babies failed: HTTP {response.status_code}")
                return False
            
            babies = response.json()
            self.log_result("Baby Management - List", True, f"Retrieved {len(babies)} baby profiles")
            
            # Test POST /api/babies (create new baby)
            baby_data = {
                "name": "Test Baby Johnson",
                "birth_date": "2024-03-15T10:30:00Z",
                "birth_weight": 7.5,
                "birth_length": 21.0,
                "gender": "girl"
            }
            
            response = self.session.post(f"{API_BASE}/babies", json=baby_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'id' in data:
                    self.baby_id = data['id']
                    self.log_result("Baby Management - Create", True, f"Baby created: {data['name']}")
                else:
                    self.log_result("Baby Management - Create", False, "No ID in response")
                    return False
            else:
                self.log_result("Baby Management - Create", False, f"POST /babies failed: HTTP {response.status_code}")
                return False
            
            # Test PUT /api/babies/[id] (update baby profile)
            if self.baby_id:
                update_data = {
                    "name": "Updated Test Baby",
                    "birth_date": "2024-03-15T10:30:00Z",
                    "birth_weight": 7.8,
                    "birth_length": 21.5,
                    "gender": "girl"
                }
                
                response = self.session.put(f"{API_BASE}/babies/{self.baby_id}", json=update_data, timeout=10)
                if response.status_code == 200:
                    self.log_result("Baby Management - Update", True, "Baby profile updated successfully")
                else:
                    self.log_result("Baby Management - Update", False, f"PUT /babies/{self.baby_id} failed: HTTP {response.status_code}")
                    return False
            
            return True
        except Exception as e:
            self.log_result("Baby Management APIs", False, f"Error: {str(e)}")
            return False
    
    def test_activity_tracking_apis(self):
        """Test activity tracking APIs"""
        try:
            if not self.baby_id:
                self.log_result("Activity Tracking", False, "No baby ID available for testing")
                return False
            
            # Test POST /api/feedings
            feeding_data = {
                "baby_id": self.baby_id,
                "type": "bottle",
                "amount": 4.0,
                "notes": "Test feeding"
            }
            
            response = self.session.post(f"{API_BASE}/feedings", json=feeding_data, timeout=10)
            if response.status_code == 200:
                self.log_result("Activity Tracking - Feedings", True, "Feeding logged successfully")
            else:
                self.log_result("Activity Tracking - Feedings", False, f"POST /feedings failed: HTTP {response.status_code}")
                return False
            
            # Test POST /api/diapers
            diaper_data = {
                "baby_id": self.baby_id,
                "type": "wet",
                "notes": "Test diaper change"
            }
            
            response = self.session.post(f"{API_BASE}/diapers", json=diaper_data, timeout=10)
            if response.status_code == 200:
                self.log_result("Activity Tracking - Diapers", True, "Diaper change logged successfully")
            else:
                self.log_result("Activity Tracking - Diapers", False, f"POST /diapers failed: HTTP {response.status_code}")
                return False
            
            # Test POST /api/sleep
            sleep_data = {
                "baby_id": self.baby_id,
                "start_time": "2024-10-08T14:00:00Z",
                "end_time": "2024-10-08T16:00:00Z",
                "quality": "good"
            }
            
            response = self.session.post(f"{API_BASE}/sleep", json=sleep_data, timeout=10)
            if response.status_code == 200:
                self.log_result("Activity Tracking - Sleep", True, "Sleep session logged successfully")
            else:
                self.log_result("Activity Tracking - Sleep", False, f"POST /sleep failed: HTTP {response.status_code}")
                return False
            
            # Test POST /api/pumping
            pumping_data = {
                "baby_id": self.baby_id,
                "amount": 3.5,
                "duration": 20,
                "notes": "Test pumping session"
            }
            
            response = self.session.post(f"{API_BASE}/pumping", json=pumping_data, timeout=10)
            if response.status_code == 200:
                self.log_result("Activity Tracking - Pumping", True, "Pumping session logged successfully")
            else:
                self.log_result("Activity Tracking - Pumping", False, f"POST /pumping failed: HTTP {response.status_code}")
                return False
            
            return True
        except Exception as e:
            self.log_result("Activity Tracking APIs", False, f"Error: {str(e)}")
            return False
    
    def test_ai_powered_features(self):
        """Test AI-powered features"""
        try:
            # Test POST /api/research (general parenting research)
            research_query = {
                "question": "How often should I feed my 6 month old baby?"
            }
            
            response = self.session.post(f"{API_BASE}/research", json=research_query, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if 'answer' in data and len(data['answer']) > 10:
                    self.log_result("AI Research", True, "Research query answered successfully")
                else:
                    self.log_result("AI Research", False, "Empty or invalid research response")
                    return False
            else:
                self.log_result("AI Research", False, f"POST /research failed: HTTP {response.status_code}")
                return False
            
            # Test POST /api/meals/search (meal planner with recipes)
            meal_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=meal_query, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 10:
                    self.log_result("AI Meal Search", True, "Meal search returned comprehensive results")
                else:
                    self.log_result("AI Meal Search", False, "Empty or invalid meal search response")
                    return False
            else:
                self.log_result("AI Meal Search", False, f"POST /meals/search failed: HTTP {response.status_code}")
                return False
            
            # Test POST /api/food/research (food safety research)
            food_query = {
                "question": "Is honey safe for my 10 month old baby?",
                "baby_age_months": 10
            }
            
            response = self.session.post(f"{API_BASE}/food/research", json=food_query, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if 'answer' in data and 'safety_level' in data:
                    self.log_result("AI Food Safety", True, f"Food safety assessment: {data['safety_level']}")
                else:
                    self.log_result("AI Food Safety", False, "Invalid food safety response format")
                    return False
            else:
                self.log_result("AI Food Safety", False, f"POST /food/research failed: HTTP {response.status_code}")
                return False
            
            return True
        except Exception as e:
            self.log_result("AI-Powered Features", False, f"Error: {str(e)}")
            return False
    
    def test_reminders_system(self):
        """Test reminders system"""
        try:
            if not self.baby_id:
                self.log_result("Reminders System", False, "No baby ID available for testing")
                return False
            
            # Test POST /api/reminders (create reminders)
            reminder_data = {
                "baby_id": self.baby_id,
                "title": "Test Feeding Reminder",
                "description": "Time for next feeding",
                "reminder_type": "feeding",
                "next_due": "2024-10-08T18:00:00Z",
                "interval_hours": 3
            }
            
            response = self.session.post(f"{API_BASE}/reminders", json=reminder_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                reminder_id = data.get('id')
                self.log_result("Reminders - Create", True, "Reminder created successfully")
                
                # Test PUT /api/reminders/[id] (update reminders)
                if reminder_id:
                    update_data = {"title": "Updated Feeding Reminder"}
                    response = self.session.patch(f"{API_BASE}/reminders/{reminder_id}", json=update_data, timeout=10)
                    if response.status_code == 200:
                        self.log_result("Reminders - Update", True, "Reminder updated successfully")
                    else:
                        self.log_result("Reminders - Update", False, f"PATCH /reminders/{reminder_id} failed: HTTP {response.status_code}")
                        return False
                    
                    # Test DELETE /api/reminders/[id] (delete reminders)
                    response = self.session.delete(f"{API_BASE}/reminders/{reminder_id}", timeout=10)
                    if response.status_code == 200:
                        self.log_result("Reminders - Delete", True, "Reminder deleted successfully")
                    else:
                        self.log_result("Reminders - Delete", False, f"DELETE /reminders/{reminder_id} failed: HTTP {response.status_code}")
                        return False
                
                return True
            else:
                self.log_result("Reminders - Create", False, f"POST /reminders failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Reminders System", False, f"Error: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling and data validation"""
        try:
            # Test malformed JSON requests
            response = self.session.post(f"{API_BASE}/babies", data="invalid json", timeout=10)
            if response.status_code in [400, 422]:
                self.log_result("Error Handling - Malformed JSON", True, f"Properly rejected malformed JSON: HTTP {response.status_code}")
            else:
                self.log_result("Error Handling - Malformed JSON", False, f"Malformed JSON not properly handled: HTTP {response.status_code}")
                return False
            
            # Test missing required fields
            incomplete_data = {"name": "Test Baby"}  # Missing birth_date
            response = self.session.post(f"{API_BASE}/babies", json=incomplete_data, timeout=10)
            if response.status_code in [400, 422]:
                self.log_result("Error Handling - Missing Fields", True, f"Properly rejected incomplete data: HTTP {response.status_code}")
            else:
                self.log_result("Error Handling - Missing Fields", False, f"Missing fields not properly validated: HTTP {response.status_code}")
                return False
            
            # Test invalid data types
            invalid_data = {
                "name": "Test Baby",
                "birth_date": "invalid-date-format",
                "birth_weight": "not-a-number"
            }
            response = self.session.post(f"{API_BASE}/babies", json=invalid_data, timeout=10)
            if response.status_code in [400, 422]:
                self.log_result("Error Handling - Invalid Types", True, f"Properly rejected invalid data types: HTTP {response.status_code}")
            else:
                self.log_result("Error Handling - Invalid Types", False, f"Invalid data types not properly validated: HTTP {response.status_code}")
                return False
            
            return True
        except Exception as e:
            self.log_result("Error Handling", False, f"Error: {str(e)}")
            return False
    
    def test_remember_me_functionality(self):
        """Test Remember Me functionality"""
        try:
            # Test login without Remember Me
            login_data = {
                "email": self.test_email,
                "password": self.test_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.log_result("Remember Me - Normal Login", True, "Normal login working")
                    return True
            
            self.log_result("Remember Me - Normal Login", False, f"Login failed: HTTP {response.status_code}")
            return False
        except Exception as e:
            self.log_result("Remember Me Functionality", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all comprehensive backend tests"""
        print("🚀 COMPREHENSIVE BABY STEPS BACKEND TESTING")
        print(f"📍 Testing against: {API_BASE}")
        print("=" * 80)
        
        # 1. AUTHENTICATION ENDPOINTS
        print("\n🔐 1. AUTHENTICATION ENDPOINTS:")
        print("=" * 50)
        
        if not self.test_health_check():
            print("❌ Health check failed - backend may be down")
            return self.results
        
        self.test_user_registration()
        if not self.test_user_login():
            print("❌ Login failed - cannot proceed with authenticated tests")
            return self.results
        
        self.test_token_validation()
        self.test_remember_me_functionality()
        
        # 2. BABY MANAGEMENT APIs
        print("\n👶 2. BABY MANAGEMENT APIs:")
        print("=" * 50)
        self.test_baby_management_apis()
        
        # 3. ACTIVITY TRACKING APIs
        print("\n📊 3. ACTIVITY TRACKING APIs:")
        print("=" * 50)
        self.test_activity_tracking_apis()
        
        # 4. AI-POWERED FEATURES
        print("\n🤖 4. AI-POWERED FEATURES:")
        print("=" * 50)
        self.test_ai_powered_features()
        
        # 5. REMINDERS SYSTEM
        print("\n⏰ 5. REMINDERS SYSTEM:")
        print("=" * 50)
        self.test_reminders_system()
        
        # 6. ERROR HANDLING
        print("\n🛡️ 6. ERROR HANDLING:")
        print("=" * 50)
        self.test_error_handling()
        
        # Print final results
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        return self.results

def main():
    """Main test execution"""
    tester = ComprehensiveBackendTester()
    results = tester.run_comprehensive_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()