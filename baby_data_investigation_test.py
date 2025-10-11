#!/usr/bin/env python3
"""
Baby Data Loading Investigation Test
Focused test to investigate the critical baby data loading issue where currentBaby is null/undefined
causing TrackingPage to show "No Baby Selected" instead of the main interface.
"""

import requests
import json
import time
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class BabyDataInvestigationTester:
    def __init__(self):
        self.frontend_url = "https://baby-genius.preview.emergentagent.com"
        self.backend_url = "https://baby-genius.preview.emergentagent.com/api"
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.driver = None
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
    
    def setup_driver(self):
        """Setup Chrome driver for testing"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            print(f"❌ Failed to setup Chrome driver: {str(e)}")
            return False
    
    def test_backend_demo_user_exists(self):
        """Test if demo user exists in backend database"""
        try:
            # Try to login with demo credentials
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            response = requests.post(f"{self.backend_url}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.log_result("Backend Demo User Exists", True, "Demo user can login successfully")
                    return data['access_token']
                else:
                    self.log_result("Backend Demo User Exists", False, f"No access token in response: {data}")
                    return None
            else:
                self.log_result("Backend Demo User Exists", False, f"Login failed: HTTP {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.log_result("Backend Demo User Exists", False, f"Error: {str(e)}")
            return None
    
    def test_backend_demo_baby_exists(self, auth_token):
        """Test if demo baby exists in backend database"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.get(f"{self.backend_url}/babies", headers=headers, timeout=30)
            
            if response.status_code == 200:
                babies = response.json()
                if isinstance(babies, list) and len(babies) > 0:
                    demo_baby = babies[0]  # Get first baby
                    baby_name = demo_baby.get('name', 'Unknown')
                    self.log_result("Backend Demo Baby Exists", True, f"Found demo baby: {baby_name}")
                    return demo_baby
                else:
                    self.log_result("Backend Demo Baby Exists", False, f"No babies found: {babies}")
                    return None
            else:
                self.log_result("Backend Demo Baby Exists", False, f"HTTP {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_result("Backend Demo Baby Exists", False, f"Error: {str(e)}")
            return None
    
    def test_frontend_login_flow(self):
        """Test frontend login flow with demo credentials"""
        try:
            if not self.driver:
                self.log_result("Frontend Login Flow", False, "Chrome driver not available")
                return False
            
            # Navigate to the app
            self.driver.get(self.frontend_url)
            time.sleep(3)
            
            # Check if we're on login page or already logged in
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")
            
            # Look for login form
            try:
                email_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
                )
                password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
                
                # Fill in demo credentials
                email_input.clear()
                email_input.send_keys(self.demo_email)
                password_input.clear()
                password_input.send_keys(self.demo_password)
                
                # Find and click login button
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button:contains('Login'), button:contains('Sign In')")
                login_button.click()
                
                # Wait for redirect or dashboard
                time.sleep(5)
                
                # Check if login was successful
                current_url = self.driver.current_url
                if "/auth" not in current_url and "/login" not in current_url:
                    self.log_result("Frontend Login Flow", True, f"Login successful, redirected to: {current_url}")
                    return True
                else:
                    self.log_result("Frontend Login Flow", False, f"Login failed, still on: {current_url}")
                    return False
                    
            except TimeoutException:
                # Maybe already logged in?
                if "/dashboard" in current_url or "/tracking" in current_url:
                    self.log_result("Frontend Login Flow", True, "Already logged in")
                    return True
                else:
                    self.log_result("Frontend Login Flow", False, "Login form not found and not logged in")
                    return False
                    
        except Exception as e:
            self.log_result("Frontend Login Flow", False, f"Error: {str(e)}")
            return False
    
    def test_localstorage_baby_data(self):
        """Test localStorage for baby data structure"""
        try:
            if not self.driver:
                self.log_result("LocalStorage Baby Data", False, "Chrome driver not available")
                return False
            
            # Execute JavaScript to check localStorage
            localStorage_keys = self.driver.execute_script("return Object.keys(localStorage);")
            print(f"LocalStorage keys: {localStorage_keys}")
            
            # Check for baby-related keys
            baby_keys = [key for key in localStorage_keys if 'baby' in key.lower()]
            print(f"Baby-related keys: {baby_keys}")
            
            # Check specific keys mentioned in review
            babysteps_keys = [key for key in localStorage_keys if 'babysteps' in key.lower()]
            print(f"BabySteps keys: {babysteps_keys}")
            
            # Get baby data
            baby_data = None
            current_baby = None
            
            for key in babysteps_keys:
                if 'babies' in key:
                    baby_data = self.driver.execute_script(f"return localStorage.getItem('{key}');")
                    print(f"Baby data from {key}: {baby_data}")
                elif 'current' in key and 'baby' in key:
                    current_baby = self.driver.execute_script(f"return localStorage.getItem('{key}');")
                    print(f"Current baby from {key}: {current_baby}")
            
            # Check if baby data exists
            if baby_data:
                try:
                    parsed_baby_data = json.loads(baby_data) if isinstance(baby_data, str) else baby_data
                    if parsed_baby_data and len(parsed_baby_data) > 0:
                        self.log_result("LocalStorage Baby Data", True, f"Baby data found: {len(parsed_baby_data)} babies")
                        return parsed_baby_data
                    else:
                        self.log_result("LocalStorage Baby Data", False, "Baby data exists but is empty")
                        return None
                except json.JSONDecodeError:
                    self.log_result("LocalStorage Baby Data", False, f"Baby data exists but invalid JSON: {baby_data}")
                    return None
            else:
                self.log_result("LocalStorage Baby Data", False, "No baby data found in localStorage")
                return None
                
        except Exception as e:
            self.log_result("LocalStorage Baby Data", False, f"Error: {str(e)}")
            return None
    
    def test_current_baby_state(self):
        """Test currentBaby state in the application"""
        try:
            if not self.driver:
                self.log_result("Current Baby State", False, "Chrome driver not available")
                return False
            
            # Check for "No Baby Selected" message
            try:
                no_baby_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No Baby Selected')]")
                if no_baby_message:
                    self.log_result("Current Baby State", False, "Found 'No Baby Selected' message - currentBaby is null")
                    return False
            except NoSuchElementException:
                pass
            
            # Check for baby profile information on page
            try:
                # Look for baby name or profile elements
                baby_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid*='baby'], .baby-profile, .baby-name")
                if baby_elements:
                    baby_text = [elem.text for elem in baby_elements if elem.text.strip()]
                    self.log_result("Current Baby State", True, f"Baby profile elements found: {baby_text}")
                    return True
                else:
                    # Check page content for baby-related text
                    page_text = self.driver.find_element(By.TAG_NAME, "body").text
                    if any(name in page_text for name in ["Emma", "Baby", "Profile"]):
                        self.log_result("Current Baby State", True, "Baby information found in page content")
                        return True
                    else:
                        self.log_result("Current Baby State", False, "No baby profile information found on page")
                        return False
            except Exception as e:
                self.log_result("Current Baby State", False, f"Error checking baby elements: {str(e)}")
                return False
                
        except Exception as e:
            self.log_result("Current Baby State", False, f"Error: {str(e)}")
            return False
    
    def test_tracking_page_access(self):
        """Test access to tracking page and check for UI components"""
        try:
            if not self.driver:
                self.log_result("Tracking Page Access", False, "Chrome driver not available")
                return False
            
            # Navigate to tracking page
            tracking_url = f"{self.frontend_url}/tracking"
            self.driver.get(tracking_url)
            time.sleep(3)
            
            current_url = self.driver.current_url
            print(f"Tracking page URL: {current_url}")
            
            # Check if we're on the tracking page
            if "/tracking" in current_url:
                # Check for "No Baby Selected" message
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                if "No Baby Selected" in page_text:
                    self.log_result("Tracking Page Access", False, "TrackingPage shows 'No Baby Selected' - currentBaby is null")
                    return False
                else:
                    # Check for tracking UI components
                    quick_actions = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid*='quick-action']")
                    if quick_actions:
                        self.log_result("Tracking Page Access", True, f"Tracking page loaded with {len(quick_actions)} quick actions")
                        return True
                    else:
                        self.log_result("Tracking Page Access", False, "Tracking page loaded but no quick actions found")
                        return False
            else:
                self.log_result("Tracking Page Access", False, f"Could not access tracking page, redirected to: {current_url}")
                return False
                
        except Exception as e:
            self.log_result("Tracking Page Access", False, f"Error: {str(e)}")
            return False
    
    def test_app_js_state_management(self):
        """Test App.js state management for currentBaby"""
        try:
            if not self.driver:
                self.log_result("App.js State Management", False, "Chrome driver not available")
                return False
            
            # Execute JavaScript to check React state (if accessible)
            try:
                # Check if React DevTools or state is accessible
                react_state = self.driver.execute_script("""
                    // Try to find React components and their state
                    const reactElements = document.querySelectorAll('[data-reactroot], [data-react-checksum]');
                    if (reactElements.length > 0) {
                        return 'React app detected';
                    }
                    return 'No React elements found';
                """)
                print(f"React state check: {react_state}")
                
                # Check for currentBaby in window object (if exposed)
                current_baby_check = self.driver.execute_script("""
                    if (window.currentBaby !== undefined) {
                        return window.currentBaby;
                    }
                    if (window.appState && window.appState.currentBaby !== undefined) {
                        return window.appState.currentBaby;
                    }
                    return 'currentBaby not accessible';
                """)
                print(f"CurrentBaby check: {current_baby_check}")
                
                if current_baby_check and current_baby_check != 'currentBaby not accessible':
                    self.log_result("App.js State Management", True, f"CurrentBaby state found: {current_baby_check}")
                    return True
                else:
                    self.log_result("App.js State Management", False, "CurrentBaby state not accessible or null")
                    return False
                    
            except Exception as e:
                self.log_result("App.js State Management", False, f"Error checking React state: {str(e)}")
                return False
                
        except Exception as e:
            self.log_result("App.js State Management", False, f"Error: {str(e)}")
            return False
    
    def test_offline_api_functionality(self):
        """Test offlineAPI.getBabies() functionality"""
        try:
            if not self.driver:
                self.log_result("OfflineAPI Functionality", False, "Chrome driver not available")
                return False
            
            # Execute JavaScript to test offlineAPI
            offline_api_test = self.driver.execute_script("""
                try {
                    // Check if offlineAPI is available
                    if (typeof offlineAPI !== 'undefined') {
                        // Try to call getBabies
                        const babies = offlineAPI.getBabies();
                        return {
                            available: true,
                            babies: babies,
                            count: babies ? babies.length : 0
                        };
                    } else {
                        return {
                            available: false,
                            error: 'offlineAPI not found'
                        };
                    }
                } catch (error) {
                    return {
                        available: false,
                        error: error.message
                    };
                }
            """)
            
            print(f"OfflineAPI test result: {offline_api_test}")
            
            if offline_api_test.get('available'):
                babies_count = offline_api_test.get('count', 0)
                if babies_count > 0:
                    self.log_result("OfflineAPI Functionality", True, f"offlineAPI.getBabies() returns {babies_count} babies")
                    return True
                else:
                    self.log_result("OfflineAPI Functionality", False, "offlineAPI.getBabies() returns empty or null")
                    return False
            else:
                error = offline_api_test.get('error', 'Unknown error')
                self.log_result("OfflineAPI Functionality", False, f"offlineAPI not available: {error}")
                return False
                
        except Exception as e:
            self.log_result("OfflineAPI Functionality", False, f"Error: {str(e)}")
            return False
    
    def run_investigation(self):
        """Run comprehensive baby data loading investigation"""
        print("🔍 BABY DATA LOADING INVESTIGATION")
        print("=" * 80)
        print("Investigating critical issue: currentBaby is null/undefined")
        print("causing TrackingPage to show 'No Baby Selected'")
        print("=" * 80)
        
        # Setup browser
        if not self.setup_driver():
            print("❌ Cannot proceed without browser driver")
            return self.results
        
        try:
            # 1. Test backend demo user and baby data
            print("\n1. BACKEND DATA VERIFICATION:")
            print("-" * 40)
            auth_token = self.test_backend_demo_user_exists()
            if auth_token:
                demo_baby = self.test_backend_demo_baby_exists(auth_token)
                if demo_baby:
                    print(f"✅ Demo baby found: {demo_baby.get('name', 'Unknown')} (ID: {demo_baby.get('id', 'Unknown')})")
            
            # 2. Test frontend login flow
            print("\n2. FRONTEND LOGIN FLOW:")
            print("-" * 40)
            login_success = self.test_frontend_login_flow()
            
            if login_success:
                # 3. Test localStorage baby data
                print("\n3. LOCALSTORAGE INVESTIGATION:")
                print("-" * 40)
                baby_data = self.test_localstorage_baby_data()
                
                # 4. Test currentBaby state
                print("\n4. CURRENT BABY STATE CHECK:")
                print("-" * 40)
                self.test_current_baby_state()
                
                # 5. Test tracking page access
                print("\n5. TRACKING PAGE ACCESS:")
                print("-" * 40)
                self.test_tracking_page_access()
                
                # 6. Test App.js state management
                print("\n6. APP.JS STATE MANAGEMENT:")
                print("-" * 40)
                self.test_app_js_state_management()
                
                # 7. Test offlineAPI functionality
                print("\n7. OFFLINE API FUNCTIONALITY:")
                print("-" * 40)
                self.test_offline_api_functionality()
            
        finally:
            if self.driver:
                self.driver.quit()
        
        # Print summary
        print("\n" + "=" * 80)
        print("🔍 INVESTIGATION SUMMARY:")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🚨 CRITICAL ISSUES FOUND:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Root cause analysis
        print(f"\n🎯 ROOT CAUSE ANALYSIS:")
        print("-" * 40)
        
        if any("No Baby Selected" in error for error in self.results['errors']):
            print("❌ CONFIRMED: currentBaby is null causing 'No Baby Selected' message")
        
        if any("Baby data found" in str(self.results) for error in self.results['errors']):
            print("✅ Baby data exists in localStorage")
            print("❌ But currentBaby state is not being set correctly")
            print("🔧 LIKELY CAUSE: Data binding issue between localStorage and React state")
        
        return self.results

def main():
    """Main investigation execution"""
    tester = BabyDataInvestigationTester()
    results = tester.run_investigation()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()