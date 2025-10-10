#!/usr/bin/env python3
"""
Quick Enhanced Meal Planner Test for Baby Steps Application
"""

import requests
import json
import time

# Local backend
API_BASE = "http://localhost:8001/api"

def test_enhanced_meal_planner():
    """Test enhanced meal planner functionality"""
    session = requests.Session()
    session.timeout = 30
    
    print("🚀 QUICK ENHANCED MEAL PLANNER TEST")
    print("=" * 50)
    
    # Step 1: Authenticate
    print("🔐 Authenticating...")
    login_data = {"email": "demo@babysteps.com", "password": "demo123"}
    
    try:
        response = session.post(f"{API_BASE}/auth/login", json=login_data, timeout=30)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            session.headers.update({'Authorization': f"Bearer {token}"})
            print("✅ Authentication successful")
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    # Step 2: Test the specific queries from review request
    test_queries = [
        {"query": "breakfast ideas for 8 month old", "baby_age_months": 8},
        {"query": "finger food recipes", "baby_age_months": 9},
        {"query": "family meal ideas baby can share", "baby_age_months": 12},
        {"query": "lunch recipes for 10 month old", "baby_age_months": 10}
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Testing Query {i}: '{query['query']}'")
        
        try:
            response = session.post(f"{API_BASE}/meals/search", json=query, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                result_text = data.get('results', '')
                
                # Analyze the response
                analysis = {
                    'query': query['query'],
                    'age_months': query['baby_age_months'],
                    'response_length': len(result_text),
                    'has_detailed_instructions': any(word in result_text.lower() for word in ['step', 'cook', 'bake', 'heat', 'temperature', 'minutes']),
                    'has_ingredients_with_measurements': any(word in result_text.lower() for word in ['cup', 'tbsp', 'tsp', 'oz', '1/2', '1/4']),
                    'has_safety_guidelines': any(word in result_text.lower() for word in ['safe', 'supervise', 'caution', 'choke', 'small pieces']),
                    'has_storage_info': any(word in result_text.lower() for word in ['store', 'refrigerate', 'freeze', 'reheat', 'leftover']),
                    'has_age_modifications': any(word in result_text.lower() for word in ['month', 'age', 'appropriate', 'texture', 'soft', 'chunky']),
                    'is_detailed_not_generic': len(result_text) > 500 and not any(word in result_text.lower() for word in ['consult your pediatrician', 'unable to provide', 'sorry, i cannot'])
                }
                
                results.append(analysis)
                
                # Score the response
                score = sum([
                    analysis['has_detailed_instructions'],
                    analysis['has_ingredients_with_measurements'],
                    analysis['has_safety_guidelines'],
                    analysis['has_storage_info'],
                    analysis['has_age_modifications'],
                    analysis['is_detailed_not_generic']
                ])
                
                print(f"   📊 Response length: {analysis['response_length']} characters")
                print(f"   📝 Detailed instructions: {'✅' if analysis['has_detailed_instructions'] else '❌'}")
                print(f"   🥄 Ingredients with measurements: {'✅' if analysis['has_ingredients_with_measurements'] else '❌'}")
                print(f"   ⚠️ Safety guidelines: {'✅' if analysis['has_safety_guidelines'] else '❌'}")
                print(f"   📦 Storage information: {'✅' if analysis['has_storage_info'] else '❌'}")
                print(f"   👶 Age modifications: {'✅' if analysis['has_age_modifications'] else '❌'}")
                print(f"   🎯 Detailed (not generic): {'✅' if analysis['is_detailed_not_generic'] else '❌'}")
                print(f"   🏆 Enhancement Score: {score}/6")
                
                # Show a preview of the response
                preview = result_text[:300] + "..." if len(result_text) > 300 else result_text
                print(f"   📄 Preview: {preview}")
                
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                results.append({'query': query['query'], 'error': f"HTTP {response.status_code}"})
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({'query': query['query'], 'error': str(e)})
    
    # Summary
    print(f"\n📊 ENHANCED MEAL PLANNER TEST SUMMARY")
    print("=" * 50)
    
    successful_queries = [r for r in results if 'error' not in r]
    failed_queries = [r for r in results if 'error' in r]
    
    print(f"✅ Successful queries: {len(successful_queries)}/{len(test_queries)}")
    print(f"❌ Failed queries: {len(failed_queries)}/{len(test_queries)}")
    
    if successful_queries:
        # Calculate average enhancement score
        total_score = 0
        feature_counts = {
            'detailed_instructions': 0,
            'ingredients_measurements': 0,
            'safety_guidelines': 0,
            'storage_info': 0,
            'age_modifications': 0,
            'detailed_not_generic': 0
        }
        
        for result in successful_queries:
            if result.get('has_detailed_instructions'): feature_counts['detailed_instructions'] += 1
            if result.get('has_ingredients_with_measurements'): feature_counts['ingredients_measurements'] += 1
            if result.get('has_safety_guidelines'): feature_counts['safety_guidelines'] += 1
            if result.get('has_storage_info'): feature_counts['storage_info'] += 1
            if result.get('has_age_modifications'): feature_counts['age_modifications'] += 1
            if result.get('is_detailed_not_generic'): feature_counts['detailed_not_generic'] += 1
        
        print(f"\n🎯 ENHANCEMENT FEATURES ANALYSIS:")
        print(f"   📝 Detailed step-by-step instructions: {feature_counts['detailed_instructions']}/{len(successful_queries)} queries")
        print(f"   🥄 Complete ingredient lists with measurements: {feature_counts['ingredients_measurements']}/{len(successful_queries)} queries")
        print(f"   ⚠️ Safety guidelines and serving suggestions: {feature_counts['safety_guidelines']}/{len(successful_queries)} queries")
        print(f"   📦 Storage and freezing instructions: {feature_counts['storage_info']}/{len(successful_queries)} queries")
        print(f"   👶 Age-appropriate modifications: {feature_counts['age_modifications']}/{len(successful_queries)} queries")
        print(f"   🎯 Detailed recipe-focused results: {feature_counts['detailed_not_generic']}/{len(successful_queries)} queries")
        
        # Overall assessment
        total_features = sum(feature_counts.values())
        max_features = len(successful_queries) * 6
        enhancement_percentage = (total_features / max_features) * 100 if max_features > 0 else 0
        
        print(f"\n🏆 OVERALL ENHANCEMENT SUCCESS: {enhancement_percentage:.1f}%")
        
        if enhancement_percentage >= 80:
            print("✅ EXCELLENT: Enhanced meal planner is working as expected!")
        elif enhancement_percentage >= 60:
            print("⚠️ GOOD: Most enhancement features are working, minor improvements needed")
        else:
            print("❌ NEEDS WORK: Enhancement features need significant improvement")
    
    # Save results
    with open('/app/quick_meal_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: quick_meal_test_results.json")

if __name__ == "__main__":
    test_enhanced_meal_planner()