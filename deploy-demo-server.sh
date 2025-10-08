#!/bin/bash

# Baby Steps Demo Server Deployment Script
# Deploys the demo server to Vercel for public access

set -e

echo "🌐 Baby Steps Demo Server Deployment"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "public-server/app.py" ]; then
    echo "❌ Please run this script from the /app directory"
    exit 1
fi

cd public-server

echo "📋 Server files:"
ls -la

echo ""
echo "🔍 Verifying server configuration..."

# Check if required files exist
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found"
    exit 1
fi

echo "✅ All required files present"

# Test server locally first
echo ""
echo "🧪 Testing server locally..."
python -m uvicorn app:app --host 127.0.0.1 --port 8081 > test.log 2>&1 &
SERVER_PID=$!

sleep 3

# Test endpoints
if curl -s http://127.0.0.1:8081/ > /dev/null; then
    echo "✅ Server responds to health check"
else
    echo "❌ Server not responding"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Test login endpoint
LOGIN_RESPONSE=$(curl -s -X POST http://127.0.0.1:8081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}')

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo "✅ Authentication endpoint working"
else
    echo "❌ Authentication failed"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Clean up test server
kill $SERVER_PID 2>/dev/null

echo ""
echo "🚀 Deployment Options:"
echo "===================="
echo ""
echo "Option 1 - Vercel (Recommended):"
echo "  npm install -g vercel"
echo "  vercel --prod"
echo ""
echo "Option 2 - Railway:"
echo "  1. Go to https://railway.app"
echo "  2. Connect GitHub and deploy this folder"
echo ""
echo "Option 3 - Render:"
echo "  1. Go to https://render.com"  
echo "  2. Create web service from GitHub"
echo "  3. Build: pip install -r requirements.txt"
echo "  4. Start: uvicorn app:app --host 0.0.0.0 --port \$PORT"
echo ""

# Check if Vercel is available
if command -v vercel &> /dev/null; then
    echo "🎯 Vercel CLI detected. Deploy now? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Deploying to Vercel..."
        vercel --prod --yes
        echo ""
        echo "✅ Deployment completed!"
        echo "🔗 Use the Vercel URL to update your Android app configuration"
    fi
else
    echo "💡 Install Vercel CLI for one-command deployment:"
    echo "   npm install -g vercel"
fi

echo ""
echo "📱 Next Steps:"
echo "============="
echo "1. Copy your deployment URL"
echo "2. Update frontend/capacitor.config.json server.url"
echo "3. Update frontend/.env.production REACT_APP_BACKEND_URL"  
echo "4. Rebuild Android app: yarn build && npx cap sync android"
echo "5. Test Android app with new server"
echo ""
echo "🎉 Demo server ready for Android app testing!"