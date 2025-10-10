#!/usr/bin/env python3
"""
Demo User and Baby Data Test
Focused test to check if demo user and baby data exist in the backend
"""

import requests
import json
from datetime import datetime, timezone

class DemoUserTester:
    def __init__(self):
        self.frontend_url = "https://smart-parent.preview.emergentagent.com"
        self.backend_url = "https://smart-parent.preview.emergentagent.com/api"
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
            response = requests.get(f"{self.backend_url}/health", timeout=30)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Backend Health", True, f"Backend healthy: {data.get('service', 'Unknown')}")
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
            
            response = requests.post(f"{self.backend_url}/auth/login", json=login_data, timeout=30)
            
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
    
    def test_demo_baby_exists(self, auth_token):
        """Test if demo baby exists"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.get(f"{self.backend_url}/babies", headers=headers, timeout=30)
            
            if response.status_code == 200:
                babies = response.json()
                if isinstance(babies, list):
                    if len(babies) > 0:
                        demo_baby = babies[0]
                        baby_name = demo_baby.get('name', 'Unknown')
                        baby_id = demo_baby.get('id', 'Unknown')
                        birth_date = demo_baby.get('birth_date', 'Unknown')
                        self.log_result("Demo Baby Exists", True, f"Found baby: {baby_name} (ID: {baby_id}, Birth: {birth_date})")
                        return demo_baby
                    else:
                        self.log_result("Demo Baby Exists", False, "No babies found in database")
                        return None
                else:
                    self.log_result("Demo Baby Exists", False, f"Invalid response format: {babies}")
                    return None
            else:
                self.log_result("Demo Baby Exists", False, f"HTTP {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_result("Demo Baby Exists", False, f"Error: {str(e)}")
            return None
    
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
            response = requests.post(f"{self.backend_url}/babies", json=baby_data, headers=headers, timeout=30)
            
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
    
    def test_demo_activities_exist(self, auth_token, baby_id):
        """Test if demo activities exist"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            
            # Check feedings
            response = requests.get(f"{self.backend_url}/feedings?baby_id={baby_id}", headers=headers, timeout=30)
            feedings_count = 0
            if response.status_code == 200:
                feedings = response.json()
                feedings_count = len(feedings) if isinstance(feedings, list) else 0
            
            # Check diapers
            response = requests.get(f"{self.backend_url}/diapers?baby_id={baby_id}", headers=headers, timeout=30)
            diapers_count = 0
            if response.status_code == 200:
                diapers = response.json()
                diapers_count = len(diapers) if isinstance(diapers, list) else 0
            
            # Check sleep
            response = requests.get(f"{self.backend_url}/sleep?baby_id={baby_id}", headers=headers, timeout=30)
            sleep_count = 0
            if response.status_code == 200:
                sleep_sessions = response.json()
                sleep_count = len(sleep_sessions) if isinstance(sleep_sessions, list) else 0
            
            total_activities = feedings_count + diapers_count + sleep_count
            
            if total_activities > 0:
                self.log_result("Demo Activities Exist", True, f"Found {total_activities} activities (Feedings: {feedings_count}, Diapers: {diapers_count}, Sleep: {sleep_count})")
                return True
            else:
                self.log_result("Demo Activities Exist", False, "No demo activities found")
                return False
                
        except Exception as e:
            self.log_result("Demo Activities Exist", False, f"Error: {str(e)}")
            return False
    
    def create_demo_activities(self, auth_token, baby_id):
        """Create demo activities"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            activities_created = 0
            
            # Create demo feeding
            feeding_data = {
                "baby_id": baby_id,
                "type": "bottle",
                "amount": 4.0,
                "notes": "Demo feeding"
            }
            response = requests.post(f"{self.backend_url}/feedings", json=feeding_data, headers=headers, timeout=30)
            if response.status_code == 200:
                activities_created += 1
            
            # Create demo diaper
            diaper_data = {
                "baby_id": baby_id,
                "type": "wet",
                "notes": "Demo diaper change"
            }
            response = requests.post(f"{self.backend_url}/diapers", json=diaper_data, headers=headers, timeout=30)
            if response.status_code == 200:
                activities_created += 1
            
            # Create demo sleep
            sleep_data = {
                "baby_id": baby_id,
                "start_time": "2024-12-19T14:00:00Z",
                "end_time": "2024-12-19T16:00:00Z",
                "notes": "Demo nap"
            }
            response = requests.post(f"{self.backend_url}/sleep", json=sleep_data, headers=headers, timeout=30)
            if response.status_code == 200:
                activities_created += 1
            
            if activities_created > 0:
                self.log_result("Create Demo Activities", True, f"Created {activities_created} demo activities")
                return True
            else:
                self.log_result("Create Demo Activities", False, "Failed to create demo activities")
                return False
                
        except Exception as e:
            self.log_result("Create Demo Activities", False, f"Error: {str(e)}")
            return False
    
    def run_demo_setup(self):
        """Run demo user and baby setup"""
        print("🔧 DEMO USER AND BABY DATA SETUP")
        print("=" * 80)
        print("Checking and setting up demo user with baby data")
        print("=" * 80)
        
        # 1. Test backend health
        print("\n1. BACKEND HEALTH CHECK:")
        print("-" * 40)
        if not self.test_backend_health():
            print("❌ Backend not healthy, cannot proceed")
            return self.results
        
        # 2. Test demo user login
        print("\n2. DEMO USER LOGIN:")
        print("-" * 40)
        auth_token = self.test_demo_user_login()
        if not auth_token:
            print("❌ Demo user login failed, cannot proceed")
            return self.results
        
        # 3. Check if demo baby exists
        print("\n3. DEMO BABY CHECK:")
        print("-" * 40)
        demo_baby = self.test_demo_baby_exists(auth_token)
        if not demo_baby:
            print("⚠️ No demo baby found, creating one...")
            demo_baby = self.create_demo_baby_if_missing(auth_token)
            if not demo_baby:
                print("❌ Failed to create demo baby")
                return self.results
        
        baby_id = demo_baby.get('id')
        if not baby_id:
            print("❌ Demo baby has no ID")
            return self.results
        
        # 4. Check demo activities
        print("\n4. DEMO ACTIVITIES CHECK:")
        print("-" * 40)
        activities_exist = self.test_demo_activities_exist(auth_token, baby_id)
        if not activities_exist:
            print("⚠️ No demo activities found, creating some...")
            self.create_demo_activities(auth_token, baby_id)
        
        # Print summary
        print("\n" + "=" * 80)
        print("🔧 DEMO SETUP SUMMARY:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🚨 ISSUES FOUND:")
            for error in self.results['errors']:
                print(f"   • {error}")
        else:
            print(f"\n🎉 DEMO SETUP COMPLETE:")
            print(f"   • Demo user: {self.demo_email}")
            print(f"   • Demo baby: {demo_baby.get('name', 'Unknown')} (ID: {baby_id})")
            print(f"   • Backend URL: {self.backend_url}")
        
        return self.results

def main():
    """Main demo setup execution"""
    tester = DemoUserTester()
    results = tester.run_demo_setup()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()