#!/bin/bash

# Test Android-specific connection issues
echo "🔍 Testing Android Connection Issues"
echo "===================================="

SERVER_URL="https://baby-steps-demo-api.onrender.com"

echo "Test 1: Basic connection with Android headers"
echo "============================================="
curl -v -X POST "$SERVER_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36" \
  -H "Accept: application/json" \
  -H "Origin: file://" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}' 2>&1 | grep -E "(HTTP|Access-Control|error|denied)"

echo ""
echo "Test 2: CORS preflight check"
echo "============================"
curl -v -X OPTIONS "$SERVER_URL/api/auth/login" \
  -H "Origin: file://" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type,Authorization" 2>&1 | grep -E "(HTTP|Access-Control|error|denied)"

echo ""
echo "Test 3: Health check with mobile headers"
echo "========================================"
curl -s -X GET "$SERVER_URL/api/health" \
  -H "User-Agent: BabyStepsApp/1.0 (Android)" \
  -H "Accept: application/json"

echo ""
echo "Test 4: Different User-Agent strings"
echo "===================================="

USER_AGENTS=(
    "BabyStepsApp/1.0 Android"
    "Mozilla/5.0 (Linux; Android 11)"
    "okhttp/4.9.0"
    "Apache-HttpClient/4.5.13"
)

for ua in "${USER_AGENTS[@]}"; do
    echo "Testing with User-Agent: $ua"
    RESPONSE=$(curl -s -w "%{http_code}" -X GET "$SERVER_URL/api/health" -H "User-Agent: $ua" -o /dev/null)
    echo "Response code: $RESPONSE"
done

echo ""
echo "Test 5: Check if server blocks certain requests"
echo "=============================================="
curl -s -X POST "$SERVER_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BabyStepsApp/1.0 Android" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}' | head -c 100