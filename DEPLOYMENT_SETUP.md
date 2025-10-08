# Baby Steps - Production Deployment Setup

## Overview
This document covers the complete setup for deploying Baby Steps to production, including Google Play Store (.aab) and Apple App Store (.ipa) builds.

## 🔧 Production Configuration

### Server Configuration
- **Production URL**: `https://babystepsapp.app`
- **API Endpoint**: `https://babystepsapp.app/api`
- **Frontend URL**: `https://babystepsapp.app`

### Environment Variables (Required for production)
```env
REACT_APP_BACKEND_URL=https://babystepsapp.app/api
REACT_APP_ADSENSE_CLIENT_ID=ca-pub-1934622676928053
GENERATE_SOURCEMAP=false
CI=false
```

## 📱 Android (.aab) Setup for Google Play

### Prerequisites
1. Android Studio installed
2. Java JDK 21 or higher
3. Android SDK with API level 35

### Local Build Commands
```bash
# Make the build script executable
chmod +x build-production.sh

# Run production build
./build-production.sh
```

### GitHub Secrets Required for Android
```
ANDROID_SIGNING_KEY_STORE_BASE64=<base64 encoded keystore>
ANDROID_KEY_ALIAS=babysteps
ANDROID_KEY_PASSWORD=babysteps2024
ANDROID_STORE_PASSWORD=babysteps2024
```

### Files Generated
- **AAB**: `frontend/android/app/build/outputs/bundle/release/app-release.aab`
- **APK**: `frontend/android/app/build/outputs/apk/release/app-release.apk`

## 🍎 iOS (.ipa) Setup for App Store

### Prerequisites
1. macOS with Xcode (latest stable)
2. Apple Developer Account
3. iOS Provisioning Profiles
4. Code Signing Certificates

### GitHub Secrets Required for iOS
```
# Apple Developer Account
APPLE_ID_EMAIL=your-apple-id@example.com
APPLE_ID_PASSWORD=app-specific-password

# App Store Connect API (Recommended)
APPSTORE_ISSUER_ID=your-issuer-id
APPSTORE_KEY_ID=your-key-id  
APPSTORE_PRIVATE_KEY=your-private-key

# Code Signing
IOS_CERTIFICATES_P12=<base64 encoded p12 certificate>
IOS_CERTIFICATES_PASSWORD=your-certificate-password
APPLE_TEAM_ID=your-team-id

# Legacy (if not using App Store Connect API)
APPLE_APP_PASSWORD=app-specific-password
```

### Manual Build Process
```bash
# Navigate to frontend
cd frontend

# Install dependencies
yarn install

# Configure production environment
echo "REACT_APP_BACKEND_URL=https://babystepsapp.app/api" > .env.production
echo "REACT_APP_ADSENSE_CLIENT_ID=ca-pub-1934622676928053" >> .env.production

# Build React app
yarn build

# Sync Capacitor
npx cap sync ios

# Install iOS dependencies
cd ios/App && pod install && cd ../..

# Open Xcode (manual build)
npx cap open ios
```

## 🚀 GitHub Actions Automation

### Triggering Builds

#### Android Build
```bash
# Automatic trigger on push to main
git push origin main

# Manual trigger
gh workflow run android-build.yml
```

#### iOS Build  
```bash
# Automatic trigger on push to main
git push origin main

# Manual trigger with build type
gh workflow run ios-build.yml -f build_type=production
```

## 🔐 Setting Up GitHub Secrets

### Using GitHub CLI
```bash
# Android secrets
gh secret set ANDROID_SIGNING_KEY_STORE_BASE64 < keystore.b64
gh secret set ANDROID_KEY_ALIAS -b "babysteps"
gh secret set ANDROID_KEY_PASSWORD -b "babysteps2024"
gh secret set ANDROID_STORE_PASSWORD -b "babysteps2024"

# iOS secrets
gh secret set APPLE_ID_EMAIL -b "your-apple-id@example.com"
gh secret set APPSTORE_ISSUER_ID -b "your-issuer-id"
gh secret set APPSTORE_KEY_ID -b "your-key-id"
gh secret set APPSTORE_PRIVATE_KEY < AuthKey.p8
gh secret set IOS_CERTIFICATES_P12 < cert.p12.b64
gh secret set IOS_CERTIFICATES_PASSWORD -b "cert-password"
gh secret set APPLE_TEAM_ID -b "XXXXXXXXXX"
```

### Using GitHub Web Interface
1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret from the list above

## 🛠 Troubleshooting

### Common Android Issues
1. **Keystore not found**: Ensure keystore is generated and secrets are set
2. **Build fails**: Check Java version (must be JDK 21)
3. **Signing errors**: Verify all keystore secrets are correct

### Common iOS Issues
1. **Code signing fails**: Ensure certificates and provisioning profiles are valid
2. **Build timeout**: iOS builds can take 15-20 minutes
3. **Xcode version**: Use latest stable Xcode version

### App Store Upload Issues
1. **Invalid bundle**: Ensure version numbers are incremented
2. **Missing metadata**: Complete App Store Connect listing
3. **Review guidelines**: Follow Apple App Store and Google Play policies

## 📋 Pre-Release Checklist

### Before Building
- [ ] Update version numbers in package.json
- [ ] Test app thoroughly on development environment  
- [ ] Verify all environment variables point to production servers
- [ ] Ensure all secrets are configured in GitHub
- [ ] Test authentication with babystepsapp.app backend

### Before Store Submission
- [ ] Test .aab/.ipa files on physical devices
- [ ] Verify app connects to production API correctly
- [ ] Complete store listings (descriptions, screenshots, metadata)
- [ ] Prepare marketing materials
- [ ] Review and follow store guidelines

## 🎯 Production Deployment Flow

1. **Development** → Push to `main` branch
2. **GitHub Actions** → Automatically builds .aab and .ipa
3. **Quality Assurance** → Test artifacts on devices  
4. **Store Submission** → Upload to Google Play Console / App Store Connect
5. **Review Process** → Wait for store approval
6. **Release** → Apps go live on stores

## 📞 Support
For issues with deployment setup, check:
1. GitHub Actions logs for build errors
2. Store developer consoles for submission issues
3. Device logs for runtime issues with production builds

---
**Last Updated**: December 2024
**Baby Steps Version**: 1.0.0