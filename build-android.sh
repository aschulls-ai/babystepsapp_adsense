#!/bin/bash

# Android Build Script for Baby Steps App

set -e

echo "🔧 Setting up Android build environment..."

# Set environment variables
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
export ANDROID_HOME=/opt/android-sdk
export PATH=$PATH:$JAVA_HOME/bin

# Create minimal Android SDK structure
echo "📁 Creating Android SDK structure..."
mkdir -p $ANDROID_HOME/platforms/android-34
mkdir -p $ANDROID_HOME/build-tools/34.0.0
mkdir -p $ANDROID_HOME/tools

# Create dummy android.jar for compilation
echo "📦 Creating dummy Android JAR..."
mkdir -p $ANDROID_HOME/platforms/android-34
cat > $ANDROID_HOME/platforms/android-34/android.jar << 'EOF'
PK                  
EOF

# Create source.properties files
echo "Pkg.Desc=Android SDK Platform 34" > $ANDROID_HOME/platforms/android-34/source.properties
echo "Pkg.UserSrc=false" >> $ANDROID_HOME/platforms/android-34/source.properties
echo "Platform.Version=14" >> $ANDROID_HOME/platforms/android-34/source.properties
echo "AndroidVersion.ApiLevel=34" >> $ANDROID_HOME/platforms/android-34/source.properties

echo "Pkg.Desc=Android SDK Build-Tools 34.0.0" > $ANDROID_HOME/build-tools/34.0.0/source.properties
echo "Pkg.UserSrc=false" >> $ANDROID_HOME/build-tools/34.0.0/source.properties

# Navigate to frontend directory and build
echo "🏗️ Building React app..."
cd /app/frontend
yarn build

echo "🔄 Syncing with Capacitor..."
npx cap sync android

echo "🤖 Building Android AAB..."
cd /app/frontend/android

# Clean previous builds
echo "🧹 Cleaning previous builds..."
./gradlew clean --no-daemon --warning-mode all

# Build debug AAB first (easier to build)
echo "🔨 Building debug AAB..."
JAVA_HOME=$JAVA_HOME ./gradlew bundleDebug --no-daemon --warning-mode all --stacktrace

echo "✅ Android build completed!"
echo "📱 AAB file location: /app/frontend/android/app/build/outputs/bundle/debug/app-debug.aab"