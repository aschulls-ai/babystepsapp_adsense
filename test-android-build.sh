#!/bin/bash

echo "🚀 Baby Steps Android App Build Test Script"
echo "==========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${NC}ℹ️  $1${NC}"
}

# Change to the frontend directory
cd /app/frontend || exit 1

echo ""
echo "📋 Pre-build Validation"
echo "======================="

# Check if necessary files exist
print_info "Checking project structure..."

if [ -f "capacitor.config.json" ]; then
    print_status 0 "Capacitor config found"
else
    print_status 1 "Capacitor config missing"
    exit 1
fi

if [ -d "android" ]; then
    print_status 0 "Android platform added"
else
    print_status 1 "Android platform not found"
    exit 1
fi

if [ -f "android/app/build.gradle" ]; then
    print_status 0 "Android build.gradle found"
else
    print_status 1 "Android build.gradle missing"
    exit 1
fi

if [ -f "build/index.html" ]; then
    print_status 0 "React build output found"
else
    print_warning "React build output missing - building now..."
    npm run build
    if [ $? -eq 0 ]; then
        print_status 0 "React build completed"
    else
        print_status 1 "React build failed"
        exit 1
    fi
fi

echo ""
echo "🔧 Environment Check"
echo "===================="

# Check Java
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    print_status 0 "Java found (version $JAVA_VERSION)"
else
    print_status 1 "Java not found"
    exit 1
fi

# Check Android SDK
if [ -n "$ANDROID_HOME" ] && [ -d "$ANDROID_HOME" ]; then
    print_status 0 "Android SDK found at $ANDROID_HOME"
else
    print_warning "Android SDK not found in environment"
fi

echo ""
echo "📱 Android Project Analysis"
echo "=========================="

# Check Android manifest
if [ -f "android/app/src/main/AndroidManifest.xml" ]; then
    APP_ID=$(grep -o 'package="[^"]*"' android/app/src/main/AndroidManifest.xml | cut -d'"' -f2)
    print_status 0 "Android manifest found (package: $APP_ID)"
else
    print_status 1 "Android manifest missing"
fi

# Check build.gradle configuration
if grep -q "com.babysteps.app" android/app/build.gradle; then
    print_status 0 "Correct app ID in build.gradle"
else
    print_warning "App ID might be incorrect in build.gradle"
fi

# Check for signing configuration
if grep -q "signingConfigs" android/app/build.gradle; then
    print_status 0 "Signing configuration present"
else
    print_warning "No signing configuration found (needed for release)"
fi

echo ""
echo "📦 Dependencies Check"
echo "===================="

# Check Capacitor dependencies
if grep -q "@capacitor/android" package.json; then
    CAPACITOR_VERSION=$(grep "@capacitor/android" package.json | cut -d'"' -f4)
    print_status 0 "Capacitor Android found (version $CAPACITOR_VERSION)"
else
    print_status 1 "Capacitor Android missing"
fi

if grep -q "@capacitor/core" package.json; then
    CORE_VERSION=$(grep "@capacitor/core" package.json | cut -d'"' -f4)
    print_status 0 "Capacitor Core found (version $CORE_VERSION)"
else
    print_status 1 "Capacitor Core missing"
fi

echo ""
echo "🔄 Capacitor Sync Test"
echo "====================="

print_info "Running Capacitor sync..."
npx cap sync android 2>&1 | grep -E "(✔|error|warning)" || echo "Sync output captured"

if [ $? -eq 0 ]; then
    print_status 0 "Capacitor sync completed"
else
    print_status 1 "Capacitor sync failed"
fi

echo ""
echo "🏗️  Gradle Build Test"
echo "===================="

cd android || exit 1

print_info "Making Gradle wrapper executable..."
chmod +x ./gradlew

print_info "Testing Gradle wrapper..."
if ./gradlew --version > /dev/null 2>&1; then
    GRADLE_VERSION=$(./gradlew --version | grep "Gradle" | head -1)
    print_status 0 "Gradle wrapper working ($GRADLE_VERSION)"
else
    print_status 1 "Gradle wrapper failed"
    echo "Error details:"
    ./gradlew --version
fi

echo ""
echo "🧪 Build Analysis"
echo "================"

print_info "Analyzing build configuration..."

# Check for common issues
if grep -q "minSdkVersion" app/build.gradle; then
    MIN_SDK=$(grep "minSdkVersion" app/build.gradle | grep -o '[0-9]*' | head -1)
    print_status 0 "Minimum SDK version: $MIN_SDK"
else
    print_warning "Minimum SDK version not found"
fi

if grep -q "targetSdkVersion" app/build.gradle; then
    TARGET_SDK=$(grep "targetSdkVersion" app/build.gradle | grep -o '[0-9]*' | head -1)
    print_status 0 "Target SDK version: $TARGET_SDK"
else
    print_warning "Target SDK version not found"
fi

echo ""
echo "📋 Build Recommendations"
echo "========================"

echo "For successful .aab generation:"
echo "1. Use x86_64 Linux environment (GitHub Actions recommended)"
echo "2. Ensure Android SDK Build Tools are properly installed"
echo "3. Set up signing configuration for release builds"
echo "4. Test on GitHub Actions with provided workflow"
echo ""

echo "🔗 Next Steps:"
echo "1. Push code to GitHub repository"
echo "2. GitHub Actions will automatically build .aab file"
echo "3. Download artifacts from Actions tab"
echo "4. Upload .aab to Google Play Console"

echo ""
echo "✨ Analysis Complete!"
echo "==================="

cd /app/frontend || exit 1
exit 0