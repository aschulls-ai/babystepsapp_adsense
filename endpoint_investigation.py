#!/usr/bin/env python3
"""
ENDPOINT INVESTIGATION: Check what endpoints are actually available
"""

import requests
import json
import time

class EndpointInvestigator:
    def __init__(self):
        self.base_url = "https://activity-repair.preview.emergentagent.com"
        self.token = None
        
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
            print(f"✅ Authentication successful: {self.token[:20]}...")
            return True
        else:
            print(f"❌ Authentication failed: HTTP {response.status_code}")
            return False
    
    def get_auth_headers(self):
        """Get authorization headers"""
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}
    
    def test_endpoint(self, method, endpoint, data=None):
        """Test a specific endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.get_auth_headers(), timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=self.get_auth_headers(), timeout=10)
            
            return response.status_code, response.text[:200] if response.text else ""
        except requests.exceptions.Timeout:
            return "Timeout", ""
        except Exception as e:
            return f"Error: {str(e)}", ""
    
    def investigate_endpoints(self):
        """Investigate available endpoints"""
        print("🔍 ENDPOINT INVESTIGATION")
        print("=" * 50)
        
        if not self.authenticate():
            return
        
        # Test various endpoints
        endpoints_to_test = [
            ("GET", "/api/activities"),
            ("GET", "/api/activities?baby_id=demo-baby-456"),
            ("GET", "/api/activities?baby_id=demo-baby-456&type=feeding"),
            ("GET", "/api/activities?baby_id=demo-baby-456&type=feeding&limit=5"),
            ("POST", "/api/activities", {"baby_id": "demo-baby-456", "type": "feeding", "feeding_type": "bottle"}),
            ("GET", "/api/feedings"),
            ("GET", "/api/feedings?baby_id=demo-baby-456"),
            ("POST", "/api/feedings", {"baby_id": "demo-baby-456", "type": "bottle", "amount": 5.0}),
            ("GET", "/api/diapers"),
            ("GET", "/api/sleep"),
            ("GET", "/api/pumping"),
            ("GET", "/api/measurements"),
            ("GET", "/api/milestones"),
            ("GET", "/api/babies"),
            ("GET", "/api/health"),
        ]
        
        print("\n📋 ENDPOINT TEST RESULTS:")
        for method, endpoint, *data in endpoints_to_test:
            test_data = data[0] if data else None
            status, response_text = self.test_endpoint(method, endpoint, test_data)
            
            if isinstance(status, int):
                if status == 200:
                    print(f"✅ {method} {endpoint} - HTTP {status}")
                elif status == 404:
                    print(f"❌ {method} {endpoint} - HTTP {status} (NOT FOUND)")
                elif status in [401, 403]:
                    print(f"🔒 {method} {endpoint} - HTTP {status} (AUTH ISSUE)")
                else:
                    print(f"⚠️ {method} {endpoint} - HTTP {status}")
                    if response_text:
                        print(f"    Response: {response_text}")
            else:
                print(f"💥 {method} {endpoint} - {status}")
        
        # Test specific feeding data retrieval
        print("\n📋 FEEDING DATA RETRIEVAL TEST:")
        
        # Try /api/feedings endpoint
        status, response_text = self.test_endpoint("GET", "/api/feedings?baby_id=demo-baby-456")
        if isinstance(status, int) and status == 200:
            try:
                feedings_data = json.loads(response_text)
                print(f"✅ /api/feedings returned {len(feedings_data)} feedings")
                if feedings_data:
                    sample_feeding = feedings_data[0]
                    print(f"    Sample feeding: {sample_feeding}")
            except:
                print(f"✅ /api/feedings responded but couldn't parse JSON")
        else:
            print(f"❌ /api/feedings failed: {status}")
        
        # Try creating a feeding via /api/feedings
        print("\n📋 FEEDING CREATION TEST:")
        feeding_data = {
            "baby_id": "demo-baby-456",
            "type": "bottle",
            "amount": 5.0,
            "notes": "Test feeding via /api/feedings"
        }
        
        status, response_text = self.test_endpoint("POST", "/api/feedings", feeding_data)
        if isinstance(status, int) and status in [200, 201]:
            try:
                created_feeding = json.loads(response_text)
                print(f"✅ Created feeding via /api/feedings: {created_feeding.get('id', 'No ID')}")
                print(f"    Feeding type: {created_feeding.get('type', 'No type')}")
                print(f"    Amount: {created_feeding.get('amount', 'No amount')}")
            except:
                print(f"✅ /api/feedings creation responded but couldn't parse JSON")
        else:
            print(f"❌ /api/feedings creation failed: {status}")
            if response_text:
                print(f"    Response: {response_text}")

if __name__ == "__main__":
    investigator = EndpointInvestigator()
    investigator.investigate_endpoints()