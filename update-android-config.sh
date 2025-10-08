#!/bin/bash

# Update Android App Configuration for Demo Server
# Usage: ./update-android-config.sh <SERVER_URL>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <SERVER_URL>"
    echo "Example: $0 https://baby-steps-demo.vercel.app"
    exit 1
fi

SERVER_URL="$1"

echo "🔧 Updating Android App Configuration"
echo "====================================="
echo "Server URL: $SERVER_URL"
echo ""

# Update Capacitor config
echo "📱 Updating Capacitor configuration..."
cat > frontend/capacitor.config.json << EOF
{
  "appId": "com.babysteps.app",
  "appName": "Baby Steps",
  "webDir": "build",
  "server": {
    "url": "$SERVER_URL",
    "cleartext": false,
    "androidScheme": "https"
  },
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

echo "✅ Capacitor config updated"

# Update production environment
echo "🌐 Updating production environment..."
cat > frontend/.env.production << EOF
REACT_APP_BACKEND_URL=$SERVER_URL
REACT_APP_ADSENSE_CLIENT_ID=ca-pub-1934622676928053
GENERATE_SOURCEMAP=false
CI=false
EOF

echo "✅ Production environment updated"

# Update local environment for testing
echo "🔧 Updating local environment..."
cp frontend/.env.production frontend/.env.local

echo "✅ Local environment updated"

echo ""
echo "🚀 Next Steps:"
echo "=============="
echo "1. Rebuild React app:"
echo "   cd frontend && yarn build"
echo ""
echo "2. Sync Capacitor:"
echo "   npx cap sync android"
echo ""
echo "3. Build Android AAB:"
echo "   Run GitHub Actions 'Build Baby Steps Android' workflow"
echo ""
echo "4. Test connection:"
echo "   curl $SERVER_URL/api/health"
echo ""
echo "📱 Demo Credentials:"
echo "==================="
echo "Email: demo@babysteps.com"
echo "Password: demo123"
echo ""
echo "✅ Android app configuration updated successfully!"