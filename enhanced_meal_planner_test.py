#!/usr/bin/env python3
"""
Enhanced Meal Planner Testing Suite for Baby Steps Application
Tests the enhanced meal planner functionality with detailed recipe results
"""

import requests
import json
import time
from datetime import datetime, timezone

# Backend URL - using local backend for testing
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

class EnhancedMealPlannerTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 60  # Longer timeout for AI responses
        self.auth_token = None
        # Demo credentials as specified in review request
        self.demo_email = "demo@babysteps.com"
        self.demo_password = "demo123"
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': [],
            'detailed_results': []
        }
    
    def log_result(self, test_name, success, message="", details=None):
        """Log test results with detailed information"""
        result_entry = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        self.results['detailed_results'].append(result_entry)
        
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
        
        if details:
            print(f"   📝 Details: {details}")
    
    def authenticate(self):
        """Authenticate with demo credentials"""
        try:
            login_data = {
                "email": self.demo_email,
                "password": self.demo_password
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.auth_token = data['access_token']
                    self.session.headers.update({'Authorization': f"Bearer {self.auth_token}"})
                    self.log_result("Authentication", True, f"Successfully authenticated as {self.demo_email}")
                    return True
                else:
                    self.log_result("Authentication", False, f"No access token in response: {data}")
                    return False
            else:
                self.log_result("Authentication", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_meal_search_endpoint_basic(self):
        """Test basic functionality of /api/meals/search endpoint"""
        try:
            search_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['results', 'query', 'age_months']
                
                if all(field in data for field in required_fields):
                    if data['query'] == search_query['query'] and data['age_months'] == search_query['baby_age_months']:
                        self.log_result("Meal Search Endpoint Basic", True, 
                                      f"Endpoint working correctly, response length: {len(data['results'])} chars")
                        return data
                    else:
                        self.log_result("Meal Search Endpoint Basic", False, 
                                      f"Query/age mismatch in response: {data}")
                        return None
                else:
                    self.log_result("Meal Search Endpoint Basic", False, 
                                  f"Missing required fields: {data}")
                    return None
            else:
                self.log_result("Meal Search Endpoint Basic", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_result("Meal Search Endpoint Basic", False, f"Error: {str(e)}")
            return None
    
    def test_detailed_recipe_instructions(self):
        """Test that results include detailed step-by-step cooking instructions"""
        try:
            search_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', '').lower()
                
                # Check for detailed cooking instructions indicators
                instruction_indicators = [
                    'step', 'instructions', 'cook', 'bake', 'heat', 'temperature',
                    'minutes', 'degrees', 'stir', 'mix', 'prepare', 'serve'
                ]
                
                found_indicators = [indicator for indicator in instruction_indicators if indicator in results]
                
                if len(found_indicators) >= 3:  # At least 3 cooking instruction indicators
                    self.log_result("Detailed Recipe Instructions", True, 
                                  f"Found {len(found_indicators)} instruction indicators: {found_indicators[:5]}")
                    return True
                else:
                    self.log_result("Detailed Recipe Instructions", False, 
                                  f"Only found {len(found_indicators)} instruction indicators: {found_indicators}")
                    return False
            else:
                self.log_result("Detailed Recipe Instructions", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Detailed Recipe Instructions", False, f"Error: {str(e)}")
            return False
    
    def test_complete_ingredient_lists(self):
        """Test that results include complete ingredient lists with measurements"""
        try:
            search_query = {
                "query": "finger food recipes",
                "baby_age_months": 10
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', '').lower()
                
                # Check for ingredient list indicators
                ingredient_indicators = [
                    'ingredients', 'cup', 'tbsp', 'tsp', 'tablespoon', 'teaspoon',
                    'ounce', 'oz', 'pound', 'lb', 'gram', 'ml', 'banana', 'apple',
                    'flour', 'oil', 'butter', 'milk', 'egg'
                ]
                
                measurement_indicators = [
                    '1 cup', '2 tbsp', '1/2', '1/4', '1 tsp', '2 cups', '3 tbsp'
                ]
                
                found_ingredients = [indicator for indicator in ingredient_indicators if indicator in results]
                found_measurements = [indicator for indicator in measurement_indicators if indicator in results]
                
                if len(found_ingredients) >= 4 and len(found_measurements) >= 1:
                    self.log_result("Complete Ingredient Lists", True, 
                                  f"Found {len(found_ingredients)} ingredients and {len(found_measurements)} measurements")
                    return True
                else:
                    self.log_result("Complete Ingredient Lists", False, 
                                  f"Found {len(found_ingredients)} ingredients and {len(found_measurements)} measurements")
                    return False
            else:
                self.log_result("Complete Ingredient Lists", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Complete Ingredient Lists", False, f"Error: {str(e)}")
            return False
    
    def test_safety_guidelines(self):
        """Test that results include safety guidelines and serving suggestions"""
        try:
            search_query = {
                "query": "finger food recipes",
                "baby_age_months": 9
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', '').lower()
                
                # Check for safety guideline indicators
                safety_indicators = [
                    'safety', 'safe', 'supervise', 'supervision', 'choke', 'choking',
                    'small pieces', 'soft', 'avoid', 'caution', 'warning', 'careful',
                    'watch', 'monitor', 'size', 'texture'
                ]
                
                serving_indicators = [
                    'serve', 'serving', 'portion', 'amount', 'size', 'pieces',
                    'cut', 'slice', 'dice', 'mash', 'puree'
                ]
                
                found_safety = [indicator for indicator in safety_indicators if indicator in results]
                found_serving = [indicator for indicator in serving_indicators if indicator in results]
                
                if len(found_safety) >= 2 and len(found_serving) >= 2:
                    self.log_result("Safety Guidelines", True, 
                                  f"Found {len(found_safety)} safety and {len(found_serving)} serving indicators")
                    return True
                else:
                    self.log_result("Safety Guidelines", False, 
                                  f"Found {len(found_safety)} safety and {len(found_serving)} serving indicators")
                    return False
            else:
                self.log_result("Safety Guidelines", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Safety Guidelines", False, f"Error: {str(e)}")
            return False
    
    def test_storage_instructions(self):
        """Test that results include storage and freezing instructions"""
        try:
            search_query = {
                "query": "family meal ideas baby can share",
                "baby_age_months": 12
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', '').lower()
                
                # Check for storage instruction indicators
                storage_indicators = [
                    'storage', 'store', 'refrigerate', 'fridge', 'freeze', 'freezer',
                    'reheat', 'reheating', 'leftover', 'leftovers', 'keep', 'fresh',
                    'days', 'hours', 'container', 'airtight'
                ]
                
                found_storage = [indicator for indicator in storage_indicators if indicator in results]
                
                if len(found_storage) >= 2:
                    self.log_result("Storage Instructions", True, 
                                  f"Found {len(found_storage)} storage indicators: {found_storage[:3]}")
                    return True
                else:
                    self.log_result("Storage Instructions", False, 
                                  f"Found only {len(found_storage)} storage indicators: {found_storage}")
                    return False
            else:
                self.log_result("Storage Instructions", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Storage Instructions", False, f"Error: {str(e)}")
            return False
    
    def test_age_appropriate_modifications(self):
        """Test that results include age-appropriate modifications"""
        try:
            search_query = {
                "query": "lunch recipes for 10 month old",
                "baby_age_months": 10
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', '').lower()
                
                # Check for age-appropriate modification indicators
                age_indicators = [
                    'month', 'months', 'age', 'older', 'younger', '6 months', '8 months',
                    '10 months', '12 months', 'toddler', 'baby', 'infant', 'appropriate',
                    'suitable', 'modify', 'adjust', 'adaptation', 'version'
                ]
                
                texture_indicators = [
                    'texture', 'soft', 'smooth', 'chunky', 'lumpy', 'mash', 'puree',
                    'finger food', 'self-feeding', 'bite-sized', 'small pieces'
                ]
                
                found_age = [indicator for indicator in age_indicators if indicator in results]
                found_texture = [indicator for indicator in texture_indicators if indicator in results]
                
                if len(found_age) >= 3 and len(found_texture) >= 2:
                    self.log_result("Age-Appropriate Modifications", True, 
                                  f"Found {len(found_age)} age and {len(found_texture)} texture indicators")
                    return True
                else:
                    self.log_result("Age-Appropriate Modifications", False, 
                                  f"Found {len(found_age)} age and {len(found_texture)} texture indicators")
                    return False
            else:
                self.log_result("Age-Appropriate Modifications", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Age-Appropriate Modifications", False, f"Error: {str(e)}")
            return False
    
    def test_response_quality_vs_generic(self):
        """Test that responses are detailed and recipe-focused (not generic)"""
        try:
            search_query = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            response = self.session.post(f"{API_BASE}/meals/search", json=search_query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', '')
                
                # Check response length (detailed responses should be longer)
                if len(results) < 500:
                    self.log_result("Response Quality vs Generic", False, 
                                  f"Response too short ({len(results)} chars) - may be generic")
                    return False
                
                # Check for generic response indicators (bad signs)
                generic_indicators = [
                    'consult your pediatrician', 'talk to your doctor', 'general guidelines',
                    'every baby is different', 'please consult', 'unable to provide',
                    'sorry, i cannot', 'i recommend consulting'
                ]
                
                found_generic = [indicator for indicator in generic_indicators if indicator.lower() in results.lower()]
                
                # Check for specific recipe indicators (good signs)
                specific_indicators = [
                    'recipe', 'ingredients', 'instructions', 'step', 'cook', 'bake',
                    'temperature', 'minutes', 'cup', 'tbsp', 'serve', 'preparation'
                ]
                
                found_specific = [indicator for indicator in specific_indicators if indicator.lower() in results.lower()]
                
                if len(found_generic) == 0 and len(found_specific) >= 5:
                    self.log_result("Response Quality vs Generic", True, 
                                  f"Response is detailed and recipe-focused ({len(results)} chars, {len(found_specific)} specific indicators)")
                    return True
                else:
                    self.log_result("Response Quality vs Generic", False, 
                                  f"Response may be generic ({len(found_generic)} generic, {len(found_specific)} specific indicators)")
                    return False
            else:
                self.log_result("Response Quality vs Generic", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Response Quality vs Generic", False, f"Error: {str(e)}")
            return False
    
    def test_all_specified_queries(self):
        """Test all the specific queries mentioned in the review request"""
        test_queries = [
            {"query": "breakfast ideas for 8 month old", "baby_age_months": 8},
            {"query": "finger food recipes", "baby_age_months": 9},
            {"query": "family meal ideas baby can share", "baby_age_months": 12},
            {"query": "lunch recipes for 10 month old", "baby_age_months": 10}
        ]
        
        all_passed = True
        results_summary = []
        
        for i, test_query in enumerate(test_queries, 1):
            try:
                print(f"\n🔍 Testing Query {i}: '{test_query['query']}'")
                
                response = self.session.post(f"{API_BASE}/meals/search", json=test_query, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', '')
                    
                    # Analyze response quality
                    analysis = {
                        'query': test_query['query'],
                        'age_months': test_query['baby_age_months'],
                        'response_length': len(results),
                        'has_instructions': any(word in results.lower() for word in ['step', 'cook', 'bake', 'prepare']),
                        'has_ingredients': any(word in results.lower() for word in ['cup', 'tbsp', 'ingredients']),
                        'has_safety': any(word in results.lower() for word in ['safe', 'supervise', 'caution']),
                        'has_storage': any(word in results.lower() for word in ['store', 'refrigerate', 'freeze']),
                        'response_preview': results[:200] + "..." if len(results) > 200 else results
                    }
                    
                    results_summary.append(analysis)
                    
                    # Check if response meets quality criteria
                    quality_score = sum([
                        analysis['response_length'] > 300,
                        analysis['has_instructions'],
                        analysis['has_ingredients'],
                        analysis['has_safety'] or analysis['has_storage']
                    ])
                    
                    if quality_score >= 3:
                        print(f"   ✅ Query {i} passed quality check (score: {quality_score}/4)")
                    else:
                        print(f"   ❌ Query {i} failed quality check (score: {quality_score}/4)")
                        all_passed = False
                else:
                    print(f"   ❌ Query {i} failed: HTTP {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                print(f"   ❌ Query {i} error: {str(e)}")
                all_passed = False
        
        if all_passed:
            self.log_result("All Specified Queries", True, 
                          f"All {len(test_queries)} queries returned detailed responses", 
                          results_summary)
        else:
            self.log_result("All Specified Queries", False, 
                          f"Some queries failed quality checks", 
                          results_summary)
        
        return all_passed
    
    def run_comprehensive_test(self):
        """Run comprehensive enhanced meal planner testing"""
        print("🚀 ENHANCED MEAL PLANNER TESTING SUITE")
        print(f"📍 Testing against: {API_BASE}")
        print(f"👤 Demo user: {self.demo_email}")
        print("=" * 80)
        
        # Step 1: Authentication
        print("\n🔐 1. AUTHENTICATION")
        print("=" * 40)
        if not self.authenticate():
            print("❌ Authentication failed - cannot proceed")
            return self.results
        
        # Step 2: Basic endpoint functionality
        print("\n🔍 2. BASIC ENDPOINT FUNCTIONALITY")
        print("=" * 40)
        basic_result = self.test_meal_search_endpoint_basic()
        if not basic_result:
            print("❌ Basic endpoint test failed - cannot proceed")
            return self.results
        
        # Step 3: Enhanced functionality tests
        print("\n🍳 3. ENHANCED RECIPE FUNCTIONALITY TESTS")
        print("=" * 40)
        
        print("📝 Testing detailed recipe instructions...")
        self.test_detailed_recipe_instructions()
        
        print("🥄 Testing complete ingredient lists...")
        self.test_complete_ingredient_lists()
        
        print("⚠️ Testing safety guidelines...")
        self.test_safety_guidelines()
        
        print("📦 Testing storage instructions...")
        self.test_storage_instructions()
        
        print("👶 Testing age-appropriate modifications...")
        self.test_age_appropriate_modifications()
        
        print("🎯 Testing response quality vs generic...")
        self.test_response_quality_vs_generic()
        
        # Step 4: Test all specified queries
        print("\n🔍 4. SPECIFIED QUERY TESTING")
        print("=" * 40)
        self.test_all_specified_queries()
        
        # Step 5: Results summary
        print("\n📊 5. TEST RESULTS SUMMARY")
        print("=" * 40)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print(f"\n🔍 Failed Tests:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        # Enhanced meal planner specific summary
        print(f"\n🎯 ENHANCED MEAL PLANNER VERIFICATION:")
        print("=" * 40)
        
        enhancement_tests = [
            "Detailed Recipe Instructions",
            "Complete Ingredient Lists", 
            "Safety Guidelines",
            "Storage Instructions",
            "Age-Appropriate Modifications",
            "Response Quality vs Generic",
            "All Specified Queries"
        ]
        
        failed_enhancements = [error for error in self.results['errors'] 
                             if any(test in error for test in enhancement_tests)]
        
        if len(failed_enhancements) == 0:
            print("✅ ENHANCED MEAL PLANNER: All enhancement features working")
            print("   • Detailed step-by-step cooking instructions ✅")
            print("   • Complete ingredient lists with measurements ✅")
            print("   • Safety guidelines and serving suggestions ✅")
            print("   • Storage and freezing instructions ✅")
            print("   • Age-appropriate modifications ✅")
            print("   • Recipe-focused (not generic) responses ✅")
        else:
            print("❌ ENHANCED MEAL PLANNER: Some enhancement features need work")
            for test in failed_enhancements:
                print(f"   • {test}")
        
        return self.results

def main():
    """Main test execution"""
    tester = EnhancedMealPlannerTester()
    results = tester.run_comprehensive_test()
    
    # Save detailed results to file
    with open('/app/enhanced_meal_planner_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: enhanced_meal_planner_test_results.json")
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()