#!/bin/bash

# Wake up the Render server and test connectivity
echo "🌐 Waking up Baby Steps Demo Server"
echo "=================================="

SERVER_URL="https://baby-steps-demo-api.onrender.com"

echo "📡 Pinging server to wake up..."
for i in {1..3}; do
    echo "Attempt $i/3..."
    RESPONSE=$(curl -s -w "%{http_code}" "$SERVER_URL/api/health")
    HTTP_CODE="${RESPONSE: -3}"
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Server is awake and responding"
        break
    else
        echo "⏳ Waiting for server to wake up... (HTTP: $HTTP_CODE)"
        sleep 5
    fi
done

echo ""
echo "🧪 Testing API endpoints..."

# Test health
echo "Health check:"
curl -s "$SERVER_URL/api/health"
echo ""

# Test login
echo "Login test:"
curl -s -X POST "$SERVER_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}' | head -c 100
echo "..."

echo ""
echo "✅ Server is ready for Android app!"
echo "📱 Try logging in to the app now with:"
echo "   Email: demo@babysteps.com"
echo "   Password: demo123"