#!/usr/bin/env python3
"""
Local Backend Test for Baby Data Investigation
Tests the local backend to understand the baby data loading issue
"""

import requests
import json
from datetime import datetime, timezone
import os

class LocalBackendTester:
    def __init__(self):
        # Use local backend URL
        self.backend_url = "http://localhost:8001/api"
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
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
    
    def test_backend_health(self):
        """Test backend health"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Backend Health", True, f"Local backend healthy: {data.get('service', 'Unknown')}")
                return True
            else:
                self.log_result("Backend Health", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Backend Health", False, f"Error: {str(e)}")
            return False
    
    def test_demo_user_login(self):
        """Test demo user login"""
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            response = requests.post(f"{self.backend_url}/auth/login", json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.log_result("Demo User Login", True, "Demo user login successful")
                    return data['access_token']
                else:
                    self.log_result("Demo User Login", False, f"No access token: {data}")
                    return None
            else:
                self.log_result("Demo User Login", False, f"HTTP {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_result("Demo User Login", False, f"Error: {str(e)}")
            return None
    
    def test_demo_baby_data(self, auth_token):
        """Test demo baby data"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.get(f"{self.backend_url}/babies", headers=headers, timeout=10)
            
            if response.status_code == 200:
                babies = response.json()
                if isinstance(babies, list):
                    if len(babies) > 0:
                        demo_baby = babies[0]
                        baby_name = demo_baby.get('name', 'Unknown')
                        baby_id = demo_baby.get('id', 'Unknown')
                        birth_date = demo_baby.get('birth_date', 'Unknown')
                        gender = demo_baby.get('gender', 'Unknown')
                        
                        print(f"📋 Demo Baby Details:")
                        print(f"   Name: {baby_name}")
                        print(f"   ID: {baby_id}")
                        print(f"   Birth Date: {birth_date}")
                        print(f"   Gender: {gender}")
                        
                        self.log_result("Demo Baby Data", True, f"Found baby: {baby_name}")
                        return demo_baby
                    else:
                        self.log_result("Demo Baby Data", False, "No babies found")
                        return None
                else:
                    self.log_result("Demo Baby Data", False, f"Invalid response: {babies}")
                    return None
            else:
                self.log_result("Demo Baby Data", False, f"HTTP {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_result("Demo Baby Data", False, f"Error: {str(e)}")
            return None
    
    def test_baby_activities(self, auth_token, baby_id):
        """Test baby activities"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            
            # Test different activity endpoints
            endpoints = [
                ("feedings", "Feedings"),
                ("diapers", "Diapers"),
                ("sleep", "Sleep"),
                ("pumping", "Pumping"),
                ("measurements", "Measurements"),
                ("milestones", "Milestones")
            ]
            
            total_activities = 0
            for endpoint, name in endpoints:
                try:
                    response = requests.get(f"{self.backend_url}/{endpoint}?baby_id={baby_id}", headers=headers, timeout=10)
                    if response.status_code == 200:
                        activities = response.json()
                        count = len(activities) if isinstance(activities, list) else 0
                        total_activities += count
                        print(f"   {name}: {count} records")
                    else:
                        print(f"   {name}: HTTP {response.status_code}")
                except Exception as e:
                    print(f"   {name}: Error - {str(e)}")
            
            if total_activities > 0:
                self.log_result("Baby Activities", True, f"Found {total_activities} total activities")
                return True
            else:
                self.log_result("Baby Activities", False, "No activities found")
                return False
                
        except Exception as e:
            self.log_result("Baby Activities", False, f"Error: {str(e)}")
            return False
    
    def test_ai_endpoints(self, auth_token):
        """Test AI endpoints"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            
            # Test food research
            food_query = {
                "question": "Is banana safe for babies?",
                "baby_age_months": 6
            }
            response = requests.post(f"{self.backend_url}/food/research", json=food_query, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Food Research AI", True, f"Safety level: {data.get('safety_level', 'Unknown')}")
            else:
                self.log_result("Food Research AI", False, f"HTTP {response.status_code}")
            
            # Test meal search
            meal_query = {
                "query": "breakfast ideas for 6 month old",
                "baby_age_months": 6
            }
            response = requests.post(f"{self.backend_url}/meals/search", json=meal_query, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Meal Search AI", True, "Meal search working")
            else:
                self.log_result("Meal Search AI", False, f"HTTP {response.status_code}")
            
            # Test general research
            research_query = {
                "question": "How often should I feed my baby?"
            }
            response = requests.post(f"{self.backend_url}/research", json=research_query, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                self.log_result("General Research AI", True, "Research endpoint working")
            else:
                self.log_result("General Research AI", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("AI Endpoints", False, f"Error: {str(e)}")
    
    def create_demo_baby_if_missing(self, auth_token):
        """Create demo baby if missing"""
        try:
            baby_data = {
                "name": "Emma",
                "birth_date": "2024-06-15T10:30:00Z",
                "birth_weight": 7.2,
                "birth_length": 20.5,
                "gender": "female"
            }
            
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.post(f"{self.backend_url}/babies", json=baby_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                baby_name = data.get('name', 'Unknown')
                baby_id = data.get('id', 'Unknown')
                self.log_result("Create Demo Baby", True, f"Created baby: {baby_name} (ID: {baby_id})")
                return data
            else:
                self.log_result("Create Demo Baby", False, f"HTTP {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_result("Create Demo Baby", False, f"Error: {str(e)}")
            return None
    
    def run_investigation(self):
        """Run local backend investigation"""
        print("🔍 LOCAL BACKEND INVESTIGATION FOR BABY DATA ISSUE")
        print("=" * 80)
        print("Testing local backend to understand baby data loading issue")
        print(f"Backend URL: {self.backend_url}")
        print("=" * 80)
        
        # 1. Test backend health
        print("\n1. BACKEND HEALTH:")
        print("-" * 40)
        if not self.test_backend_health():
            print("❌ Local backend not healthy")
            return self.results
        
        # 2. Test demo user login
        print("\n2. DEMO USER LOGIN:")
        print("-" * 40)
        auth_token = self.test_demo_user_login()
        if not auth_token:
            print("❌ Demo user login failed")
            return self.results
        
        # 3. Test demo baby data
        print("\n3. DEMO BABY DATA:")
        print("-" * 40)
        demo_baby = self.test_demo_baby_data(auth_token)
        if not demo_baby:
            print("⚠️ No demo baby found, creating one...")
            demo_baby = self.create_demo_baby_if_missing(auth_token)
            if not demo_baby:
                print("❌ Failed to create demo baby")
                return self.results
        
        baby_id = demo_baby.get('id')
        
        # 4. Test baby activities
        print("\n4. BABY ACTIVITIES:")
        print("-" * 40)
        print(f"📊 Activity counts for baby {demo_baby.get('name', 'Unknown')}:")
        self.test_baby_activities(auth_token, baby_id)
        
        # 5. Test AI endpoints
        print("\n5. AI ENDPOINTS:")
        print("-" * 40)
        self.test_ai_endpoints(auth_token)
        
        # Print summary
        print("\n" + "=" * 80)
        print("🔍 LOCAL BACKEND INVESTIGATION SUMMARY:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🚨 ISSUES FOUND:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Analysis for baby data issue
        print(f"\n🎯 BABY DATA LOADING ANALYSIS:")
        print("-" * 40)
        
        if demo_baby:
            print("✅ BACKEND STATUS: Demo baby data exists in backend")
            print(f"   • Baby Name: {demo_baby.get('name', 'Unknown')}")
            print(f"   • Baby ID: {demo_baby.get('id', 'Unknown')}")
            print(f"   • Birth Date: {demo_baby.get('birth_date', 'Unknown')}")
            print("")
            print("🔧 NEXT STEPS FOR FRONTEND INVESTIGATION:")
            print("   1. Check if frontend is using correct backend URL")
            print("   2. Verify localStorage baby data structure")
            print("   3. Check currentBaby state in App.js")
            print("   4. Verify baby data binding in TrackingPage component")
            print("")
            print("💡 LIKELY ISSUE: Frontend not loading baby data into currentBaby state")
            print("   - Backend has the data ✅")
            print("   - Frontend may have data binding or state management issue ❌")
        else:
            print("❌ BACKEND STATUS: No demo baby data found")
            print("🔧 RECOMMENDATION: Create demo baby data first")
        
        return self.results

def main():
    """Main investigation execution"""
    tester = LocalBackendTester()
    results = tester.run_investigation()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()