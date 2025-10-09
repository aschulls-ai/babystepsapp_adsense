#!/bin/bash

# Deploy Baby Steps Demo Server to Render
# This script prepares files and provides deployment instructions

echo "🌐 Render Deployment Preparation"
echo "==============================="

cd public-server

# Verify all files are ready
echo "📋 Checking required files..."

REQUIRED_FILES=("app.py" "requirements.txt" "render.yaml" "README.md")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

echo ""
echo "🧪 Testing server locally..."

# Start test server
python -m uvicorn app:app --host 127.0.0.1 --port 8082 > render-test.log 2>&1 &
SERVER_PID=$!

sleep 4

# Test health endpoint
if curl -s http://127.0.0.1:8082/api/health | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Test login
LOGIN_TEST=$(curl -s -X POST http://127.0.0.1:8082/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}')

if echo "$LOGIN_TEST" | grep -q "access_token"; then
    echo "✅ Authentication working"
else
    echo "❌ Authentication failed"
    echo "Response: $LOGIN_TEST"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Clean up test server
kill $SERVER_PID 2>/dev/null

echo ""
echo "🚀 Ready for Render Deployment!"
echo "=============================="
echo ""
echo "📋 Deployment Settings:"
echo "----------------------"
echo "Build Command: pip install -r requirements.txt"
echo "Start Command: uvicorn app:app --host 0.0.0.0 --port \$PORT"
echo "Health Check:  /api/health"
echo "Environment:   Python 3"
echo ""
echo "🔗 Manual Deployment Steps:"
echo "1. Go to https://render.com"
echo "2. Create account (free)"
echo "3. New → Web Service"
echo "4. Upload this folder OR connect GitHub"
echo "5. Use the settings above"
echo "6. Deploy!"
echo ""
echo "📱 Demo Credentials:"
echo "Email: demo@babysteps.com"
echo "Password: demo123"
echo ""

# Create deployment package
echo "📦 Creating deployment package..."
cd ..
tar -czf baby-steps-demo-server.tar.gz public-server/ --exclude="public-server/__pycache__" --exclude="public-server/*.log"
echo "✅ Created: baby-steps-demo-server.tar.gz"
echo ""
echo "💡 You can upload this tar.gz file to Render if not using GitHub"
echo ""
echo "🎯 After deployment, run:"
echo "./update-android-config.sh https://YOUR-RENDER-URL"
echo ""
echo "🎉 Ready to deploy to Render!"