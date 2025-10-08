# Mobile App Deployment Guide

This guide covers the deployment process for both Android (.aab) and iOS (.ipa) builds of the Baby Steps app.

## 🤖 Android Deployment (.aab for Google Play)

### Automatic Build via GitHub Actions

The Android build is fully automated through GitHub Actions. The workflow generates a signed .aab file ready for Google Play Console.

#### To trigger a build:

1. **Push to main branch** - Automatically builds .aab
2. **Manual trigger** - Go to Actions → "Build Baby Steps Android App" → Run workflow
3. **Create a release tag** - `git tag v1.0.0 && git push origin v1.0.0`

#### Build outputs:
- **app-release.aab** - Upload this to Google Play Console
- **app-release.apk** - For direct installation/testing
- **Keystore file** - Automatically generated and included

### Google Play Console Upload

1. Download the `.aab` file from GitHub Actions artifacts
2. Go to [Google Play Console](https://play.google.com/console)
3. Select your app → Production → Create new release
4. Upload the `.aab` file
5. Complete the release process

### Current Configuration

- **App ID**: `com.babysteps.app`
- **Version**: Auto-incremented based on build number
- **Signing**: Automatically handled with generated keystore
- **API URL**: Points to `https://babystepsapp.app/api` in production builds

## 📱 iOS Deployment (.ipa for App Store)

### GitHub Actions Setup

The iOS build workflow is configured but requires Apple Developer account setup.

#### Required GitHub Secrets

Add these secrets in your repository settings (Settings → Secrets and variables → Actions):

```
APPLE_TEAM_ID=YOUR_TEAM_ID
APPLE_ID=your-apple-id@email.com
APPLE_APP_PASSWORD=your-app-specific-password
```

#### To get these values:

1. **APPLE_TEAM_ID**:
   - Go to [Apple Developer Account](https://developer.apple.com/account/)
   - Navigate to Membership → Team ID

2. **APPLE_ID**:
   - Your Apple ID email address

3. **APPLE_APP_PASSWORD**:
   - Go to [Apple ID Account](https://appleid.apple.com/)
   - Sign-In and Security → App-Specific Passwords
   - Generate a new password for "GitHub Actions"

#### Additional Setup Required

1. **Add iOS platform** (if not already done):
   ```bash
   cd frontend
   npx cap add ios
   ```

2. **Configure signing in Xcode**:
   - Open `frontend/ios/App/App.xcworkspace` in Xcode
   - Select the App target → Signing & Capabilities
   - Set your Team and Bundle Identifier

3. **Provisioning Profiles**:
   - Create App Store provisioning profile in Apple Developer Console
   - Download and install on your development machine

### Manual iOS Build (Alternative)

If you prefer to build locally:

```bash
cd frontend
npm run build
npx cap sync ios
npx cap open ios
```

Then build and archive in Xcode:
1. Product → Archive
2. Distribute App → App Store Connect
3. Upload to App Store Connect

## 🔧 Environment Configuration

### Production API Configuration

The app automatically uses the production API (`https://babystepsapp.app/api`) when built for production.

Environment files:
- `.env.production` - Production configuration
- Default development uses relative paths (`/api`)

### Server Requirements

Ensure your production server at `babystepsapp.app` has:
- ✅ HTTPS enabled
- ✅ CORS configured for mobile app
- ✅ All API endpoints functional
- ✅ Database connectivity

## 🚀 Deployment Checklist

### Before Building:

- [ ] Test app functionality locally
- [ ] Verify API connectivity to production server
- [ ] Update version numbers if needed
- [ ] Test authentication flow
- [ ] Verify push notifications (if implemented)

### Android (.aab):

- [ ] Trigger GitHub Actions build
- [ ] Download .aab artifact
- [ ] Upload to Google Play Console
- [ ] Complete Play Console release process
- [ ] Test on Google Play Internal Testing

### iOS (.ipa):

- [ ] Configure GitHub secrets
- [ ] Set up Apple Developer certificates
- [ ] Trigger GitHub Actions build
- [ ] Download .ipa artifact
- [ ] Upload to App Store Connect via Transporter or Xcode
- [ ] Complete App Store review process

## 🐛 Troubleshooting

### Android Build Issues:

1. **Gradle build fails**:
   - Check Java version (should be 21)
   - Clear Gradle cache: `./gradlew clean`

2. **Signing issues**:
   - Keystore is auto-generated in GitHub Actions
   - For local builds, create keystore manually

3. **App not loading on device**:
   - Check API URL configuration
   - Verify CORS settings on server
   - Check network connectivity

### iOS Build Issues:

1. **Code signing errors**:
   - Verify Apple Developer account setup
   - Check provisioning profiles
   - Ensure certificates are valid

2. **Archive fails**:
   - Update Xcode to latest version
   - Clean build folder: Product → Clean Build Folder

3. **Upload to App Store fails**:
   - Verify app-specific password
   - Check bundle identifier matches App Store Connect

## 📞 Support

If you encounter issues:

1. Check GitHub Actions logs for detailed error messages
2. Verify all secrets and certificates are properly configured
3. Test the web version first to isolate mobile-specific issues
4. Check server logs for API connectivity issues

## 🔄 Continuous Deployment

The current setup supports:
- ✅ Automatic Android builds on push to main
- ✅ Manual trigger for both platforms
- ✅ Version management and artifact storage
- ✅ Release creation with downloadable files

For fully automated deployment to stores, additional configuration of store APIs would be required.