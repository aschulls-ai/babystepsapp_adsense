# Google Play Store Setup Guide

## 🚀 Your Baby Steps App is Ready for Google Play!

### 📦 What You'll Get:
- **✅ SIGNED AAB file** (`app-release.aab`) - Ready for upload to Google Play Console
- **🔐 Upload keystore** (`release.keystore`) - Keep this safe for future updates
- **📋 Mapping files** (for crash debugging)

### 🔐 Keystore Information:
```
Keystore: release.keystore
Store Password: babysteps2024
Key Alias: babysteps
Key Password: babysteps2024
```

## 📋 Google Play Console Upload Steps:

### 1. **First Time Setup (Google Play App Signing)**
1. Go to [Google Play Console](https://play.google.com/console)
2. Create a new app or select existing app
3. Navigate to **Release > Setup > App signing**
4. Choose **"Let Google manage and protect your app signing key"** (Recommended)
5. Upload your SIGNED AAB file - Google Play will accept it now!

### 2. **Upload Your AAB**
1. Go to **Release > Production**
2. Click **"Create new release"**
3. Upload the `app-release.aab` file from GitHub Actions artifacts
4. Fill in release notes and version information
5. Save and review

### 3. **Complete Store Listing**
1. **Store listing**: Add descriptions, screenshots, graphics
2. **Content rating**: Complete the questionnaire
3. **Target audience**: Set age requirements
4. **Privacy policy**: Add your privacy policy URL
5. **App content**: Declare app contents and permissions

### 4. **Submit for Review**
1. Complete all required sections
2. Submit app for review
3. Wait for Google's approval (usually 1-3 days)

## 🔒 Security Notes:
- **Keep your upload keystore safe** (`release.keystore`) - Store it securely
- **Google Play App Signing** manages your production signing key
- The upload keystore is used only for uploading updates
- Never share your keystore passwords publicly

## 🆘 If You Lose Your Upload Keystore:
With Google Play App Signing enabled, you can:
1. Contact Google Play support to reset your upload key
2. Generate a new upload keystore 
3. Continue updating your app

## 📱 App Details:
- **App Name**: Baby Steps
- **Package**: com.babysteps.app  
- **Features**: Baby tracking, nutrition guidance, offline support, push notifications
- **Target SDK**: Android 14 (API level 35)
- **Minimum SDK**: Android 6.0 (API level 23)

## ✅ Ready for Production!
Your Baby Steps app includes:
- ✅ Professional parenting features
- ✅ Mobile-optimized UI
- ✅ Offline data storage
- ✅ Push notifications ready
- ✅ Signed and ready for Google Play