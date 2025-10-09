#!/bin/bash

# Fix Android App Configuration 
# This ensures the app uses local React build with remote API server

echo "🔧 Fixing Android App Configuration"
echo "=================================="

# Update Capacitor config to use local build (not remote server)
cat > frontend/capacitor.config.json << 'EOF'
{
  "appId": "com.babysteps.app",
  "appName": "Baby Steps",
  "webDir": "build",
  "plugins": {
    "PushNotifications": {
      "presentationOptions": ["badge", "sound", "alert"]
    },
    "LocalNotifications": {
      "smallIcon": "ic_stat_icon_config_sample",
      "iconColor": "#488AFF",
      "sound": "beep.wav"
    },
    "SplashScreen": {
      "launchShowDuration": 3000,
      "launchAutoHide": true,
      "backgroundColor": "#10b981",
      "androidSplashResourceName": "splash",
      "androidScaleType": "CENTER_CROP"
    },
    "StatusBar": {
      "style": "LIGHT_CONTENT",
      "backgroundColor": "#10b981"
    },
    "Keyboard": {
      "resize": "body",
      "style": "dark",
      "resizeOnFullScreen": true
    }
  },
  "android": {
    "allowMixedContent": true,
    "captureInput": true,
    "webContentsDebuggingEnabled": false
  }
}
EOF

echo "✅ Capacitor config updated (local build mode)"

# Ensure production environment points to demo server for API calls
cat > frontend/.env.production << 'EOF'
REACT_APP_BACKEND_URL=https://baby-steps-demo-api.onrender.com
REACT_APP_ADSENSE_CLIENT_ID=ca-pub-1934622676928053
GENERATE_SOURCEMAP=false
CI=false
EOF

echo "✅ Production environment configured for demo server API"

# Update local env for testing
cp frontend/.env.production frontend/.env.local

echo "✅ Local environment synced"

echo ""
echo "🚀 Next Steps:"
echo "=============="
echo "1. Build React app:"
echo "   cd frontend && yarn build"
echo ""
echo "2. Sync Capacitor:"
echo "   npx cap sync android"
echo ""
echo "3. Build Android AAB:"
echo "   Run GitHub Actions workflow"
echo ""
echo "4. Install and test new AAB"
echo ""
echo "📋 How This Works:"
echo "=================="
echo "✅ App UI: Served locally from React build"
echo "✅ API calls: Made to https://baby-steps-demo-api.onrender.com"
echo "✅ Demo data: Available via server API"
echo "✅ Offline capability: React app works without internet"
echo ""
echo "🔑 Demo Credentials:"
echo "==================="
echo "Email: demo@babysteps.com"
echo "Password: demo123"
echo ""
echo "✅ Android app configuration fixed!"