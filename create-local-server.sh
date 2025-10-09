#!/bin/bash

# Create a local server that can be exposed via ngrok
# This bypasses any Render connectivity issues

echo "🏠 Setting up Local Demo Server"
echo "=============================="

cd /app/public-server

# Start local server in background
echo "🚀 Starting local server on port 8080..."
python -m uvicorn app:app --host 0.0.0.0 --port 8080 > local-server.log 2>&1 &
LOCAL_PID=$!

sleep 3

# Test local server
if curl -s http://localhost:8080/api/health > /dev/null; then
    echo "✅ Local server running successfully"
    echo "📋 Server details:"
    echo "   - URL: http://localhost:8080"
    echo "   - PID: $LOCAL_PID"
    echo "   - Log: /app/public-server/local-server.log"
    
    echo ""
    echo "🌐 To expose publicly:"
    echo "===================="
    echo "Option 1 - Install ngrok:"
    echo "  1. Download: https://ngrok.com/download"
    echo "  2. Run: ngrok http 8080"
    echo "  3. Use the https URL provided"
    echo ""
    echo "Option 2 - Use Cloudflare Tunnel:"
    echo "  1. Install: npm install -g cloudflared"
    echo "  2. Run: cloudflared tunnel --url http://localhost:8080"
    echo ""
    echo "Option 3 - Use LocalTunnel:"
    echo "  1. Install: npm install -g localtunnel"
    echo "  2. Run: lt --port 8080 --subdomain babysteps"
    echo ""
    echo "📱 Demo Credentials:"
    echo "==================="
    echo "Email: demo@babysteps.com"
    echo "Password: demo123"
    
else
    echo "❌ Local server failed to start"
    echo "Check logs: cat /app/public-server/local-server.log"
fi