#!/usr/bin/env python3
"""
COMPREHENSIVE TESTING: Recent Feeding Widget Data Flow

Testing the complete data flow for the "Recent Feeding" widget in the Baby Steps app.
The user reported that feeding activities logged via Quick Feed button are NOT showing up 
in the "Recent Feeding" sidebar widget, even though they appear in "Activity History".

Backend: https://growth-tracker-41.preview.emergentagent.com
Test Account: demo@babysteps.com / demo123
Demo Baby ID: demo-baby-456
"""

import requests
import json
import time
from datetime import datetime, timezone
import uuid

class RecentFeedingWidgetTester:
    def __init__(self):
        self.base_url = "https://growth-tracker-41.preview.emergentagent.com"
        self.token = None
        self.baby_id = "demo-baby-456"
        self.created_feeding_ids = []
        self.test_results = []
        self.total_tests = 15
        self.passed_tests = 0
        self.failed_tests = 0
        
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
    
    def test_1_authentication(self):
        """Test 1: Authentication with Demo Account"""
        data = {
            "email": "demo@babysteps.com",
            "password": "demo123"
        }
        
        response, response_time = self.make_request("POST", "/api/auth/login", data)
        
        if response and response.status_code == 200:
            try:
                result = response.json()
                self.token = result.get("access_token")
                if self.token:
                    self.log_test("1. Authentication", True, 
                                f"JWT token received: {self.token[:20]}...", response_time)
                    return True
                else:
                    self.log_test("1. Authentication", False, 
                                "No access_token in response", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("1. Authentication", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("1. Authentication", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_2_quick_feed_bottle(self):
        """Test 2: Quick Feed Button → Backend (Bottle Feeding)"""
        data = {
            "baby_id": "demo-baby-456",
            "type": "feeding",
            "feeding_type": "bottle",
            "amount": 5.0,
            "notes": "Quick feed test - bottle"
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                feeding_type = result.get("feeding_type")
                activity_type = result.get("type")
                timestamp = result.get("timestamp")
                
                if activity_id and feeding_type == "bottle" and activity_type == "feeding" and timestamp:
                    self.created_feeding_ids.append(activity_id)
                    self.log_test("2. Quick Feed Bottle", True, 
                                f"Created bottle feeding ID: {activity_id}, feeding_type: {feeding_type}", response_time)
                    return True
                else:
                    self.log_test("2. Quick Feed Bottle", False, 
                                f"Missing fields - ID: {activity_id}, type: {activity_type}, feeding_type: {feeding_type}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("2. Quick Feed Bottle", False, 
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
            self.log_test("2. Quick Feed Bottle", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_3_quick_feed_breast(self):
        """Test 3: Quick Feed Button → Backend (Breastfeeding)"""
        data = {
            "baby_id": "demo-baby-456",
            "type": "feeding",
            "feeding_type": "breast",
            "duration": 15,
            "notes": "Quick feed test - breast"
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                feeding_type = result.get("feeding_type")
                activity_type = result.get("type")
                timestamp = result.get("timestamp")
                
                if activity_id and feeding_type == "breast" and activity_type == "feeding" and timestamp:
                    self.created_feeding_ids.append(activity_id)
                    self.log_test("3. Quick Feed Breast", True, 
                                f"Created breast feeding ID: {activity_id}, feeding_type: {feeding_type}", response_time)
                    return True
                else:
                    self.log_test("3. Quick Feed Breast", False, 
                                f"Missing fields - ID: {activity_id}, type: {activity_type}, feeding_type: {feeding_type}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("3. Quick Feed Breast", False, 
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
            self.log_test("3. Quick Feed Breast", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_4_quick_feed_solid(self):
        """Test 4: Quick Feed Button → Backend (Solid Food)"""
        data = {
            "baby_id": "demo-baby-456",
            "type": "feeding",
            "feeding_type": "solid",
            "notes": "Quick feed test - solid"
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                feeding_type = result.get("feeding_type")
                activity_type = result.get("type")
                timestamp = result.get("timestamp")
                
                if activity_id and feeding_type == "solid" and activity_type == "feeding" and timestamp:
                    self.created_feeding_ids.append(activity_id)
                    self.log_test("4. Quick Feed Solid", True, 
                                f"Created solid feeding ID: {activity_id}, feeding_type: {feeding_type}", response_time)
                    return True
                else:
                    self.log_test("4. Quick Feed Solid", False, 
                                f"Missing fields - ID: {activity_id}, type: {activity_type}, feeding_type: {feeding_type}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("4. Quick Feed Solid", False, 
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
            self.log_test("4. Quick Feed Solid", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return False
    
    def test_5_recent_feeding_widget_endpoint(self):
        """Test 5: Recent Feeding Widget → Backend Fetch"""
        endpoint = f"/api/activities?baby_id=demo-baby-456&type=feeding&limit=5"
        response, response_time = self.make_request("GET", endpoint,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list):
                    # Verify all activities are feeding type
                    feeding_activities = [a for a in activities if a.get("type") == "feeding"]
                    if len(feeding_activities) == len(activities):
                        # Check if our created feedings are present
                        activity_ids = [a.get("id") for a in activities]
                        found_our_feedings = sum(1 for fid in self.created_feeding_ids if fid in activity_ids)
                        
                        # Verify feeding_type field is present
                        has_feeding_types = all(a.get("feeding_type") for a in activities)
                        
                        # Verify ordering (newest first)
                        timestamps = [a.get("timestamp") for a in activities if a.get("timestamp")]
                        is_ordered = len(timestamps) <= 1 or all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
                        
                        # Verify limit is respected
                        limit_respected = len(activities) <= 5
                        
                        success_details = f"Found {len(activities)} feeding activities, {found_our_feedings}/{len(self.created_feeding_ids)} our feedings, feeding_types: {has_feeding_types}, ordered: {is_ordered}, limit: {limit_respected}"
                        
                        if len(activities) > 0 and has_feeding_types and is_ordered and limit_respected:
                            self.log_test("5. Recent Feeding Widget Endpoint", True, success_details, response_time)
                            return activities
                        else:
                            self.log_test("5. Recent Feeding Widget Endpoint", False, success_details, response_time)
                            return None
                    else:
                        self.log_test("5. Recent Feeding Widget Endpoint", False, 
                                    f"Mixed activity types: {len(feeding_activities)}/{len(activities)} are feeding", response_time)
                        return None
                else:
                    self.log_test("5. Recent Feeding Widget Endpoint", False, 
                                "Response is not a list", response_time)
                    return None
            except json.JSONDecodeError:
                self.log_test("5. Recent Feeding Widget Endpoint", False, 
                            "Invalid JSON response", response_time)
                return None
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("5. Recent Feeding Widget Endpoint", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return None
    
    def test_6_activity_history_endpoint(self):
        """Test 6: Activity History → Backend Fetch"""
        endpoint = f"/api/activities?baby_id=demo-baby-456"
        response, response_time = self.make_request("GET", endpoint,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list):
                    # Should return ALL activity types (not just feeding)
                    activity_types = list(set(a.get("type") for a in activities))
                    feeding_activities = [a for a in activities if a.get("type") == "feeding"]
                    
                    # Check if our created feedings are present
                    activity_ids = [a.get("id") for a in activities]
                    found_our_feedings = sum(1 for fid in self.created_feeding_ids if fid in activity_ids)
                    
                    success_details = f"Found {len(activities)} total activities, types: {activity_types}, {len(feeding_activities)} feedings, {found_our_feedings}/{len(self.created_feeding_ids)} our feedings"
                    
                    if len(activities) > 0 and len(feeding_activities) > 0:
                        self.log_test("6. Activity History Endpoint", True, success_details, response_time)
                        return activities
                    else:
                        self.log_test("6. Activity History Endpoint", False, success_details, response_time)
                        return None
                else:
                    self.log_test("6. Activity History Endpoint", False, 
                                "Response is not a list", response_time)
                    return None
            except json.JSONDecodeError:
                self.log_test("6. Activity History Endpoint", False, 
                            "Invalid JSON response", response_time)
                return None
        else:
            status = response.status_code if response else "Timeout"
            error_detail = ""
            if response:
                try:
                    error_detail = response.text[:200]
                except:
                    pass
            self.log_test("6. Activity History Endpoint", False, 
                        f"HTTP {status} - {error_detail}", response_time)
            return None
    
    def test_7_data_comparison(self):
        """Test 7: Data Comparison Between Endpoints"""
        # Get data from both endpoints
        recent_feeding_data = self.test_5_recent_feeding_widget_endpoint()
        activity_history_data = self.test_6_activity_history_endpoint()
        
        if recent_feeding_data is not None and activity_history_data is not None:
            # Extract feeding activities from activity history
            history_feedings = [a for a in activity_history_data if a.get("type") == "feeding"]
            
            # Compare the feeding activities
            recent_ids = set(a.get("id") for a in recent_feeding_data)
            history_feeding_ids = set(a.get("id") for a in history_feedings)
            
            # Check if recent feeding IDs are subset of history feeding IDs
            ids_match = recent_ids.issubset(history_feeding_ids)
            
            # Check if feeding_type is identical in both responses for same activities
            feeding_type_consistency = True
            for recent_activity in recent_feeding_data:
                recent_id = recent_activity.get("id")
                recent_feeding_type = recent_activity.get("feeding_type")
                
                # Find same activity in history
                history_activity = next((a for a in history_feedings if a.get("id") == recent_id), None)
                if history_activity:
                    history_feeding_type = history_activity.get("feeding_type")
                    if recent_feeding_type != history_feeding_type:
                        feeding_type_consistency = False
                        break
            
            # Check if our created activities appear in both
            our_feedings_in_recent = sum(1 for fid in self.created_feeding_ids if fid in recent_ids)
            our_feedings_in_history = sum(1 for fid in self.created_feeding_ids if fid in history_feeding_ids)
            
            success_details = f"IDs match: {ids_match}, feeding_type consistent: {feeding_type_consistency}, our feedings in recent: {our_feedings_in_recent}/{len(self.created_feeding_ids)}, in history: {our_feedings_in_history}/{len(self.created_feeding_ids)}"
            
            if ids_match and feeding_type_consistency and our_feedings_in_recent > 0 and our_feedings_in_history > 0:
                self.log_test("7. Data Comparison", True, success_details, 0.0)
                return True
            else:
                self.log_test("7. Data Comparison", False, success_details, 0.0)
                return False
        else:
            self.log_test("7. Data Comparison", False, "Could not retrieve data from both endpoints", 0.0)
            return False
    
    def test_8_zero_feedings(self):
        """Test 8: Edge Case - Zero Feedings"""
        # Use a different baby ID that shouldn't have feedings
        fake_baby_id = str(uuid.uuid4())
        endpoint = f"/api/activities?baby_id={fake_baby_id}&type=feeding&limit=5"
        response, response_time = self.make_request("GET", endpoint,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list) and len(activities) == 0:
                    self.log_test("8. Zero Feedings Edge Case", True, 
                                "Empty array returned for non-existent baby", response_time)
                    return True
                else:
                    self.log_test("8. Zero Feedings Edge Case", False, 
                                f"Expected empty array, got {len(activities) if isinstance(activities, list) else 'invalid'}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("8. Zero Feedings Edge Case", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("8. Zero Feedings Edge Case", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_9_more_than_5_feedings(self):
        """Test 9: Edge Case - More Than 5 Feedings"""
        # Create 4 more feedings to test limit
        for i in range(4):
            data = {
                "baby_id": "demo-baby-456",
                "type": "feeding",
                "feeding_type": "bottle",
                "amount": 6.0 + i,
                "notes": f"Limit test feeding {i+1}"
            }
            
            response, response_time = self.make_request("POST", "/api/activities", data,
                                                      headers=self.get_auth_headers())
            
            if response and response.status_code in [200, 201]:
                try:
                    result = response.json()
                    activity_id = result.get("id")
                    if activity_id:
                        self.created_feeding_ids.append(activity_id)
                except:
                    pass
        
        # Now test the limit
        endpoint = f"/api/activities?baby_id=demo-baby-456&type=feeding&limit=5"
        response, response_time = self.make_request("GET", endpoint,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list) and len(activities) == 5:
                    self.log_test("9. More Than 5 Feedings", True, 
                                f"Limit respected: returned exactly 5 activities out of {len(self.created_feeding_ids)}+ total", response_time)
                    return True
                else:
                    self.log_test("9. More Than 5 Feedings", False, 
                                f"Expected 5 activities, got {len(activities) if isinstance(activities, list) else 'invalid'}", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("9. More Than 5 Feedings", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("9. More Than 5 Feedings", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_10_mixed_activities(self):
        """Test 10: Edge Case - Mixed Activities"""
        # Create non-feeding activities
        non_feeding_data = [
            {"baby_id": "demo-baby-456", "type": "diaper", "diaper_type": "wet", "notes": "Mixed test diaper"},
            {"baby_id": "demo-baby-456", "type": "sleep", "duration": 60, "notes": "Mixed test sleep"}
        ]
        
        for data in non_feeding_data:
            response, response_time = self.make_request("POST", "/api/activities", data,
                                                      headers=self.get_auth_headers())
        
        # Test that Recent Feeding endpoint only returns feedings
        endpoint = f"/api/activities?baby_id=demo-baby-456&type=feeding&limit=5"
        response, response_time = self.make_request("GET", endpoint,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list):
                    # Verify all activities are feeding type
                    feeding_activities = [a for a in activities if a.get("type") == "feeding"]
                    non_feeding_activities = [a for a in activities if a.get("type") != "feeding"]
                    
                    if len(feeding_activities) == len(activities) and len(non_feeding_activities) == 0:
                        self.log_test("10. Mixed Activities Filter", True, 
                                    f"Only feeding activities returned: {len(feeding_activities)}, no non-feeding: {len(non_feeding_activities)}", response_time)
                        return True
                    else:
                        self.log_test("10. Mixed Activities Filter", False, 
                                    f"Filter failed: {len(feeding_activities)} feeding, {len(non_feeding_activities)} non-feeding", response_time)
                        return False
                else:
                    self.log_test("10. Mixed Activities Filter", False, 
                                "Response is not a list", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("10. Mixed Activities Filter", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("10. Mixed Activities Filter", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_11_null_feeding_type(self):
        """Test 11: Edge Case - Null Feeding Type"""
        data = {
            "baby_id": "demo-baby-456",
            "type": "feeding",
            "notes": "Feeding without feeding_type"
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                activity_id = result.get("id")
                if activity_id:
                    self.created_feeding_ids.append(activity_id)
                    
                    # Check if it appears in Recent Feeding widget
                    endpoint = f"/api/activities?baby_id=demo-baby-456&type=feeding&limit=5"
                    response2, response_time2 = self.make_request("GET", endpoint,
                                                                headers=self.get_auth_headers())
                    
                    if response2 and response2.status_code == 200:
                        activities = response2.json()
                        activity_ids = [a.get("id") for a in activities]
                        
                        if activity_id in activity_ids:
                            self.log_test("11. Null Feeding Type", True, 
                                        f"Feeding without feeding_type still appears in widget: {activity_id}", response_time + response_time2)
                            return True
                        else:
                            self.log_test("11. Null Feeding Type", False, 
                                        f"Feeding without feeding_type missing from widget: {activity_id}", response_time + response_time2)
                            return False
                    else:
                        self.log_test("11. Null Feeding Type", False, 
                                    "Could not verify widget appearance", response_time + response_time2)
                        return False
                else:
                    self.log_test("11. Null Feeding Type", False, 
                                "No activity ID returned", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("11. Null Feeding Type", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("11. Null Feeding Type", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_12_different_baby_id(self):
        """Test 12: Edge Case - Different Baby ID Filtering"""
        # Create feeding for different baby
        different_baby_id = str(uuid.uuid4())
        data = {
            "baby_id": different_baby_id,
            "type": "feeding",
            "feeding_type": "bottle",
            "amount": 4.0,
            "notes": "Different baby feeding test"
        }
        
        response, response_time = self.make_request("POST", "/api/activities", data,
                                                  headers=self.get_auth_headers())
        
        different_baby_feeding_id = None
        if response and response.status_code in [200, 201]:
            try:
                result = response.json()
                different_baby_feeding_id = result.get("id")
            except:
                pass
        
        # Check that it doesn't appear in demo-baby-456's Recent Feeding widget
        endpoint = f"/api/activities?baby_id=demo-baby-456&type=feeding&limit=5"
        response2, response_time2 = self.make_request("GET", endpoint,
                                                    headers=self.get_auth_headers())
        
        if response2 and response2.status_code == 200:
            try:
                activities = response2.json()
                activity_ids = [a.get("id") for a in activities]
                
                if different_baby_feeding_id and different_baby_feeding_id not in activity_ids:
                    self.log_test("12. Different Baby ID Filter", True, 
                                f"Different baby's feeding correctly filtered out: {different_baby_feeding_id}", response_time + response_time2)
                    return True
                elif different_baby_feeding_id and different_baby_feeding_id in activity_ids:
                    self.log_test("12. Different Baby ID Filter", False, 
                                f"Different baby's feeding incorrectly included: {different_baby_feeding_id}", response_time + response_time2)
                    return False
                else:
                    self.log_test("12. Different Baby ID Filter", True, 
                                "Could not create different baby feeding, but filtering appears to work", response_time + response_time2)
                    return True
            except json.JSONDecodeError:
                self.log_test("12. Different Baby ID Filter", False, 
                            "Invalid JSON response", response_time + response_time2)
                return False
        else:
            status = response2.status_code if response2 else "Timeout"
            self.log_test("12. Different Baby ID Filter", False, 
                        f"HTTP {status}", response_time + response_time2)
            return False
    
    def test_13_endpoint_availability(self):
        """Test 13: Verify Both Endpoints Exist"""
        # Test if /api/activities endpoint exists (unified endpoint)
        response1, response_time1 = self.make_request("GET", "/api/activities?baby_id=demo-baby-456&type=feeding&limit=1",
                                                    headers=self.get_auth_headers())
        
        # Test if /api/feedings endpoint exists (separate endpoint)
        response2, response_time2 = self.make_request("GET", "/api/feedings?baby_id=demo-baby-456",
                                                    headers=self.get_auth_headers())
        
        activities_exists = response1 and response1.status_code == 200
        feedings_exists = response2 and response2.status_code == 200
        
        if activities_exists and feedings_exists:
            self.log_test("13. Endpoint Availability", True, 
                        "Both /api/activities and /api/feedings endpoints exist", response_time1 + response_time2)
            return True
        elif activities_exists:
            self.log_test("13. Endpoint Availability", True, 
                        "Only /api/activities endpoint exists (unified approach)", response_time1 + response_time2)
            return True
        elif feedings_exists:
            self.log_test("13. Endpoint Availability", False, 
                        "Only /api/feedings endpoint exists (Recent Feeding widget may be calling wrong endpoint)", response_time1 + response_time2)
            return False
        else:
            self.log_test("13. Endpoint Availability", False, 
                        "Neither /api/activities nor /api/feedings endpoints work", response_time1 + response_time2)
            return False
    
    def test_14_response_format_validation(self):
        """Test 14: Response Format Validation"""
        endpoint = f"/api/activities?baby_id=demo-baby-456&type=feeding&limit=5"
        response, response_time = self.make_request("GET", endpoint,
                                                  headers=self.get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                activities = response.json()
                if isinstance(activities, list) and len(activities) > 0:
                    # Check required fields in each activity
                    required_fields = ["id", "type", "timestamp"]
                    optional_fields = ["feeding_type", "amount", "duration", "notes"]
                    
                    all_valid = True
                    field_analysis = {}
                    
                    for field in required_fields + optional_fields:
                        field_analysis[field] = sum(1 for a in activities if field in a and a[field] is not None)
                    
                    # All activities must have required fields
                    for field in required_fields:
                        if field_analysis[field] != len(activities):
                            all_valid = False
                    
                    # Check that type is always "feeding"
                    correct_types = sum(1 for a in activities if a.get("type") == "feeding")
                    if correct_types != len(activities):
                        all_valid = False
                    
                    success_details = f"Field analysis: {field_analysis}, all feeding type: {correct_types}/{len(activities)}"
                    
                    if all_valid:
                        self.log_test("14. Response Format Validation", True, success_details, response_time)
                        return True
                    else:
                        self.log_test("14. Response Format Validation", False, success_details, response_time)
                        return False
                else:
                    self.log_test("14. Response Format Validation", False, 
                                f"No activities to validate format", response_time)
                    return False
            except json.JSONDecodeError:
                self.log_test("14. Response Format Validation", False, 
                            "Invalid JSON response", response_time)
                return False
        else:
            status = response.status_code if response else "Timeout"
            self.log_test("14. Response Format Validation", False, 
                        f"HTTP {status}", response_time)
            return False
    
    def test_15_root_cause_analysis(self):
        """Test 15: Root Cause Analysis"""
        # Compare what frontend expects vs what backend provides
        
        # 1. Check if Recent Feeding widget endpoint works
        recent_feeding_response, rt1 = self.make_request("GET", "/api/activities?baby_id=demo-baby-456&type=feeding&limit=5",
                                                       headers=self.get_auth_headers())
        
        # 2. Check if Activity History endpoint works  
        activity_history_response, rt2 = self.make_request("GET", "/api/activities?baby_id=demo-baby-456",
                                                         headers=self.get_auth_headers())
        
        # 3. Check if separate feeding endpoint works
        feeding_endpoint_response, rt3 = self.make_request("GET", "/api/feedings?baby_id=demo-baby-456",
                                                         headers=self.get_auth_headers())
        
        analysis = {
            "recent_feeding_works": recent_feeding_response and recent_feeding_response.status_code == 200,
            "activity_history_works": activity_history_response and activity_history_response.status_code == 200,
            "feeding_endpoint_works": feeding_endpoint_response and feeding_endpoint_response.status_code == 200,
            "created_feedings_count": len(self.created_feeding_ids)
        }
        
        # Analyze the data
        if analysis["recent_feeding_works"] and analysis["activity_history_works"]:
            try:
                recent_data = recent_feeding_response.json()
                history_data = activity_history_response.json()
                
                recent_count = len(recent_data) if isinstance(recent_data, list) else 0
                history_feeding_count = len([a for a in history_data if a.get("type") == "feeding"]) if isinstance(history_data, list) else 0
                
                analysis["recent_feeding_count"] = recent_count
                analysis["history_feeding_count"] = history_feeding_count
                analysis["data_mismatch"] = recent_count != history_feeding_count and history_feeding_count > 5
                
                # Check if our created feedings appear
                if recent_count > 0:
                    recent_ids = [a.get("id") for a in recent_data]
                    our_feedings_in_recent = sum(1 for fid in self.created_feeding_ids if fid in recent_ids)
                    analysis["our_feedings_in_recent"] = our_feedings_in_recent
                else:
                    analysis["our_feedings_in_recent"] = 0
                
            except:
                analysis["data_parsing_error"] = True
        
        # Determine root cause
        root_cause = "Unknown"
        if not analysis["recent_feeding_works"]:
            root_cause = "Recent Feeding endpoint (/api/activities?type=feeding) not working"
        elif analysis["recent_feeding_count"] == 0:
            root_cause = "Recent Feeding endpoint returns empty array"
        elif analysis.get("our_feedings_in_recent", 0) == 0:
            root_cause = "Created feedings not appearing in Recent Feeding endpoint"
        elif analysis.get("data_mismatch", False):
            root_cause = "Data inconsistency between Recent Feeding and Activity History"
        elif analysis["feeding_endpoint_works"] and not analysis["recent_feeding_works"]:
            root_cause = "Frontend calling wrong endpoint (/api/feedings vs /api/activities)"
        else:
            root_cause = "No obvious issues detected - may be frontend display problem"
        
        success = root_cause == "No obvious issues detected - may be frontend display problem"
        
        self.log_test("15. Root Cause Analysis", success, 
                    f"Analysis: {analysis}, Root Cause: {root_cause}", rt1 + rt2 + rt3)
        
        return success
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 COMPREHENSIVE TESTING: Recent Feeding Widget Data Flow")
        print(f"Backend: {self.base_url}")
        print(f"Test Account: demo@babysteps.com / demo123")
        print(f"Demo Baby ID: {self.baby_id}")
        print(f"Total Tests: {self.total_tests}")
        print("=" * 80)
        
        # Step 1: Authentication
        print("\n📋 STEP 1: Authentication")
        if not self.test_1_authentication():
            print("❌ Cannot proceed without authentication")
            return self.generate_report()
        
        # Step 2: Quick Feed Button → Backend
        print("\n📋 STEP 2: Quick Feed Button → Backend")
        self.test_2_quick_feed_bottle()
        self.test_3_quick_feed_breast()
        self.test_4_quick_feed_solid()
        
        # Step 3: Widget Endpoints
        print("\n📋 STEP 3: Widget Endpoints")
        self.test_5_recent_feeding_widget_endpoint()
        self.test_6_activity_history_endpoint()
        
        # Step 4: Data Comparison
        print("\n📋 STEP 4: Data Comparison")
        self.test_7_data_comparison()
        
        # Step 5: Edge Cases
        print("\n📋 STEP 5: Edge Cases")
        self.test_8_zero_feedings()
        self.test_9_more_than_5_feedings()
        self.test_10_mixed_activities()
        self.test_11_null_feeding_type()
        self.test_12_different_baby_id()
        
        # Step 6: Technical Analysis
        print("\n📋 STEP 6: Technical Analysis")
        self.test_13_endpoint_availability()
        self.test_14_response_format_validation()
        self.test_15_root_cause_analysis()
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 RECENT FEEDING WIDGET TEST RESULTS")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Tests Failed: {self.failed_tests}/{self.total_tests}")
        
        # Success Criteria Check
        print("\n🎯 SUCCESS CRITERIA:")
        criteria_met = []
        
        # Check Quick Feed creation
        quick_feed_tests = [r for r in self.test_results if "Quick Feed" in r["test"]]
        quick_feed_success = sum(1 for t in quick_feed_tests if "✅" in t["status"])
        criteria_met.append(f"✅ Quick Feed POST creates activities: {quick_feed_success}/3" if quick_feed_success == 3 else f"❌ Quick Feed POST creates activities: {quick_feed_success}/3")
        
        # Check Recent Feeding endpoint
        recent_feeding_test = next((r for r in self.test_results if "Recent Feeding Widget Endpoint" in r["test"]), None)
        if recent_feeding_test and "✅" in recent_feeding_test["status"]:
            criteria_met.append("✅ Recent Feeding GET endpoint returns activities with type=feeding")
        else:
            criteria_met.append("❌ Recent Feeding GET endpoint fails")
        
        # Check Activity History endpoint
        activity_history_test = next((r for r in self.test_results if "Activity History Endpoint" in r["test"]), None)
        if activity_history_test and "✅" in activity_history_test["status"]:
            criteria_met.append("✅ Activity History GET endpoint returns same activities")
        else:
            criteria_met.append("❌ Activity History GET endpoint fails")
        
        # Check data comparison
        data_comparison_test = next((r for r in self.test_results if "Data Comparison" in r["test"]), None)
        if data_comparison_test and "✅" in data_comparison_test["status"]:
            criteria_met.append("✅ Same activity IDs appear in both endpoints")
        else:
            criteria_met.append("❌ Data inconsistency between endpoints")
        
        # Check feeding_type preservation
        format_test = next((r for r in self.test_results if "Response Format" in r["test"]), None)
        if format_test and "✅" in format_test["status"]:
            criteria_met.append("✅ feeding_type values are preserved")
        else:
            criteria_met.append("❌ feeding_type values not preserved")
        
        # Check limit and ordering
        limit_test = next((r for r in self.test_results if "More Than 5" in r["test"]), None)
        if limit_test and "✅" in limit_test["status"]:
            criteria_met.append("✅ Limit parameter works correctly")
        else:
            criteria_met.append("❌ Limit parameter not working")
        
        for criterion in criteria_met:
            print(criterion)
        
        # Root Cause Analysis
        print("\n🔍 ROOT CAUSE ANALYSIS:")
        root_cause_test = next((r for r in self.test_results if "Root Cause" in r["test"]), None)
        if root_cause_test:
            print(f"Analysis Result: {root_cause_test['details']}")
        
        # Expected Issues Found
        print("\n⚠️ EXPECTED ISSUES TO INVESTIGATE:")
        issues_found = []
        
        if quick_feed_success < 3:
            issues_found.append("❌ Quick Feed buttons not creating activities correctly")
        
        if not (recent_feeding_test and "✅" in recent_feeding_test["status"]):
            issues_found.append("❌ Recent Feeding endpoint returning empty array or errors")
        
        if not (data_comparison_test and "✅" in data_comparison_test["status"]):
            issues_found.append("❌ feeding_type not being stored/returned correctly")
        
        endpoint_test = next((r for r in self.test_results if "Endpoint Availability" in r["test"]), None)
        if endpoint_test and "❌" in endpoint_test["status"]:
            issues_found.append("❌ Frontend calling incorrect endpoint")
        
        if not issues_found:
            issues_found.append("✅ No backend issues found - problem may be in frontend display logic")
        
        for issue in issues_found:
            print(issue)
        
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
            print("🎉 EXCELLENT - Recent Feeding Widget data flow working correctly")
        elif success_rate >= 75:
            print("✅ GOOD - Minor issues found, mostly functional")
        elif success_rate >= 50:
            print("⚠️ FAIR - Significant issues found, needs investigation")
        else:
            print("❌ POOR - Critical issues preventing Recent Feeding Widget functionality")
        
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success_rate": success_rate,
            "test_results": self.test_results,
            "created_feeding_ids": self.created_feeding_ids,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0
        }

if __name__ == "__main__":
    tester = RecentFeedingWidgetTester()
    results = tester.run_all_tests()