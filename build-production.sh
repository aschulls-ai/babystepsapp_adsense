#!/bin/bash

# Baby Steps - Production Build Script
echo "🚀 Starting Baby Steps production build..."

# Set environment to production
export NODE_ENV=production

# Copy production environment variables
echo "📋 Configuring production environment..."
cp .env.production frontend/.env.production

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
yarn install --frozen-lockfile

# Build the React app with production settings
echo "🔨 Building React application..."
REACT_APP_BACKEND_URL=https://babystepsapp.app/api \
REACT_APP_ADSENSE_CLIENT_ID=ca-pub-1934622676928053 \
GENERATE_SOURCEMAP=false \
yarn build

# Sync with Capacitor
echo "🔄 Syncing with Capacitor..."
npx cap sync

# Build Android AAB
echo "📱 Building Android App Bundle (.aab)..."
cd android
./gradlew bundleRelease

# Build Android APK (for testing)
echo "📱 Building Android APK (.apk)..."
./gradlew assembleRelease

echo "✅ Production build complete!"
echo "📁 Android AAB file: frontend/android/app/build/outputs/bundle/release/app-release.aab"
echo "📁 Android APK file: frontend/android/app/build/outputs/apk/release/app-release.apk"

# Verify the build
echo "🔍 Verifying build..."
if [ -f "app/build/outputs/bundle/release/app-release.aab" ]; then
    echo "✅ AAB file generated successfully"
    ls -la app/build/outputs/bundle/release/app-release.aab
else
    echo "❌ AAB file not found"
    exit 1
fi

echo "🎉 Baby Steps is ready for Google Play Store!"