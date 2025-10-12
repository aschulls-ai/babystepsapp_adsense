#!/usr/bin/env python3
"""
AI Assistant Failure Diagnosis Test
Focused testing for the reported AI Assistant failure issue
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://baby-steps-demo-api.onrender.com"

class AIAssistantDiagnostics:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.token = None
        self.test_results = []
        
    def log_result(self, test_name, success, details, response_data=None):
        """Log test result with detailed information"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        print(f"   Details: {details}")
        if response_data:
            print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
        print()
        
    def test_backend_health(self):
        """Test 1: Basic backend connectivity"""
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=10)
            if response.status_code == 200:
                self.log_result("Backend Health Check", True, f"Backend responding (HTTP {response.status_code})")
                return True
            else:
                self.log_result("Backend Health Check", False, f"Backend returned HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Backend Health Check", False, f"Connection failed: {str(e)}")
            return False
    
    def test_demo_login(self):
        """Test 2: Demo user authentication"""
        try:
            login_data = {
                "email": "demo@babysteps.com",
                "password": "demo123"
            }
            
            response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                if self.token:
                    self.log_result("Demo Login", True, "JWT token obtained successfully", {"token_length": len(self.token)})
                    return True
                else:
                    self.log_result("Demo Login", False, "No access token in response", data)
                    return False
            else:
                self.log_result("Demo Login", False, f"Login failed (HTTP {response.status_code})", response.text)
                return False
                
        except Exception as e:
            self.log_result("Demo Login", False, f"Login request failed: {str(e)}")
            return False
    
    def test_ai_chat_endpoint(self):
        """Test 3: AI Chat endpoint with authentication"""
        if not self.token:
            self.log_result("AI Chat Endpoint", False, "No authentication token available")
            return False
            
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            # Test the specific query mentioned in the review
            chat_data = {
                "message": "When can babies eat strawberries?",
                "baby_age_months": 6
            }
            
            response = requests.post(
                f"{self.backend_url}/api/ai/chat",
                json=chat_data,
                headers=headers,
                timeout=30  # AI requests can take longer
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                # Check if it's a real AI response or fallback
                if "demo response" in ai_response.lower() or "temporarily unavailable" in ai_response.lower():
                    self.log_result("AI Chat Endpoint", False, "Returning fallback response - AI not working", {
                        "response_length": len(ai_response),
                        "response_preview": ai_response[:100]
                    })
                    return False
                elif len(ai_response) > 50:  # Real AI responses are typically longer
                    self.log_result("AI Chat Endpoint", True, "Real AI response received", {
                        "response_length": len(ai_response),
                        "response_preview": ai_response[:100]
                    })
                    return True
                else:
                    self.log_result("AI Chat Endpoint", False, "Response too short - likely error", {
                        "response_length": len(ai_response),
                        "full_response": ai_response
                    })
                    return False
            else:
                self.log_result("AI Chat Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("AI Chat Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def test_food_research_endpoint(self):
        """Test 4: Food Research endpoint"""
        if not self.token:
            self.log_result("Food Research Endpoint", False, "No authentication token available")
            return False
            
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            research_data = {
                "question": "Are strawberries safe for babies?",
                "baby_age_months": 6
            }
            
            response = requests.post(
                f"{self.backend_url}/api/food/research",
                json=research_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "")
                safety_level = data.get("safety_level", "")
                
                if "temporarily unavailable" in answer.lower() or "demo response" in answer.lower():
                    self.log_result("Food Research Endpoint", False, "Returning fallback response", {
                        "safety_level": safety_level,
                        "answer_preview": answer[:100]
                    })
                    return False
                else:
                    self.log_result("Food Research Endpoint", True, "Real food research response", {
                        "safety_level": safety_level,
                        "answer_length": len(answer)
                    })
                    return True
            else:
                self.log_result("Food Research Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Food Research Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def test_meal_search_endpoint(self):
        """Test 5: Meal Search endpoint"""
        if not self.token:
            self.log_result("Meal Search Endpoint", False, "No authentication token available")
            return False
            
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            meal_data = {
                "query": "breakfast ideas for 8 month old",
                "baby_age_months": 8
            }
            
            response = requests.post(
                f"{self.backend_url}/api/meals/search",
                json=meal_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", "")
                
                if "temporarily unavailable" in results.lower() or "demo response" in results.lower():
                    self.log_result("Meal Search Endpoint", False, "Returning fallback response", {
                        "results_preview": results[:100]
                    })
                    return False
                else:
                    self.log_result("Meal Search Endpoint", True, "Real meal search response", {
                        "results_length": len(results)
                    })
                    return True
            else:
                self.log_result("Meal Search Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Meal Search Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def check_environment_variables(self):
        """Test 6: Check if AI keys are configured (indirect test)"""
        # We can't directly check environment variables on the server,
        # but we can infer from the responses whether keys are configured
        
        ai_working = False
        emergent_working = False
        
        # Check if AI chat worked (indicates OPENAI_API_KEY is set)
        for result in self.test_results:
            if result["test"] == "AI Chat Endpoint" and result["success"]:
                ai_working = True
            if result["test"] in ["Food Research Endpoint", "Meal Search Endpoint"] and result["success"]:
                emergent_working = True
        
        if ai_working and emergent_working:
            self.log_result("Environment Variables", True, "Both OPENAI_API_KEY and EMERGENT_LLM_KEY appear to be configured")
        elif ai_working:
            self.log_result("Environment Variables", False, "OPENAI_API_KEY working, but EMERGENT_LLM_KEY may be missing")
        elif emergent_working:
            self.log_result("Environment Variables", False, "EMERGENT_LLM_KEY working, but OPENAI_API_KEY may be missing")
        else:
            self.log_result("Environment Variables", False, "Both API keys appear to be missing or misconfigured")
    
    def run_full_diagnosis(self):
        """Run complete AI Assistant diagnosis"""
        print("🔍 AI Assistant Failure Diagnosis")
        print("=" * 50)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Time: {datetime.now().isoformat()}")
        print()
        
        # Run all tests in sequence
        self.test_backend_health()
        self.test_demo_login()
        self.test_ai_chat_endpoint()
        self.test_food_research_endpoint()
        self.test_meal_search_endpoint()
        self.check_environment_variables()
        
        # Summary
        print("=" * 50)
        print("📊 DIAGNOSIS SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print()
        
        # Critical findings
        critical_issues = []
        for result in self.test_results:
            if not result["success"]:
                critical_issues.append(f"❌ {result['test']}: {result['details']}")
        
        if critical_issues:
            print("🚨 CRITICAL ISSUES FOUND:")
            for issue in critical_issues:
                print(f"   {issue}")
        else:
            print("✅ All tests passed - AI Assistant should be working")
        
        print()
        print("💡 RECOMMENDATIONS:")
        
        # Specific recommendations based on failures
        ai_chat_failed = any(r["test"] == "AI Chat Endpoint" and not r["success"] for r in self.test_results)
        food_research_failed = any(r["test"] == "Food Research Endpoint" and not r["success"] for r in self.test_results)
        
        if ai_chat_failed:
            print("   • Check OPENAI_API_KEY configuration on Render deployment")
            print("   • Verify gpt-5-nano model access permissions")
        
        if food_research_failed:
            print("   • Check EMERGENT_LLM_KEY configuration on Render deployment")
            print("   • Verify emergentintegrations package installation")
        
        if not ai_chat_failed and not food_research_failed:
            print("   • AI endpoints appear to be working correctly")
            print("   • Issue may be frontend-related or user-specific")

if __name__ == "__main__":
    diagnostics = AIAssistantDiagnostics()
    diagnostics.run_full_diagnosis()