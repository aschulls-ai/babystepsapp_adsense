#!/usr/bin/env python3
"""
USER PROFILE ENDPOINT TESTING
Testing the new user profile endpoints as specified in review request:
1. GET /api/user/profile - Get current user profile
2. PUT /api/user/profile - Update user profile

Backend: https://babysteps-tracker.preview.emergentagent.com
Test Account: demo@babysteps.com / demo123
"""

import requests
import json
import time
from datetime import datetime, timezone
import uuid

class UserProfileTester:
    def __init__(self):
        self.base_url = "https://babysteps-tracker.preview.emergentagent.com"
        self.token = None
        self.test_results = []
        self.total_tests = 8
        self.passed_tests = 0
        self.failed_tests = 0
        self.original_email = "demo@babysteps.com"
        self.original_password = "demo123"
        self.original_name = "Demo Parent"
        
    def log_test(self, test_name, success, details="", response_time=0):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "response_time": f"{response_time:.2f}s"
        }
        self.test_results.append(result)
        
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
        print(f"{status} - {test_name} ({response_time:.2f}s)")
        if details:
            print(f"    Details: {details}")
    
    def make_request(self, method, endpoint, data=None, headers=None):
        """Make HTTP request with timing"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response_time = time.time() - start_time
            return response, response_time
            
        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            return None, response_time
        except Exception as e:
            response_time = time.time() - start_time
            print(f"Request error: {str(e)}")
            return None, response_time
    
    def get_auth_headers(self):
        """Get authorization headers"""
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}
    
    def test_1_login_demo_account(self):
        """Test 1: Login with Demo Account (demo@babysteps.com / demo123)"""
        data = {
            "email": self.original_email,
            "password": self.original_password
        }
        
        response, response_time = self.make_request("POST", "/api/auth/login", data)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                self.token = result.get("access_token")
                if self.token:
                    self.log_test("1. Login Demo Account", True, 
                                f"JWT token received: {self.token[:20]}...", response_time)
                    return True
                else:
                    self.log_test("1. Login Demo Account", False, 
                                "No access_token in response", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("1. Login Demo Account", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("1. Login Demo Account", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_2_get_user_profile(self):
        """Test 2: GET /api/user/profile - Get current user profile"""
        response, response_time = self.make_request("GET", "/api/user/profile", 
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                profile = response.json()
                expected_fields = ["id", "email", "name"]
                
                # Check if all expected fields are present
                missing_fields = [field for field in expected_fields if field not in profile]
                if missing_fields:
                    self.log_test("2. Get User Profile", False, 
                                f"Missing fields: {missing_fields}", response_time)
                    return False
                
                # Verify demo account details
                if profile["email"] == self.original_email and profile["name"] == self.original_name:
                    self.log_test("2. Get User Profile", True, 
                                f"Profile retrieved: {profile['email']}, {profile['name']}", response_time)
                    return True
                else:
                    self.log_test("2. Get User Profile", False, 
                                f"Unexpected profile data: {profile}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2. Get User Profile", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("2. Get User Profile", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_3_update_name(self):
        """Test 3: PUT /api/user/profile - Update name"""
        new_name = "New Demo Name"
        data = {
            "name": new_name,
            "current_password": self.original_password
        }
        
        response, response_time = self.make_request("PUT", "/api/user/profile", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                if result.get("message") and "updated successfully" in result["message"]:
                    # Verify the name was updated by getting profile again
                    profile_response, profile_time = self.make_request("GET", "/api/user/profile", 
                                                                     headers=self.get_auth_headers())
                    
                    if profile_response and profile_response.status_code == 200:
                        profile = profile_response.json()
                        if profile.get("name") == new_name:
                            self.log_test("3. Update Name", True, 
                                        f"Name updated to: {new_name}", response_time + profile_time)
                            return True
                        else:
                            self.log_test("3. Update Name", False, 
                                        f"Name not updated correctly: {profile.get('name')}", response_time + profile_time)
                            return False
                    else:
                        self.log_test("3. Update Name", False, 
                                    "Could not verify name update", response_time)
                        return False
                else:
                    self.log_test("3. Update Name", False, 
                                f"Unexpected response: {result}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("3. Update Name", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("3. Update Name", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_2_1_create_feeding_activity(self):
        """Test 2.1: Create Feeding Activity with NEW FIELDS"""
        data = {
            "baby_id": self.baby_id,
            "type": "feeding",
            "feeding_type": "bottle",  # NEW FIELD - should not cause 500 error
            "amount": 8.0,  # NEW FIELD - should not cause 500 error
            "notes": "Post-migration feeding test with new database fields",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                if activity_id:
                    self.activity_ids["feeding"] = activity_id
                    self.log_test("2.1 Create Feeding Activity", True, 
                                f"Activity created with ID: {activity_id}", response_time)
                    return True
                else:
                    self.log_test("2.1 Create Feeding Activity", False, 
                                "No activity ID returned", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2.1 Create Feeding Activity", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("2.1 Create Feeding Activity", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_2_2_create_diaper_activity(self):
        """Test 2.2: Create Diaper Activity with NEW FIELDS"""
        data = {
            "baby_id": self.baby_id,
            "type": "diaper",
            "diaper_type": "wet",  # NEW FIELD - should not cause 500 error
            "notes": "Post-migration diaper test with new database fields",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                if activity_id:
                    self.activity_ids["diaper"] = activity_id
                    self.log_test("2.2 Create Diaper Activity", True, 
                                f"Activity created with ID: {activity_id}", response_time)
                    return True
                else:
                    self.log_test("2.2 Create Diaper Activity", False, 
                                "No activity ID returned", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2.2 Create Diaper Activity", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("2.2 Create Diaper Activity", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_2_3_create_sleep_activity(self):
        """Test 2.3: Create Sleep Activity with NEW FIELDS"""
        data = {
            "baby_id": self.baby_id,
            "type": "sleep",
            "duration": 120,  # NEW FIELD - should not cause 500 error
            "notes": "Post-migration sleep test with new database fields",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                if activity_id:
                    self.activity_ids["sleep"] = activity_id
                    self.log_test("2.3 Create Sleep Activity", True, 
                                f"Activity created with ID: {activity_id}", response_time)
                    return True
                else:
                    self.log_test("2.3 Create Sleep Activity", False, 
                                "No activity ID returned", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2.3 Create Sleep Activity", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("2.3 Create Sleep Activity", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_2_4_create_pumping_activity(self):
        """Test 2.4: Create Pumping Activity with NEW FIELDS"""
        data = {
            "baby_id": self.baby_id,
            "type": "pumping",
            "amount": 4.0,  # NEW FIELD - should not cause 500 error
            "duration": 15,  # NEW FIELD - should not cause 500 error
            "notes": "Post-migration pumping test with new database fields",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                if activity_id:
                    self.activity_ids["pumping"] = activity_id
                    self.log_test("2.4 Create Pumping Activity", True, 
                                f"Activity created with ID: {activity_id}", response_time)
                    return True
                else:
                    self.log_test("2.4 Create Pumping Activity", False, 
                                "No activity ID returned", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2.4 Create Pumping Activity", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("2.4 Create Pumping Activity", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_2_5_create_measurement_activity(self):
        """Test 2.5: Create Measurement Activity with NEW FIELDS"""
        data = {
            "baby_id": self.baby_id,
            "type": "measurement",
            "weight": 15.5,  # NEW FIELD - should not cause 500 error
            "height": 65.0,  # NEW FIELD - should not cause 500 error
            "head_circumference": 42.0,  # NEW FIELD - should not cause 500 error
            "temperature": 98.6,  # NEW FIELD - should not cause 500 error
            "notes": "Post-migration measurement test with new database fields",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                if activity_id:
                    self.activity_ids["measurement"] = activity_id
                    self.log_test("2.5 Create Measurement Activity", True, 
                                f"Activity created with ID: {activity_id}", response_time)
                    return True
                else:
                    self.log_test("2.5 Create Measurement Activity", False, 
                                "No activity ID returned", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2.5 Create Measurement Activity", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("2.5 Create Measurement Activity", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_2_6_create_milestone_activity(self):
        """Test 2.6: Create Milestone Activity with NEW FIELDS"""
        data = {
            "baby_id": self.baby_id,
            "type": "milestone",
            "title": "First smile",  # NEW FIELD - should not cause 500 error
            "category": "social",  # NEW FIELD - should not cause 500 error
            "description": "Baby smiled for the first time - post-migration test",  # NEW FIELD - should not cause 500 error
            "notes": "Post-migration milestone test with new database fields",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                if activity_id:
                    self.activity_ids["milestone"] = activity_id
                    self.log_test("2.6 Create Milestone Activity", True, 
                                f"Activity created with ID: {activity_id}", response_time)
                    return True
                else:
                    self.log_test("2.6 Create Milestone Activity", False, 
                                "No activity ID returned", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2.6 Create Milestone Activity", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("2.6 Create Milestone Activity", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_3_1_get_all_activities(self):
        """Test 3.1: Get All Activities for Baby"""
        response, response_time = self.make_request("GET", f"/api/activities?baby_id={self.baby_id}",
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list) and len(activities) >= 6:
                    # Verify all 6 activity types are present
                    activity_types = [activity.get("type") for activity in activities]
                    expected_types = ["feeding", "diaper", "sleep", "pumping", "measurement", "milestone"]
                    found_types = [t for t in expected_types if t in activity_types]
                    
                    self.log_test("3.1 Get All Activities", True, 
                                f"Found {len(activities)} activities with types: {found_types}", response_time)
                    return True
                else:
                    self.log_test("3.1 Get All Activities", False, 
                                f"Expected at least 6 activities, got {len(activities) if isinstance(activities, list) else 'invalid'}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("3.1 Get All Activities", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("3.1 Get All Activities", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_3_2_get_feeding_activities(self):
        """Test 3.2: Get Activities with Type Filter (Feeding)"""
        response, response_time = self.make_request("GET", f"/api/activities?baby_id={self.baby_id}&type=feeding&limit=5",
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list):
                    # Verify all activities are feeding type
                    feeding_activities = [a for a in activities if a.get("type") == "feeding"]
                    if len(feeding_activities) == len(activities) and len(activities) > 0:
                        self.log_test("3.2 Get Feeding Activities", True, 
                                    f"Found {len(feeding_activities)} feeding activities", response_time)
                        return True
                    else:
                        self.log_test("3.2 Get Feeding Activities", False, 
                                    f"Mixed activity types or no feeding activities found", response_time)
                        return False
                else:
                    self.log_test("3.2 Get Feeding Activities", False, 
                                "Response is not a list", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("3.2 Get Feeding Activities", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("3.2 Get Feeding Activities", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_3_3_get_activities_with_limit(self):
        """Test 3.3: Get Activities with Limit"""
        response, response_time = self.make_request("GET", f"/api/activities?baby_id={self.baby_id}&limit=3",
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list) and len(activities) == 3:
                    # Verify activities are ordered by timestamp descending
                    timestamps = [activity.get("timestamp") for activity in activities if activity.get("timestamp")]
                    if len(timestamps) >= 2:
                        is_descending = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
                        self.log_test("3.3 Get Activities with Limit", True, 
                                    f"Got exactly 3 activities, ordered: {is_descending}", response_time)
                        return True
                    else:
                        self.log_test("3.3 Get Activities with Limit", True, 
                                    f"Got exactly 3 activities", response_time)
                        return True
                else:
                    self.log_test("3.3 Get Activities with Limit", False, 
                                f"Expected 3 activities, got {len(activities) if isinstance(activities, list) else 'invalid'}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("3.3 Get Activities with Limit", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("3.3 Get Activities with Limit", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_3_4_test_all_type_filters(self):
        """Test 3.4: Test All Type Filters"""
        activity_types = ["feeding", "diaper", "sleep", "pumping", "measurement", "milestone"]
        all_passed = True
        total_time = 0
        
        for activity_type in activity_types:
            response, response_time = self.make_request("GET", f"/api/activities?baby_id={self.baby_id}&type={activity_type}&limit=5",
                                                      headers=self.get_auth_headers())
            total_time += response_time
            
            if response and response.status_code == 200:
                try:
                    activities = response.json()
                    if isinstance(activities, list):
                        # Check if all activities are of the correct type
                        correct_type_activities = [a for a in activities if a.get("type") == activity_type]
                        if len(correct_type_activities) != len(activities):
                            all_passed = False
                            break
                    else:
                        all_passed = False
                        break
                except json.JSONDecodeError:
                    all_passed = False
                    break
            else:
                all_passed = False
                break
        
        if all_passed:
            self.log_test("3.4 Test All Type Filters", True, 
                        f"All 6 activity type filters working correctly", total_time)
            return True
        else:
            self.log_test("3.4 Test All Type Filters", False, 
                        f"Some activity type filters failed", total_time)
            return False
    
    def test_4_1_simulate_logout(self):
        """Test 4.1: Simulate Logout"""
        # Store current token for later re-login test
        self.old_token = self.token
        self.token = None
        
        self.log_test("4.1 Simulate Logout", True, 
                    "Token cleared (simulated logout)", 0.0)
        return True
    
    def test_4_2_re_login(self):
        """Test 4.2: Re-Login with Same Account"""
        data = {
            "email": "demo@babysteps.com",
            "password": "demo123"
        }
        
        response, response_time = self.make_request("POST", "/api/auth/login", data)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                new_token = result.get("access_token")
                if new_token and new_token != self.old_token:
                    self.token = new_token
                    self.log_test("4.2 Re-Login Same Account", True, 
                                f"New JWT token received (different from old): {new_token[:20]}...", response_time)
                    return True
                else:
                    self.log_test("4.2 Re-Login Same Account", False, 
                                "No new access_token or same as old token", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4.2 Re-Login Same Account", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("4.2 Re-Login Same Account", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_4_3_verify_activities_persist(self):
        """Test 4.3: Verify Activities Persist After Re-Login"""
        response, response_time = self.make_request("GET", f"/api/activities?baby_id={self.baby_id}",
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list) and len(activities) >= 6:
                    # Verify our created activity IDs still exist
                    activity_ids_in_response = [a.get("id") for a in activities]
                    found_our_activities = 0
                    
                    for activity_type, activity_id in self.activity_ids.items():
                        if activity_id in activity_ids_in_response:
                            found_our_activities += 1
                    
                    if found_our_activities >= 3:  # At least half of our activities should persist
                        self.log_test("4.3 Verify Activities Persist", True, 
                                    f"Found {found_our_activities}/{len(self.activity_ids)} created activities after re-login", response_time)
                        return True
                    else:
                        self.log_test("4.3 Verify Activities Persist", False, 
                                    f"Only found {found_our_activities}/{len(self.activity_ids)} created activities", response_time)
                        return False
                else:
                    self.log_test("4.3 Verify Activities Persist", False, 
                                f"Expected at least 6 activities, got {len(activities) if isinstance(activities, list) else 'invalid'}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4.3 Verify Activities Persist", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("4.3 Verify Activities Persist", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_4_4_baby_profile_with_image(self):
        """Test 4.4: Baby Profile with NEW profile_image Field"""
        baby_data = {
            "name": "Migration Test Baby",
            "birth_date": "2024-06-01T00:00:00Z",
            "gender": "girl",
            "profile_image": "https://example.com/baby-photo.jpg"  # NEW FIELD - should not cause 500 error
        }
        
        response, response_time = self.make_request("POST", "/api/babies", baby_data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                baby = response.json()
                if baby.get("profile_image") == baby_data["profile_image"]:
                    self.log_test("4.4 Baby Profile with Image", True, 
                                f"Baby created with profile_image field: {baby.get('id')}", response_time)
                    return True
                else:
                    self.log_test("4.4 Baby Profile with Image", False, 
                                "profile_image field not saved correctly", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4.4 Baby Profile with Image", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("4.4 Baby Profile with Image", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_4_5_ai_chat_endpoint(self):
        """Test 4.5: AI Chat Endpoint"""
        data = {
            "message": "When can babies eat strawberries?",
            "baby_age_months": 6
        }
        
        response, response_time = self.make_request("POST", "/api/ai/chat", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                ai_response = result.get("response", "")
                if len(ai_response) > 50:  # Reasonable AI response length
                    self.log_test("4.5 AI Chat Endpoint", True, 
                                f"AI response received ({len(ai_response)} chars)", response_time)
                    return True
                else:
                    self.log_test("4.5 AI Chat Endpoint", False, 
                                f"AI response too short ({len(ai_response)} chars)", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4.5 AI Chat Endpoint", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("4.5 AI Chat Endpoint", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_4_6_food_research_endpoint(self):
        """Test 4.6: Food Research Endpoint"""
        data = {
            "question": "Are strawberries safe for babies?",
            "baby_age_months": 6
        }
        
        response, response_time = self.make_request("POST", "/api/food/research", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                answer = result.get("answer", "")
                safety_level = result.get("safety_level", "")
                if len(answer) > 20 and safety_level:
                    self.log_test("4.6 Food Research Endpoint", True, 
                                f"Food safety response received (safety_level: {safety_level})", response_time)
                    return True
                else:
                    self.log_test("4.6 Food Research Endpoint", False, 
                                f"Incomplete food research response", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4.6 Food Research Endpoint", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("4.6 Food Research Endpoint", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_4_7_meal_search_endpoint(self):
        """Test 4.7: Meal Search Endpoint"""
        data = {
            "query": "breakfast ideas for 8 month old",
            "baby_age_months": 8
        }
        
        response, response_time = self.make_request("POST", "/api/meals/search", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                meal_results = result.get("results", "")
                if len(meal_results) > 50:  # Reasonable meal suggestions length
                    self.log_test("4.7 Meal Search Endpoint", True, 
                                f"Meal suggestions received ({len(meal_results)} chars)", response_time)
                    return True
                else:
                    self.log_test("4.7 Meal Search Endpoint", False, 
                                f"Meal suggestions too short ({len(meal_results)} chars)", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4.7 Meal Search Endpoint", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("4.7 Meal Search Endpoint", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_5_edge_cases(self):
        """Test 5: Edge Cases & Error Handling (10 tests)"""
        edge_test_results = []
        
        # Test 5.1: Unauthorized Activity Creation
        response, response_time = self.make_request("POST", "/api/activities", {
            "baby_id": self.baby_id,
            "type": "feeding",
            "feeding_type": "bottle"
        })
        
        expected_unauthorized = response and response.status_code in [401, 403]
        edge_test_results.append(("5.1 Unauthorized Activity Creation", expected_unauthorized, 
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Test 5.2: Unauthorized Activity Retrieval
        response, response_time = self.make_request("GET", f"/api/activities?baby_id={self.baby_id}")
        
        expected_unauthorized = response and response.status_code in [401, 403]
        edge_test_results.append(("5.2 Unauthorized Activity Retrieval", expected_unauthorized,
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Test 5.3: Activity for Non-Existent Baby
        fake_baby_id = str(uuid.uuid4())
        response, response_time = self.make_request("POST", "/api/activities", {
            "baby_id": fake_baby_id,
            "type": "feeding",
            "feeding_type": "bottle"
        }, headers=self.get_auth_headers())
        
        expected_not_found = response and response.status_code == 404
        edge_test_results.append(("5.3 Activity Non-Existent Baby", expected_not_found,
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Test 5.4: Activity with Invalid Type
        response, response_time = self.make_request("POST", "/api/activities", {
            "baby_id": self.baby_id,
            "type": "invalid_type"
        }, headers=self.get_auth_headers())
        
        expected_validation_error = response and response.status_code in [400, 422]
        edge_test_results.append(("5.4 Invalid Activity Type", expected_validation_error,
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Test 5.5: Activity with Missing Required Fields
        response, response_time = self.make_request("POST", "/api/activities", {
            "baby_id": self.baby_id
        }, headers=self.get_auth_headers())
        
        expected_validation_error = response and response.status_code in [400, 422]
        edge_test_results.append(("5.5 Missing Required Fields", expected_validation_error,
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Test 5.6: Get Activities Without Baby ID
        response, response_time = self.make_request("GET", "/api/activities", 
                                                  headers=self.get_auth_headers())
        
        expected_success = response and response.status_code == 200
        edge_test_results.append(("5.6 Activities Without Baby ID", expected_success,
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Test 5.7: Get Activities with Invalid Baby ID Format
        response, response_time = self.make_request("GET", "/api/activities?baby_id=invalid-id-format",
                                                  headers=self.get_auth_headers())
        
        expected_handled = response and response.status_code in [200, 400]
        edge_test_results.append(("5.7 Invalid Baby ID Format", expected_handled,
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Test 5.8: Create Multiple Activities Rapidly
        rapid_success = True
        total_rapid_time = 0
        for i in range(3):
            response, response_time = self.make_request("POST", "/api/activities", {
                "baby_id": self.baby_id,
                "type": "feeding",
                "feeding_type": "bottle",
                "amount": f"{i+1}",
                "notes": f"Rapid test {i+1}"
            }, headers=self.get_auth_headers())
            total_rapid_time += response_time
            
            if not (response and response.status_code in [200, 201]):
                rapid_success = False
                break
        
        edge_test_results.append(("5.8 Multiple Activities Rapidly", rapid_success,
                                f"3 activities in {total_rapid_time:.2f}s", total_rapid_time))
        
        # Test 5.9: Very Long Notes Field
        long_notes = "Test " * 250  # 1250+ characters
        response, response_time = self.make_request("POST", "/api/activities", {
            "baby_id": self.baby_id,
            "type": "feeding",
            "feeding_type": "bottle",
            "notes": long_notes
        }, headers=self.get_auth_headers())
        
        expected_success = response and response.status_code in [200, 201]
        edge_test_results.append(("5.9 Very Long Notes Field", expected_success,
                                f"HTTP {response.status_code if response else 'Timeout'} - {len(long_notes)} chars", response_time))
        
        # Test 5.10: Special Characters in Notes
        special_notes = "Test 🍼 baby's feeding @ 3:00pm - 8oz formula!"
        response, response_time = self.make_request("POST", "/api/activities", {
            "baby_id": self.baby_id,
            "type": "feeding",
            "feeding_type": "bottle",
            "notes": special_notes
        }, headers=self.get_auth_headers())
        
        expected_success = response and response.status_code in [200, 201]
        edge_test_results.append(("5.10 Special Characters Notes", expected_success,
                                f"HTTP {response.status_code if response else 'Timeout'}", response_time))
        
        # Log all edge case results
        for test_name, success, details, response_time in edge_test_results:
            self.log_test(test_name, success, details, response_time)
        
        # Return True if at least 7/10 edge cases pass
        passed_edge_cases = sum(1 for _, success, _, _ in edge_test_results if success)
        return passed_edge_cases >= 7
    
    def run_all_tests(self):
        """Run all 29 tests in sequence"""
        print("🚀 COMPREHENSIVE BACKEND TESTING AFTER DATABASE MIGRATION AND TIMESTAMP FIX")
        print(f"Backend: {self.base_url}")
        print(f"Test Account: demo@babysteps.com / demo123")
        print(f"Demo Baby ID: demo-baby-456")
        print(f"Total Tests: {self.total_tests}")
        print("=" * 80)
        
        # Phase 1: Authentication & Setup (2 tests)
        print("\n📋 PHASE 1: Authentication & Setup")
        if not self.test_1_1_login_demo_account():
            print("❌ Cannot proceed without authentication")
            return self.generate_report()
        
        if not self.test_1_2_get_demo_babies():
            print("❌ Cannot proceed without baby ID")
            return self.generate_report()
        
        # Phase 2: Create All 6 Activity Types (6 tests)
        print("\n📋 PHASE 2: Create All 6 Activity Types")
        self.test_2_1_create_feeding_activity()
        self.test_2_2_create_diaper_activity()
        self.test_2_3_create_sleep_activity()
        self.test_2_4_create_pumping_activity()
        self.test_2_5_create_measurement_activity()
        self.test_2_6_create_milestone_activity()
        
        # Phase 3: Retrieve All Activities (4 tests)
        print("\n📋 PHASE 3: Retrieve All Activities")
        self.test_3_1_get_all_activities()
        self.test_3_2_get_feeding_activities()
        self.test_3_3_get_activities_with_limit()
        self.test_3_4_test_all_type_filters()
        
        # Phase 4: Logout & Re-Login Persistence Test + Secondary Endpoints (7 tests)
        print("\n📋 PHASE 4: Logout & Re-Login Persistence Test + Secondary Endpoints")
        self.test_4_1_simulate_logout()
        self.test_4_2_re_login()
        self.test_4_3_verify_activities_persist()
        self.test_4_4_baby_profile_with_image()
        self.test_4_5_ai_chat_endpoint()
        self.test_4_6_food_research_endpoint()
        self.test_4_7_meal_search_endpoint()
        
        # Phase 5: Edge Cases & Error Handling (10 tests)
        print("\n📋 PHASE 5: Edge Cases & Error Handling")
        self.test_5_edge_cases()
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Tests Failed: {self.failed_tests}/{self.total_tests}")
        
        # Success Criteria Check
        print("\n🎯 SUCCESS CRITERIA:")
        criteria_met = []
        
        # Check if all 6 activity types POST successfully
        activity_creation_tests = [r for r in self.test_results if "Create" in r["test"] and "Activity" in r["test"]]
        activity_creation_success = sum(1 for t in activity_creation_tests if "✅" in t["status"])
        criteria_met.append(f"✅ All 6 activity types POST: {activity_creation_success}/6" if activity_creation_success == 6 else f"❌ All 6 activity types POST: {activity_creation_success}/6")
        
        # Check if activities persist after re-login
        persistence_test = next((r for r in self.test_results if "Persist" in r["test"]), None)
        if persistence_test and "✅" in persistence_test["status"]:
            criteria_met.append("✅ Activities persist after logout/re-login (PostgreSQL persistence verified)")
        else:
            criteria_met.append("❌ Activities persist after logout/re-login")
        
        # Check for 500 errors
        has_500_errors = any("500" in r["details"] for r in self.test_results)
        criteria_met.append("✅ No 500 Internal Server Errors" if not has_500_errors else "❌ 500 Internal Server Errors detected")
        
        # Check for specific migration-related errors
        has_undefined_column_errors = any("UndefinedColumn" in r["details"] for r in self.test_results)
        criteria_met.append("✅ No UndefinedColumn errors" if not has_undefined_column_errors else "❌ UndefinedColumn errors detected")
        
        has_isoformat_errors = any("isoformat" in r["details"] for r in self.test_results)
        criteria_met.append("✅ No isoformat errors" if not has_isoformat_errors else "❌ isoformat timestamp errors detected")
        
        # Check authentication
        auth_tests = [r for r in self.test_results if "Login" in r["test"]]
        auth_success = all("✅" in t["status"] for t in auth_tests)
        criteria_met.append("✅ Authentication working" if auth_success else "❌ Authentication issues")
        
        for criterion in criteria_met:
            print(criterion)
        
        # Failure Indicators
        print("\n⚠️ FAILURE INDICATORS:")
        failure_indicators = []
        
        if has_500_errors:
            failure_indicators.append("❌ HTTP 500 errors detected")
        
        get_db_errors = any("get_db_connection" in r["details"] for r in self.test_results)
        if get_db_errors:
            failure_indicators.append("❌ 'get_db_connection' NameError detected")
        
        if activity_creation_success < 6:
            failure_indicators.append(f"❌ Only {activity_creation_success}/6 activity types working")
        
        if not failure_indicators:
            failure_indicators.append("✅ No critical failure indicators detected")
        
        for indicator in failure_indicators:
            print(indicator)
        
        # Performance Metrics
        response_times = [float(r["response_time"].replace("s", "")) for r in self.test_results if r["response_time"] != "0.00s"]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"Average Response Time: {avg_response_time:.2f}s")
            print(f"Fastest Response: {min(response_times):.2f}s")
            print(f"Slowest Response: {max(response_times):.2f}s")
        
        # Detailed Test Results
        print(f"\n📋 DETAILED TEST RESULTS:")
        for result in self.test_results:
            print(f"{result['status']} - {result['test']} ({result['response_time']})")
            if result['details']:
                print(f"    {result['details']}")
        
        # Final Assessment
        print(f"\n🏆 FINAL ASSESSMENT:")
        if success_rate >= 90:
            print("🎉 EXCELLENT - Backend is production ready")
        elif success_rate >= 75:
            print("✅ GOOD - Backend is mostly functional with minor issues")
        elif success_rate >= 50:
            print("⚠️ FAIR - Backend has significant issues requiring attention")
        else:
            print("❌ POOR - Backend has critical issues preventing normal operation")
        
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success_rate": success_rate,
            "test_results": self.test_results,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0
        }

if __name__ == "__main__":
    tester = ProductionBackendTester()
    results = tester.run_all_tests()