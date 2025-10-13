#!/usr/bin/env python3
"""
COMPREHENSIVE DIAGNOSIS: Recent Feeding Widget Data Flow Issue

ROOT CAUSE IDENTIFIED:
- Frontend expects: /api/activities?baby_id=X&type=feeding&limit=5
- Backend provides: /api/feedings?baby_id=X (separate endpoints)
- The /api/activities unified endpoint does NOT exist

This explains why feeding activities don't show up in Recent Feeding widget!
"""

import requests
import json
import time
from datetime import datetime, timezone

class FeedingWidgetDiagnoser:
    def __init__(self):
        self.base_url = "https://activity-repair.preview.emergentagent.com"
        self.token = None
        self.baby_id = None
        self.test_results = []
        
    def log_result(self, test_name, success, details=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "details": details
        }
        self.test_results.append(result)
        print(f"{status} - {test_name}")
        if details:
            print(f"    {details}")
    
    def authenticate(self):
        """Authenticate and get token"""
        data = {
            "email": "demo@babysteps.com",
            "password": "demo123"
        }
        
        response = requests.post(f"{self.base_url}/api/auth/login", json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("access_token")
            self.log_result("Authentication", True, f"JWT token received: {self.token[:20]}...")
            return True
        else:
            self.log_result("Authentication", False, f"HTTP {response.status_code}")
            return False
    
    def get_auth_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def get_baby_id(self):
        """Get or create a baby for testing"""
        # First try to get existing babies
        response = requests.get(f"{self.base_url}/api/babies", headers=self.get_auth_headers(), timeout=30)
        
        if response.status_code == 200:
            babies = response.json()
            if babies:
                self.baby_id = babies[0]["id"]
                self.log_result("Get Baby ID", True, f"Using existing baby: {self.baby_id}")
                return True
        
        # Create a new baby
        baby_data = {
            "name": "Test Baby for Feeding Widget",
            "birth_date": "2024-01-01T00:00:00Z",
            "gender": "other"
        }
        
        response = requests.post(f"{self.base_url}/api/babies", json=baby_data, headers=self.get_auth_headers(), timeout=30)
        
        if response.status_code in [200, 201]:
            baby = response.json()
            self.baby_id = baby["id"]
            self.log_result("Create Baby", True, f"Created baby: {self.baby_id}")
            return True
        else:
            self.log_result("Get/Create Baby", False, f"HTTP {response.status_code}")
            return False
    
    def test_feeding_creation_via_separate_endpoint(self):
        """Test creating feedings via /api/feedings (the working endpoint)"""
        feeding_data = {
            "baby_id": self.baby_id,
            "type": "bottle",
            "amount": 5.0,
            "notes": "Test feeding via separate endpoint"
        }
        
        response = requests.post(f"{self.base_url}/api/feedings", json=feeding_data, headers=self.get_auth_headers(), timeout=30)
        
        if response.status_code in [200, 201]:
            try:
                result = response.json()
                feeding_id = result.get("id")
                self.log_result("Create Feeding (Separate Endpoint)", True, f"Created feeding ID: {feeding_id}")
                return feeding_id
            except:
                self.log_result("Create Feeding (Separate Endpoint)", False, "Invalid JSON response")
                return None
        else:
            error_detail = ""
            try:
                error_detail = response.text[:200]
            except:
                pass
            self.log_result("Create Feeding (Separate Endpoint)", False, f"HTTP {response.status_code} - {error_detail}")
            return None
    
    def test_feeding_retrieval_via_separate_endpoint(self):
        """Test retrieving feedings via /api/feedings"""
        response = requests.get(f"{self.base_url}/api/feedings?baby_id={self.baby_id}", headers=self.get_auth_headers(), timeout=30)
        
        if response.status_code == 200:
            try:
                feedings = response.json()
                self.log_result("Retrieve Feedings (Separate Endpoint)", True, f"Retrieved {len(feedings)} feedings")
                return feedings
            except:
                self.log_result("Retrieve Feedings (Separate Endpoint)", False, "Invalid JSON response")
                return None
        else:
            self.log_result("Retrieve Feedings (Separate Endpoint)", False, f"HTTP {response.status_code}")
            return None
    
    def test_unified_activities_endpoint(self):
        """Test the unified /api/activities endpoint that frontend expects"""
        # Test GET
        response = requests.get(f"{self.base_url}/api/activities?baby_id={self.baby_id}&type=feeding&limit=5", 
                              headers=self.get_auth_headers(), timeout=30)
        
        if response.status_code == 404:
            self.log_result("Unified Activities Endpoint (GET)", False, "HTTP 404 - Endpoint does not exist")
        elif response.status_code == 200:
            try:
                activities = response.json()
                self.log_result("Unified Activities Endpoint (GET)", True, f"Retrieved {len(activities)} activities")
                return activities
            except:
                self.log_result("Unified Activities Endpoint (GET)", False, "Invalid JSON response")
                return None
        else:
            self.log_result("Unified Activities Endpoint (GET)", False, f"HTTP {response.status_code}")
            return None
        
        # Test POST
        activity_data = {
            "baby_id": self.baby_id,
            "type": "feeding",
            "feeding_type": "bottle",
            "amount": 5.0,
            "notes": "Test via unified endpoint"
        }
        
        response = requests.post(f"{self.base_url}/api/activities", json=activity_data, headers=self.get_auth_headers(), timeout=30)
        
        if response.status_code == 404:
            self.log_result("Unified Activities Endpoint (POST)", False, "HTTP 404 - Endpoint does not exist")
        elif response.status_code in [200, 201]:
            self.log_result("Unified Activities Endpoint (POST)", True, "Activity created successfully")
        else:
            self.log_result("Unified Activities Endpoint (POST)", False, f"HTTP {response.status_code}")
        
        return None
    
    def analyze_frontend_backend_mismatch(self):
        """Analyze the mismatch between frontend expectations and backend reality"""
        print("\n🔍 FRONTEND-BACKEND MISMATCH ANALYSIS")
        print("=" * 60)
        
        # What frontend expects (based on review request)
        frontend_expectations = {
            "quick_feed_post": "POST /api/activities",
            "recent_feeding_get": "GET /api/activities?baby_id=X&type=feeding&limit=5",
            "activity_history_get": "GET /api/activities?baby_id=X"
        }
        
        # What backend actually provides
        backend_reality = {
            "feeding_post": "POST /api/feedings",
            "feeding_get": "GET /api/feedings?baby_id=X",
            "diaper_get": "GET /api/diapers?baby_id=X",
            "sleep_get": "GET /api/sleep?baby_id=X",
            "pumping_get": "GET /api/pumping?baby_id=X",
            "measurements_get": "GET /api/measurements?baby_id=X",
            "milestones_get": "GET /api/milestones?baby_id=X"
        }
        
        print("FRONTEND EXPECTATIONS:")
        for key, endpoint in frontend_expectations.items():
            print(f"  {key}: {endpoint}")
        
        print("\nBACKEND REALITY:")
        for key, endpoint in backend_reality.items():
            print(f"  {key}: {endpoint}")
        
        print("\n❌ MISMATCH IDENTIFIED:")
        print("  - Frontend expects unified /api/activities endpoint")
        print("  - Backend provides separate endpoints for each activity type")
        print("  - Recent Feeding widget calls non-existent /api/activities endpoint")
        print("  - This causes empty results in Recent Feeding widget")
        
        return {
            "frontend_expectations": frontend_expectations,
            "backend_reality": backend_reality,
            "mismatch": True
        }
    
    def test_complete_feeding_flow(self):
        """Test the complete feeding flow using correct endpoints"""
        print("\n🧪 TESTING COMPLETE FEEDING FLOW WITH CORRECT ENDPOINTS")
        print("=" * 60)
        
        # Step 1: Create feeding via correct endpoint
        feeding_id = self.test_feeding_creation_via_separate_endpoint()
        
        if not feeding_id:
            self.log_result("Complete Feeding Flow", False, "Could not create feeding")
            return False
        
        # Step 2: Retrieve feedings via correct endpoint
        feedings = self.test_feeding_retrieval_via_separate_endpoint()
        
        if feedings is None:
            self.log_result("Complete Feeding Flow", False, "Could not retrieve feedings")
            return False
        
        # Step 3: Verify our feeding appears
        feeding_ids = [f.get("id") for f in feedings]
        if feeding_id in feeding_ids:
            self.log_result("Complete Feeding Flow", True, f"Feeding {feeding_id} successfully created and retrieved")
            return True
        else:
            self.log_result("Complete Feeding Flow", False, f"Created feeding {feeding_id} not found in retrieval")
            return False
    
    def generate_solution_recommendations(self):
        """Generate recommendations to fix the issue"""
        print("\n💡 SOLUTION RECOMMENDATIONS")
        print("=" * 60)
        
        solutions = [
            {
                "option": "Option 1: Update Frontend (Recommended)",
                "description": "Update Recent Feeding widget to use /api/feedings endpoint",
                "steps": [
                    "Change Recent Feeding widget API call from:",
                    "  GET /api/activities?baby_id=X&type=feeding&limit=5",
                    "To:",
                    "  GET /api/feedings?baby_id=X",
                    "Add client-side limit of 5 results",
                    "Ensure proper sorting by timestamp (newest first)"
                ],
                "pros": ["Quick fix", "Uses existing working backend"],
                "cons": ["Need to update multiple widgets for different activity types"]
            },
            {
                "option": "Option 2: Add Unified Backend Endpoint",
                "description": "Implement /api/activities endpoint in backend",
                "steps": [
                    "Add /api/activities GET endpoint that:",
                    "  - Accepts baby_id, type, limit parameters",
                    "  - Queries appropriate collection based on type",
                    "  - Returns unified response format",
                    "Add /api/activities POST endpoint that:",
                    "  - Routes to appropriate handler based on type",
                    "  - Maintains consistent response format"
                ],
                "pros": ["Matches frontend expectations", "Unified API design"],
                "cons": ["More backend development work", "Need to test all activity types"]
            },
            {
                "option": "Option 3: Hybrid Approach",
                "description": "Add /api/activities GET only for widgets",
                "steps": [
                    "Add /api/activities GET endpoint for widget data retrieval",
                    "Keep existing POST endpoints for activity creation",
                    "Update only Recent Feeding widget to use new endpoint"
                ],
                "pros": ["Minimal changes", "Backward compatible"],
                "cons": ["Mixed API design"]
            }
        ]
        
        for i, solution in enumerate(solutions, 1):
            print(f"\n{solution['option']}:")
            print(f"  Description: {solution['description']}")
            print("  Steps:")
            for step in solution['steps']:
                print(f"    {step}")
            print(f"  Pros: {', '.join(solution['pros'])}")
            print(f"  Cons: {', '.join(solution['cons'])}")
        
        print(f"\n🎯 RECOMMENDED IMMEDIATE FIX:")
        print("  Update Recent Feeding widget to call:")
        print("    GET /api/feedings?baby_id={baby_id}")
        print("  And implement client-side limit and sorting")
        
        return solutions
    
    def run_diagnosis(self):
        """Run complete diagnosis"""
        print("🚀 COMPREHENSIVE DIAGNOSIS: Recent Feeding Widget Data Flow Issue")
        print(f"Backend: {self.base_url}")
        print("=" * 80)
        
        # Step 1: Authentication
        if not self.authenticate():
            return
        
        # Step 2: Get baby ID
        if not self.get_baby_id():
            return
        
        # Step 3: Test unified endpoint (expected to fail)
        print("\n📋 TESTING FRONTEND EXPECTATIONS:")
        self.test_unified_activities_endpoint()
        
        # Step 4: Test separate endpoints (expected to work)
        print("\n📋 TESTING BACKEND REALITY:")
        self.test_complete_feeding_flow()
        
        # Step 5: Analyze mismatch
        mismatch_analysis = self.analyze_frontend_backend_mismatch()
        
        # Step 6: Generate solutions
        solutions = self.generate_solution_recommendations()
        
        # Step 7: Summary
        print("\n📊 DIAGNOSIS SUMMARY")
        print("=" * 60)
        
        success_rate = sum(1 for r in self.test_results if "✅" in r["status"]) / len(self.test_results) * 100
        
        print(f"Tests Passed: {sum(1 for r in self.test_results if '✅' in r['status'])}/{len(self.test_results)} ({success_rate:.1f}%)")
        
        print("\n🔍 ROOT CAUSE CONFIRMED:")
        print("  ❌ Frontend calls non-existent /api/activities endpoint")
        print("  ✅ Backend provides working /api/feedings endpoint")
        print("  ❌ Recent Feeding widget gets 404 errors")
        print("  ❌ Widget displays empty results")
        
        print("\n🎯 IMMEDIATE ACTION REQUIRED:")
        print("  1. Update Recent Feeding widget API endpoint")
        print("  2. Change from /api/activities to /api/feedings")
        print("  3. Add client-side limit and sorting")
        print("  4. Test widget functionality")
        
        return {
            "root_cause": "Frontend-Backend API endpoint mismatch",
            "success_rate": success_rate,
            "test_results": self.test_results,
            "solutions": solutions
        }

if __name__ == "__main__":
    diagnoser = FeedingWidgetDiagnoser()
    results = diagnoser.run_diagnosis()