#!/usr/bin/env python3
"""
Baby Data Debug Test - Focused on localStorage and currentBaby issue
This test simulates the frontend localStorage operations to debug the baby data loading issue
"""

import json
import uuid
from datetime import datetime

class BabyDataDebugger:
    def __init__(self):
        # Simulate localStorage
        self.localStorage = {}
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
    
    def simulate_localStorage_setItem(self, key, value):
        """Simulate localStorage.setItem"""
        self.localStorage[key] = str(value)
    
    def simulate_localStorage_getItem(self, key):
        """Simulate localStorage.getItem"""
        return self.localStorage.get(key)
    
    def simulate_demo_data_initialization(self):
        """Simulate the demo data initialization from offlineMode.js"""
        try:
            # Check if users exist
            users_data = self.simulate_localStorage_getItem('babysteps_offline_users')
            users = json.loads(users_data) if users_data else {}
            
            if len(users) == 0:
                # Create demo user (simulating offlineMode.js line 49-56)
                demo_user_id = str(uuid.uuid4())
                users['demo@babysteps.com'] = {
                    'id': demo_user_id,
                    'email': 'demo@babysteps.com',
                    'name': 'Demo Parent',
                    'password': 'demo123',
                    'createdAt': datetime.now().isoformat()
                }
                self.simulate_localStorage_setItem('babysteps_offline_users', json.dumps(users))
                
                # Create demo baby (simulating offlineMode.js line 60-72)
                demo_baby = {
                    'id': str(uuid.uuid4()),
                    'name': 'Emma',
                    'birth_date': '2024-01-15',
                    'gender': 'girl',
                    'profile_image': None,
                    'user_id': demo_user_id,
                    'createdAt': datetime.now().isoformat()
                }
                
                # Store babies by user ID (simulating offlineMode.js line 71-72)
                babies = {}
                babies[demo_user_id] = [demo_baby]
                self.simulate_localStorage_setItem('babysteps_offline_babies', json.dumps(babies))
                
                # Create demo activities (simulating offlineMode.js line 75-104)
                activities = {}
                demo_activities = [
                    {
                        'id': str(uuid.uuid4()),
                        'type': 'feeding',
                        'notes': 'Formula feeding - 4oz',
                        'baby_id': demo_baby['id'],
                        'user_id': demo_user_id,
                        'timestamp': datetime.now().isoformat()
                    }
                ]
                activities[demo_user_id] = demo_activities
                self.simulate_localStorage_setItem('babysteps_offline_activities', json.dumps(activities))
                
                self.log_result("Demo Data Initialization", True, f"Created demo user: {demo_user_id}")
                return demo_user_id, demo_baby
            else:
                # Users already exist
                demo_user = users.get('demo@babysteps.com')
                if demo_user:
                    demo_user_id = demo_user['id']
                    
                    # Get babies for this user
                    babies_data = self.simulate_localStorage_getItem('babysteps_offline_babies')
                    babies = json.loads(babies_data) if babies_data else {}
                    user_babies = babies.get(demo_user_id, [])
                    
                    if user_babies:
                        self.log_result("Demo Data Initialization", True, f"Demo data already exists for user: {demo_user_id}")
                        return demo_user_id, user_babies[0]
                    else:
                        self.log_result("Demo Data Initialization", False, f"Demo user exists but no babies found for user: {demo_user_id}")
                        return demo_user_id, None
                else:
                    self.log_result("Demo Data Initialization", False, "Demo user not found in existing users")
                    return None, None
                    
        except Exception as e:
            self.log_result("Demo Data Initialization", False, f"Error: {str(e)}")
            return None, None
    
    def simulate_demo_login(self):
        """Simulate demo user login process"""
        try:
            email = 'demo@babysteps.com'
            password = 'demo123'
            
            # Get users (simulating offlineMode.js line 124)
            users_data = self.simulate_localStorage_getItem('babysteps_offline_users')
            users = json.loads(users_data) if users_data else {}
            
            email_key = email.lower().strip()
            user = users.get(email_key)
            
            if not user or user['password'] != password:
                self.log_result("Demo Login", False, "Invalid credentials")
                return None
            
            # Set current user (simulating offlineMode.js line 139)
            self.simulate_localStorage_setItem('babysteps_current_user', user['id'])
            
            # Generate token (simulating offlineMode.js line 142)
            token = f"standalone_token_{user['id']}_{int(datetime.now().timestamp())}"
            
            self.log_result("Demo Login", True, f"Login successful for user: {user['id']}")
            return user['id'], token
            
        except Exception as e:
            self.log_result("Demo Login", False, f"Error: {str(e)}")
            return None, None
    
    def simulate_getBabies(self):
        """Simulate getBabies function from offlineMode.js"""
        try:
            # Get current user ID (simulating offlineMode.js line 247)
            current_user_id = self.simulate_localStorage_getItem('babysteps_current_user')
            
            if not current_user_id:
                self.log_result("Get Babies", False, "No current user ID found")
                return []
            
            # Get babies data (simulating offlineMode.js line 248)
            babies_data = self.simulate_localStorage_getItem('babysteps_offline_babies')
            babies = json.loads(babies_data) if babies_data else {}
            
            # Get babies for current user (simulating offlineMode.js line 251)
            user_babies = babies.get(current_user_id, [])
            
            self.log_result("Get Babies", True, f"Found {len(user_babies)} babies for user {current_user_id}")
            return user_babies
            
        except Exception as e:
            self.log_result("Get Babies", False, f"Error: {str(e)}")
            return []
    
    def debug_localStorage_structure(self):
        """Debug the localStorage structure"""
        print("\n🔍 LOCALSTORAGE DEBUG:")
        print("-" * 40)
        
        for key, value in self.localStorage.items():
            print(f"Key: {key}")
            try:
                parsed_value = json.loads(value)
                if isinstance(parsed_value, dict):
                    print(f"  Type: dict with {len(parsed_value)} keys")
                    for k, v in parsed_value.items():
                        if isinstance(v, list):
                            print(f"    {k}: list with {len(v)} items")
                        elif isinstance(v, dict):
                            print(f"    {k}: dict with {len(v)} keys")
                        else:
                            print(f"    {k}: {type(v).__name__}")
                elif isinstance(parsed_value, list):
                    print(f"  Type: list with {len(parsed_value)} items")
                else:
                    print(f"  Type: {type(parsed_value).__name__}")
            except:
                print(f"  Value: {value[:100]}...")
            print()
    
    def run_debug_investigation(self):
        """Run comprehensive baby data debug investigation"""
        print("🔍 BABY DATA DEBUG INVESTIGATION")
        print("=" * 80)
        print("Simulating frontend localStorage operations to debug currentBaby issue")
        print("=" * 80)
        
        # 1. Initialize demo data
        print("\n1. DEMO DATA INITIALIZATION:")
        print("-" * 40)
        demo_user_id, demo_baby = self.simulate_demo_data_initialization()
        
        # 2. Debug localStorage structure after initialization
        self.debug_localStorage_structure()
        
        # 3. Simulate login
        print("\n2. DEMO LOGIN SIMULATION:")
        print("-" * 40)
        logged_in_user_id, token = self.simulate_demo_login()
        
        # 4. Check if user IDs match
        print("\n3. USER ID VERIFICATION:")
        print("-" * 40)
        if demo_user_id and logged_in_user_id:
            if demo_user_id == logged_in_user_id:
                self.log_result("User ID Match", True, f"Demo user ID matches login user ID: {demo_user_id}")
            else:
                self.log_result("User ID Match", False, f"Demo user ID ({demo_user_id}) != Login user ID ({logged_in_user_id})")
        
        # 5. Simulate getBabies
        print("\n4. GET BABIES SIMULATION:")
        print("-" * 40)
        babies = self.simulate_getBabies()
        
        if babies:
            print(f"📋 Babies found:")
            for baby in babies:
                print(f"   Name: {baby.get('name', 'Unknown')}")
                print(f"   ID: {baby.get('id', 'Unknown')}")
                print(f"   User ID: {baby.get('user_id', 'Unknown')}")
                print(f"   Birth Date: {baby.get('birth_date', 'Unknown')}")
        
        # 6. Check current user in localStorage
        print("\n5. CURRENT USER CHECK:")
        print("-" * 40)
        current_user = self.simulate_localStorage_getItem('babysteps_current_user')
        print(f"Current user in localStorage: {current_user}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("🔍 DEBUG INVESTIGATION SUMMARY:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🚨 ISSUES FOUND:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Root cause analysis
        print(f"\n🎯 ROOT CAUSE ANALYSIS:")
        print("-" * 40)
        
        if len(babies) > 0:
            print("✅ Demo baby data exists in localStorage")
            print("✅ getBabies() function would return baby data")
            print("🔧 LIKELY ISSUE: Frontend App.js not calling fetchBabies() properly")
            print("   OR currentBaby state not being set after fetchBabies() succeeds")
        else:
            print("❌ No baby data found - this explains 'No Baby Selected'")
            print("🔧 LIKELY ISSUE: Demo data initialization or user ID mismatch")
        
        if current_user:
            print(f"✅ Current user is set: {current_user}")
        else:
            print("❌ No current user set - authentication issue")
        
        return self.results

def main():
    """Main debug execution"""
    debugger = BabyDataDebugger()
    results = debugger.run_debug_investigation()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()