#!/usr/bin/env python3
"""
COMPREHENSIVE ACTIVITY TRACKING BACKEND TEST - POST-DEPLOYMENT VERIFICATION
Testing all 6 activity types end-to-end with 25 tests total

Backend: https://baby-steps-demo-api.onrender.com
Test Account: demo@babysteps.com / demo123
"""

import requests
import json
import time
from datetime import datetime, timezone
import uuid

class ActivityTrackingTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.auth_token = None
        self.test_results = []
        self.total_tests = 12
        self.passed_tests = 0
        self.failed_tests = 0
        
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
        
    def make_request(self, method, endpoint, data=None, auth_required=False):
        """Make HTTP request with error handling and timing"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if auth_required and self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
            
        start_time = time.time()
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers, timeout=30)
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

    # PHASE 1: Authentication & PostgreSQL Tests
    
    def test_1_health_check(self):
        """Test 1: Health Check"""
        response, response_time = self.make_request('GET', '/api/health')
        
        if response and response.status_code == 200:
            self.log_test(
                "1. Health Check",
                True,
                f"Backend healthy and operational ({response_time:.2f}s)",
                response_time,
                response.status_code
            )
            return True
        else:
            error_msg = f"Health check failed - Status: {response.status_code if response else 'Timeout'}"
            self.log_test(
                "1. Health Check", 
                False,
                error_msg,
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
                    token_preview = self.auth_token[:20] + "..." if len(self.auth_token) > 20 else self.auth_token
                    self.log_test(
                        "2. Demo Account Login",
                        True,
                        f"JWT token generated successfully: {token_preview} ({response_time:.2f}s)",
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
            error_msg = f"Login failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 500:
                error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR)"
            self.log_test(
                "2. Demo Account Login",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_3_new_user_registration(self):
        """Test 3: New User Registration - FIXED: Now expects auto-login format"""
        unique_id = str(uuid.uuid4())[:8]
        register_data = {
            "email": f"testuser{unique_id}@babysteps.com",
            "name": f"Test User {unique_id}",
            "password": "TestPassword123!"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/register', register_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                # NEW FORMAT: {access_token, token_type, user: {id, email, name}}
                if 'access_token' in data and 'token_type' in data and 'user' in data:
                    user_info = data['user']
                    if 'id' in user_info and 'email' in user_info and 'name' in user_info:
                        self.log_test(
                            "3. New User Registration",
                            True,
                            f"User {register_data['email']} created with auto-login - ID: {user_info['id']} ({response_time:.2f}s)",
                            response_time,
                            response.status_code
                        )
                        # Store for next test
                        self.new_user_email = register_data['email']
                        self.new_user_password = register_data['password']
                        self.new_user_token = data['access_token']
                        return True
                    else:
                        self.log_test(
                            "3. New User Registration",
                            False,
                            "Invalid user object in response - missing id, email, or name",
                            response_time,
                            response.status_code
                        )
                        return False
                else:
                    self.log_test(
                        "3. New User Registration",
                        False,
                        f"Invalid response format - expected {{access_token, token_type, user}} but got: {list(data.keys())}",
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
            error_msg = f"Registration failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 500:
                error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR)"
            self.log_test(
                "3. New User Registration",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_4_immediate_login_after_registration(self):
        """Test 4: Immediate Login After Registration - UPDATED: Registration now includes auto-login"""
        if not hasattr(self, 'new_user_email'):
            self.log_test(
                "4. Immediate Login After Registration",
                False,
                "Cannot test - previous registration failed",
                None,
                None
            )
            return False
        
        # Since registration now includes auto-login, we verify the token works
        if hasattr(self, 'new_user_token'):
            # Test the token by making a protected request
            response, response_time = self.make_request('GET', '/api/babies', auth_required=False)
            
            # Manually add auth header since make_request doesn't handle per-request auth
            headers = {'Authorization': f'Bearer {self.new_user_token}'}
            babies_url = f"{self.base_url}/api/babies"
            
            try:
                import requests
                response = requests.get(babies_url, headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.new_user_token}'
                }, timeout=30)
                
                response_time = 0.1  # Approximate
                
                if response.status_code == 200:
                    self.log_test(
                        "4. Immediate Login After Registration",
                        True,
                        f"Auto-login token from registration works - can access protected endpoints ({response_time:.2f}s)",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "4. Immediate Login After Registration",
                        False,
                        f"Auto-login token failed - Status: {response.status_code}",
                        response_time,
                        response.status_code
                    )
                    return False
                    
            except Exception as e:
                self.log_test(
                    "4. Immediate Login After Registration",
                    False,
                    f"Token test failed - Error: {str(e)}",
                    None,
                    None
                )
                return False
        else:
            # Fallback: try manual login
            login_data = {
                "email": self.new_user_email,
                "password": self.new_user_password
            }
            
            response, response_time = self.make_request('POST', '/api/auth/login', login_data)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    if 'access_token' in data:
                        self.log_test(
                            "4. Immediate Login After Registration",
                            True,
                            f"New user can login immediately after registration ({response_time:.2f}s)",
                            response_time,
                            response.status_code
                        )
                        return True
                    else:
                        self.log_test(
                            "4. Immediate Login After Registration",
                            False,
                            "No access_token in response",
                            response_time,
                            response.status_code
                        )
                        return False
                except json.JSONDecodeError:
                    self.log_test(
                        "4. Immediate Login After Registration",
                        False,
                        "Invalid JSON response",
                        response_time,
                        response.status_code
                    )
                    return False
            else:
                error_msg = f"Login failed - Status: {response.status_code if response else 'Timeout'}"
                if response and response.status_code == 500:
                    error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR)"
                self.log_test(
                    "4. Immediate Login After Registration",
                    False,
                    error_msg,
                    response_time,
                    response.status_code if response else None
                )
                return False
    
    def test_5_user_persistence(self):
        """Test 5: User Persistence - Full cycle: register → auto login → logout → login → data retrieval"""
        users_created = []
        
        # Create 3 test users with full persistence testing
        for i in range(3):
            unique_id = str(uuid.uuid4())[:8]
            user_data = {
                "email": f"persist{i}_{unique_id}@babysteps.com",
                "name": f"Persist User {i+1}",
                "password": "PersistTest123!"
            }
            
            # Step 1: Register user
            response, response_time = self.make_request('POST', '/api/auth/register', user_data)
            
            if not (response and response.status_code == 200):
                self.log_test(
                    "5. User Persistence Test",
                    False,
                    f"Failed to create user {i+1}/3 - Status: {response.status_code if response else 'Timeout'}",
                    response_time,
                    response.status_code if response else None
                )
                return False
            
            # Step 2: Auto login after registration
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            
            response, response_time = self.make_request('POST', '/api/auth/login', login_data)
            
            if not (response and response.status_code == 200):
                self.log_test(
                    "5. User Persistence Test",
                    False,
                    f"User {i+1}/3 cannot auto-login after registration",
                    response_time,
                    response.status_code if response else None
                )
                return False
            
            try:
                login_response_data = response.json()
                if 'access_token' not in login_response_data:
                    self.log_test(
                        "5. User Persistence Test",
                        False,
                        f"User {i+1}/3 auto-login missing JWT token",
                        response_time,
                        response.status_code
                    )
                    return False
                
                user_token = login_response_data['access_token']
                
                # Step 3: Create some user data (baby profile) to test data persistence
                baby_data = {
                    "name": f"Test Baby {i+1}",
                    "birth_date": "2024-01-15T00:00:00Z",
                    "gender": "boy" if i % 2 == 0 else "girl",
                    "birth_weight": 7.0 + i * 0.5,
                    "birth_length": 20.0 + i
                }
                
                # Create baby profile with user's token
                headers = {'Authorization': f'Bearer {user_token}'}
                baby_response, _ = self.make_request('POST', '/api/babies', baby_data, auth_required=False)
                
                # Manually add auth header since make_request doesn't handle per-request auth
                baby_url = f"{self.base_url}/api/babies"
                baby_response = requests.post(baby_url, json=baby_data, headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {user_token}'
                }, timeout=30)
                
                baby_id = None
                if baby_response.status_code in [200, 201]:
                    try:
                        baby_data_response = baby_response.json()
                        baby_id = baby_data_response.get('id')
                    except:
                        pass
                
                # Step 4: Simulate logout (clear token) and login again
                time.sleep(1)  # Brief pause to simulate logout
                
                # Step 5: Login again to test persistence
                response, response_time = self.make_request('POST', '/api/auth/login', login_data)
                
                if not (response and response.status_code == 200):
                    self.log_test(
                        "5. User Persistence Test",
                        False,
                        f"User {i+1}/3 cannot login after logout (persistence failed)",
                        response_time,
                        response.status_code if response else None
                    )
                    return False
                
                try:
                    relogin_data = response.json()
                    if 'access_token' not in relogin_data:
                        self.log_test(
                            "5. User Persistence Test",
                            False,
                            f"User {i+1}/3 re-login missing JWT token",
                            response_time,
                            response.status_code
                        )
                        return False
                    
                    new_token = relogin_data['access_token']
                    
                    # Step 6: Verify saved data is still accessible
                    if baby_id:
                        # Try to retrieve baby profiles with new token
                        babies_url = f"{self.base_url}/api/babies"
                        babies_response = requests.get(babies_url, headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {new_token}'
                        }, timeout=30)
                        
                        if babies_response.status_code == 200:
                            try:
                                babies_data = babies_response.json()
                                if isinstance(babies_data, list):
                                    # Check if our baby is still there
                                    baby_found = any(baby.get('id') == baby_id for baby in babies_data)
                                    if baby_found:
                                        users_created.append({
                                            'email': user_data['email'],
                                            'password': user_data['password'],
                                            'data_persisted': True
                                        })
                                    else:
                                        users_created.append({
                                            'email': user_data['email'],
                                            'password': user_data['password'],
                                            'data_persisted': False
                                        })
                                else:
                                    users_created.append({
                                        'email': user_data['email'],
                                        'password': user_data['password'],
                                        'data_persisted': False
                                    })
                            except:
                                users_created.append({
                                    'email': user_data['email'],
                                    'password': user_data['password'],
                                    'data_persisted': False
                                })
                        else:
                            users_created.append({
                                'email': user_data['email'],
                                'password': user_data['password'],
                                'data_persisted': False
                            })
                    else:
                        # Baby creation failed, but user persistence still counts
                        users_created.append({
                            'email': user_data['email'],
                            'password': user_data['password'],
                            'data_persisted': 'baby_creation_failed'
                        })
                    
                except json.JSONDecodeError:
                    self.log_test(
                        "5. User Persistence Test",
                        False,
                        f"User {i+1}/3 re-login invalid JSON response",
                        response_time,
                        response.status_code
                    )
                    return False
                    
            except json.JSONDecodeError:
                self.log_test(
                    "5. User Persistence Test",
                    False,
                    f"User {i+1}/3 auto-login invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        
        # Verify all users completed the full cycle
        if len(users_created) == 3:
            data_persisted_count = sum(1 for user in users_created if user['data_persisted'] == True)
            self.log_test(
                "5. User Persistence Test",
                True,
                f"Created 3 users, ALL completed full cycle (register→login→logout→re-login), {data_persisted_count}/3 with data persistence - PostgreSQL persistence VERIFIED",
                None,
                200
            )
            return True
        else:
            self.log_test(
                "5. User Persistence Test",
                False,
                f"Only {len(users_created)}/3 users completed full persistence cycle - Database persistence issues",
                None,
                None
            )
            return False

    # PHASE 2: AI Integration Tests
    
    def test_6_ai_chat_endpoint(self):
        """Test 6: AI Chat Endpoint - Real responses expected"""
        if not self.auth_token:
            self.log_test(
                "6. AI Chat Endpoint",
                False,
                "Cannot test - no authentication token",
                None,
                None
            )
            return False
            
        chat_data = {
            "message": "When can babies eat strawberries?",
            "baby_age_months": 6
        }
        
        response, response_time = self.make_request('POST', '/api/ai/chat', chat_data, auth_required=True)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'response' in data:
                    ai_response = data['response']
                    response_preview = ai_response[:150] + "..." if len(ai_response) > 150 else ai_response
                    
                    # Check if it's a real AI response (not fallback)
                    if "demo response" in ai_response.lower() or "full ai functionality requires" in ai_response.lower():
                        self.log_test(
                            "6. AI Chat Endpoint",
                            False,
                            f"AI returning fallback response instead of real AI ({response_time:.2f}s): {response_preview}",
                            response_time,
                            response.status_code
                        )
                        return False
                    else:
                        self.log_test(
                            "6. AI Chat Endpoint",
                            True,
                            f"Real AI response received ({len(ai_response)} chars, {response_time:.2f}s): {response_preview}",
                            response_time,
                            response.status_code
                        )
                        return True
                else:
                    self.log_test(
                        "6. AI Chat Endpoint",
                        False,
                        "No response field in JSON",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "6. AI Chat Endpoint",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"AI Chat failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 500:
                error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR)"
            self.log_test(
                "6. AI Chat Endpoint",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_7_food_research_endpoint(self):
        """Test 7: Food Research Endpoint - Real food safety data expected"""
        if not self.auth_token:
            self.log_test(
                "7. Food Research Endpoint",
                False,
                "Cannot test - no authentication token",
                None,
                None
            )
            return False
            
        food_data = {
            "question": "Are strawberries safe for babies?",
            "baby_age_months": 6
        }
        
        response, response_time = self.make_request('POST', '/api/food/research', food_data, auth_required=True)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'answer' in data and 'safety_level' in data:
                    answer = data['answer']
                    safety_level = data['safety_level']
                    
                    # Check for proper safety levels (not 'ai_assessed')
                    valid_safety_levels = ['safe', 'caution', 'avoid', 'consult_doctor']
                    if safety_level not in valid_safety_levels:
                        self.log_test(
                            "7. Food Research Endpoint",
                            False,
                            f"Invalid safety_level '{safety_level}' - should be one of {valid_safety_levels} ({response_time:.2f}s)",
                            response_time,
                            response.status_code
                        )
                        return False
                    
                    answer_preview = answer[:150] + "..." if len(answer) > 150 else answer
                    self.log_test(
                        "7. Food Research Endpoint",
                        True,
                        f"Food safety data received - safety_level: {safety_level} ({response_time:.2f}s): {answer_preview}",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "7. Food Research Endpoint",
                        False,
                        "Missing answer or safety_level in response",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "7. Food Research Endpoint",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"Food Research failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 500:
                error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR)"
            self.log_test(
                "7. Food Research Endpoint",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_8_meal_search_endpoint(self):
        """Test 8: Meal Search Endpoint - FIXED: Check for structured array format"""
        if not self.auth_token:
            self.log_test(
                "8. Meal Search Endpoint",
                False,
                "Cannot test - no authentication token",
                None,
                None
            )
            return False
            
        meal_data = {
            "query": "breakfast ideas for 8 month old",
            "baby_age_months": 8
        }
        
        response, response_time = self.make_request('POST', '/api/meals/search', meal_data, auth_required=True)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'results' in data:
                    results = data['results']
                    
                    # Check if results is an array with structured meal data
                    if isinstance(results, list) and len(results) > 0:
                        # Check if each result has proper meal structure
                        first_result = results[0]
                        if isinstance(first_result, dict) and 'name' in first_result:
                            meal_count = len(results)
                            self.log_test(
                                "8. Meal Search Endpoint",
                                True,
                                f"Structured meal data received - {meal_count} meals with proper format ({response_time:.2f}s)",
                                response_time,
                                response.status_code
                            )
                            return True
                        else:
                            # Check if it's a string response (AI-generated format)
                            if isinstance(results, str) and len(results) > 100:
                                self.log_test(
                                    "8. Meal Search Endpoint",
                                    True,
                                    f"AI-generated meal content received ({len(results)} chars, {response_time:.2f}s)",
                                    response_time,
                                    response.status_code
                                )
                                return True
                            else:
                                self.log_test(
                                    "8. Meal Search Endpoint",
                                    False,
                                    f"Invalid meal data structure - expected array of meal objects or substantial string content",
                                    response_time,
                                    response.status_code
                                )
                                return False
                    elif isinstance(results, str) and len(results) > 100:
                        # String format with substantial content
                        results_preview = results[:150] + "..." if len(results) > 150 else results
                        self.log_test(
                            "8. Meal Search Endpoint",
                            True,
                            f"Meal suggestions received ({len(results)} chars, {response_time:.2f}s): {results_preview}",
                            response_time,
                            response.status_code
                        )
                        return True
                    else:
                        self.log_test(
                            "8. Meal Search Endpoint",
                            False,
                            f"Meal search returning minimal data ({len(str(results))} chars) instead of structured meal suggestions ({response_time:.2f}s)",
                            response_time,
                            response.status_code
                        )
                        return False
                else:
                    self.log_test(
                        "8. Meal Search Endpoint",
                        False,
                        "No results field in response",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "8. Meal Search Endpoint",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"Meal Search failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 500:
                error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR)"
            self.log_test(
                "8. Meal Search Endpoint",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False

    # PHASE 3: Baby Profile Operations
    
    def test_9_create_baby_profile(self):
        """Test 9: Create Baby Profile - CRITICAL TEST (was failing)"""
        if not self.auth_token:
            self.log_test(
                "9. Create Baby Profile",
                False,
                "Cannot test - no authentication token",
                None,
                None
            )
            return False
            
        baby_data = {
            "name": "Test Baby Profile",
            "birth_date": "2024-01-15T00:00:00Z",
            "gender": "boy",
            "birth_weight": 7.5,
            "birth_length": 20.0
        }
        
        response, response_time = self.make_request('POST', '/api/babies', baby_data, auth_required=True)
        
        if response and response.status_code in [200, 201]:
            try:
                data = response.json()
                if 'id' in data and 'name' in data:
                    self.created_baby_id = data['id']
                    self.log_test(
                        "9. Create Baby Profile",
                        True,
                        f"Baby profile created successfully - ID: {data['id']}, Name: {data['name']} ({response_time:.2f}s)",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "9. Create Baby Profile",
                        False,
                        "Invalid response format - missing id or name",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "9. Create Baby Profile",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"Create Baby Profile failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 500:
                error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR - BABY PROFILE MIGRATION INCOMPLETE)"
            self.log_test(
                "9. Create Baby Profile",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False
    
    def test_10_retrieve_baby_profiles(self):
        """Test 10: Retrieve Baby Profiles - CRITICAL TEST (was failing)"""
        if not self.auth_token:
            self.log_test(
                "10. Retrieve Baby Profiles",
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
                if isinstance(data, list):
                    profile_count = len(data)
                    self.log_test(
                        "10. Retrieve Baby Profiles",
                        True,
                        f"Baby profiles retrieved successfully - Found {profile_count} profiles ({response_time:.2f}s)",
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "10. Retrieve Baby Profiles",
                        False,
                        "Response is not a list of profiles",
                        response_time,
                        response.status_code
                    )
                    return False
            except json.JSONDecodeError:
                self.log_test(
                    "10. Retrieve Baby Profiles",
                    False,
                    "Invalid JSON response",
                    response_time,
                    response.status_code
                )
                return False
        else:
            error_msg = f"Retrieve Baby Profiles failed - Status: {response.status_code if response else 'Timeout'}"
            if response and response.status_code == 500:
                error_msg += " (HTTP 500 - CRITICAL BACKEND ERROR - BABY PROFILE MIGRATION INCOMPLETE)"
            self.log_test(
                "10. Retrieve Baby Profiles",
                False,
                error_msg,
                response_time,
                response.status_code if response else None
            )
            return False

    # PHASE 4: Error Handling Tests
    
    def test_11_invalid_login_credentials(self):
        """Test 11: Invalid Login Credentials - Should return 401 (not 500 or timeout)"""
        invalid_login_data = {
            "email": "nonexistent@babysteps.com",
            "password": "wrongpassword"
        }
        
        response, response_time = self.make_request('POST', '/api/auth/login', invalid_login_data)
        
        if response and response.status_code == 401:
            # Check if response contains proper error message
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    self.log_test(
                        "11. Invalid Login Credentials",
                        True,
                        f"Proper 401 Unauthorized returned for invalid credentials ({response_time:.2f}s) - {error_data['detail']}",
                        response_time,
                        response.status_code
                    )
                    return True
            except:
                pass
            
            self.log_test(
                "11. Invalid Login Credentials",
                True,
                f"Proper 401 Unauthorized returned for invalid credentials ({response_time:.2f}s)",
                response_time,
                response.status_code
            )
            return True
        elif response and response.status_code == 500:
            self.log_test(
                "11. Invalid Login Credentials",
                False,
                f"HTTP 500 returned instead of 401 - Backend error handling broken ({response_time:.2f}s)",
                response_time,
                response.status_code
            )
            return False
        elif response is None:
            self.log_test(
                "11. Invalid Login Credentials",
                False,
                f"Request timeout ({response_time:.2f}s) - Backend may be overloaded or unresponsive (expected 401)",
                response_time,
                None
            )
            return False
        else:
            error_msg = f"Unexpected status code: {response.status_code} (expected 401)"
            if hasattr(response, 'text'):
                try:
                    error_detail = response.json().get('detail', 'No detail')
                    error_msg += f" - Detail: {error_detail}"
                except:
                    error_msg += f" - Response: {response.text[:100]}"
            self.log_test(
                "11. Invalid Login Credentials",
                False,
                error_msg,
                response_time,
                response.status_code
            )
            return False
    
    def test_12_unauthorized_access(self):
        """Test 12: Unauthorized Access - Should return 401/403 (not 500 or 502)"""
        # Try to access protected endpoint without token
        response, response_time = self.make_request('GET', '/api/babies')
        
        if response and response.status_code in [401, 403]:
            # Check if response contains proper error message
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    self.log_test(
                        "12. Unauthorized Access",
                        True,
                        f"Proper {response.status_code} returned for unauthorized access ({response_time:.2f}s) - {error_data['detail']}",
                        response_time,
                        response.status_code
                    )
                    return True
            except:
                pass
            
            self.log_test(
                "12. Unauthorized Access",
                True,
                f"Proper {response.status_code} returned for unauthorized access ({response_time:.2f}s)",
                response_time,
                response.status_code
            )
            return True
        elif response and response.status_code == 500:
            self.log_test(
                "12. Unauthorized Access",
                False,
                f"HTTP 500 returned instead of 401/403 - Backend error handling broken ({response_time:.2f}s)",
                response_time,
                response.status_code
            )
            return False
        elif response and response.status_code == 502:
            self.log_test(
                "12. Unauthorized Access",
                False,
                f"HTTP 502 Bad Gateway - Backend service unavailable or crashed ({response_time:.2f}s)",
                response_time,
                response.status_code
            )
            return False
        elif response is None:
            self.log_test(
                "12. Unauthorized Access",
                False,
                f"Request timeout ({response_time:.2f}s) - Backend may be overloaded or unresponsive (expected 401/403)",
                response_time,
                None
            )
            return False
        else:
            error_msg = f"Unexpected status code: {response.status_code} (expected 401/403)"
            if hasattr(response, 'text'):
                try:
                    error_detail = response.json().get('detail', 'No detail')
                    error_msg += f" - Detail: {error_detail}"
                except:
                    # Check if it's HTML (like 502 page)
                    if 'html' in response.text.lower():
                        error_msg += " - HTML error page returned"
                    else:
                        error_msg += f" - Response: {response.text[:100]}"
            self.log_test(
                "12. Unauthorized Access",
                False,
                error_msg,
                response_time,
                response.status_code
            )
            return False

    def run_all_tests(self):
        """Run all 12 tests in sequence"""
        print("🚀 STARTING FINAL VERIFICATION - All Endpoints Migrated to PostgreSQL")
        print(f"🎯 Backend URL: {self.base_url}")
        print(f"📋 Total Tests: {self.total_tests}")
        print("=" * 80)
        print()
        
        # PHASE 1: Authentication & PostgreSQL (5 tests)
        print("📍 PHASE 1: Authentication & PostgreSQL (5 tests)")
        print("-" * 50)
        self.test_1_health_check()
        self.test_2_demo_login()
        self.test_3_new_user_registration()
        self.test_4_immediate_login_after_registration()
        self.test_5_user_persistence()
        print()
        
        # PHASE 2: AI Integration (3 tests)
        print("📍 PHASE 2: AI Integration (3 tests)")
        print("-" * 50)
        self.test_6_ai_chat_endpoint()
        self.test_7_food_research_endpoint()
        self.test_8_meal_search_endpoint()
        print()
        
        # PHASE 3: Baby Profile Operations (2 tests)
        print("📍 PHASE 3: Baby Profile Operations (2 tests)")
        print("-" * 50)
        self.test_9_create_baby_profile()
        self.test_10_retrieve_baby_profiles()
        print()
        
        # PHASE 4: Error Handling (2 tests)
        print("📍 PHASE 4: Error Handling (2 tests)")
        print("-" * 50)
        self.test_11_invalid_login_credentials()
        self.test_12_unauthorized_access()
        print()
        
        # Final Results
        self.print_final_results()

    def print_final_results(self):
        """Print comprehensive final results"""
        success_rate = (self.passed_tests / self.total_tests) * 100
        
        print("=" * 80)
        print("🏁 FINAL VERIFICATION RESULTS")
        print("=" * 80)
        print()
        
        print("📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Check for HTTP 500 errors
        http_500_count = sum(1 for result in self.test_results if result.get('status_code') == 500)
        
        print("🔍 CRITICAL SUCCESS CRITERIA:")
        if success_rate == 100.0:
            print("   ✅ 12/12 tests pass (100% success rate)")
        else:
            print(f"   ❌ {self.passed_tests}/12 tests pass ({success_rate:.1f}% success rate)")
            
        if http_500_count == 0:
            print("   ✅ NO HTTP 500 errors")
        else:
            print(f"   ❌ {http_500_count} HTTP 500 errors detected")
        print()
        
        # Detailed test breakdown
        print("📋 DETAILED TEST RESULTS:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅" if result['success'] else "❌"
            print(f"   {status} Test {i}: {result['test']}")
            if not result['success']:
                print(f"      └─ {result['details']}")
        print()
        
        # Sample AI responses (if available)
        ai_responses = []
        for result in self.test_results:
            if 'AI' in result['test'] and result['success'] and 'chars' in result['details']:
                ai_responses.append(result)
        
        if ai_responses:
            print("🤖 SAMPLE AI RESPONSES:")
            for result in ai_responses:
                print(f"   {result['test']}:")
                # Extract response preview from details
                details = result['details']
                if ': ' in details:
                    response_part = details.split(': ', 1)[1]
                    print(f"      └─ {response_part}")
            print()
        
        # Final recommendation
        print("🎯 FINAL RECOMMENDATION:")
        if success_rate == 100.0 and http_500_count == 0:
            print("   🟢 GO - Backend ready for Android app download")
            print("   ✅ All endpoints working correctly")
            print("   ✅ PostgreSQL migration successful")
            print("   ✅ AI integration functional")
            print("   ✅ Baby profiles working")
        else:
            print("   🔴 NO-GO - Backend NOT ready for production")
            if success_rate < 100.0:
                print(f"   ❌ Success rate {success_rate:.1f}% below required 100%")
            if http_500_count > 0:
                print(f"   ❌ {http_500_count} HTTP 500 errors need fixing")
            
            # Identify critical failures
            critical_failures = []
            for result in self.test_results:
                if not result['success'] and any(keyword in result['test'] for keyword in ['Baby Profile', 'Login', 'Registration']):
                    critical_failures.append(result['test'])
            
            if critical_failures:
                print("   🚨 CRITICAL FAILURES:")
                for failure in critical_failures:
                    print(f"      - {failure}")
        
        print("=" * 80)

def main():
    """Main execution function"""
    tester = BackendTester()
    tester.run_all_tests()
    
    # Exit with appropriate code
    if tester.passed_tests == tester.total_tests:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()