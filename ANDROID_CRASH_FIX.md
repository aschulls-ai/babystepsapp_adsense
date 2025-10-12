# Android App Crash Fix - Backend URL Mismatch

## 🐛 Issue Identified

Android app crashes on startup with "Baby Steps keeps stopping" error.

### Root Cause

The main `.env` file still pointed to the old **preview backend URL** instead of the **Render production URL**:

```
❌ OLD: https://baby-steps-demo-api.onrender.com
✅ NEW: https://baby-steps-demo-api.onrender.com
```

## ✅ Fix Applied

**File Modified**: `/app/frontend/.env`

```bash
# Changed from:
REACT_APP_BACKEND_URL=https://baby-steps-demo-api.onrender.com

# To:
REACT_APP_BACKEND_URL=https://baby-steps-demo-api.onrender.com
```

## 🔧 Rebuild Required

Since the Android APK was built with the wrong backend URL baked into it, a **complete rebuild** is required:

### Option 1: GitHub Actions (Recommended)

1. **Commit the .env change**:
   ```bash
   git add frontend/.env
   git commit -m "Fix: Update Android backend URL to Render production"
   git push origin main
   ```

2. **Trigger Android Build**:
   - Go to GitHub Actions
   - Run the `android-build.yml` workflow
   - Download the new APK from artifacts

### Option 2: Local Build

1. **Sync Capacitor**:
   ```bash
   cd /app/frontend
   yarn build
   npx cap sync android
   ```

2. **Build APK**:
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

3. **Find APK**:
   ```
   android/app/build/outputs/apk/release/app-release.apk
   ```

## 📋 Verification Checklist

After rebuild, verify these configurations:

✅ **Environment Files**:
- `frontend/.env` → `https://baby-steps-demo-api.onrender.com`
- `frontend/.env.production` → `https://baby-steps-demo-api.onrender.com`
- `frontend/.env.local` → `https://baby-steps-demo-api.onrender.com`

✅ **Android Configs**:
- `android/app/src/main/res/xml/network_security_config.xml` → Allows `onrender.com`
- `capacitor.config.json` → Allows navigation to Render URL

✅ **GitHub Workflow**:
- `.github/workflows/android-build.yml` → Uses Render URL

## 🧪 Testing After Rebuild

1. **Install new APK** on Android device
2. **Open app** - should load without crashing
3. **Check dashboard** - should show demo baby (Emma Johnson)
4. **Test AI Assistant** - ask a question about baby care
5. **Verify network logs** - should see connections to `baby-steps-demo-api.onrender.com`

## 🔍 Debugging (If Still Crashing)

If the app still crashes after rebuild:

1. **Enable USB debugging** on Android device
2. **Connect to computer** and run:
   ```bash
   adb logcat | grep -i babysteps
   ```
3. **Look for error messages** in logcat output
4. **Common issues**:
   - Network permission denied
   - SSL certificate errors
   - API response format mismatches
   - Authentication token issues

## 📊 Expected Behavior

After successful rebuild:
- ✅ App opens without crashing
- ✅ Shows login screen or dashboard
- ✅ Can authenticate with demo credentials (demo@babysteps.com/demo123)
- ✅ AI features work (chat, food research, meal planner)
- ✅ Network requests go to Render production backend

## 🎯 Why This Happened

The Android APK build process bakes the environment variables (including `REACT_APP_BACKEND_URL`) into the compiled JavaScript bundle. When the app was built:

1. Frontend `.env` had old preview URL
2. Build process compiled React app with that URL
3. Capacitor bundled the compiled app into APK
4. APK had hardcoded old URL that doesn't work

**Solution**: Update `.env` → Rebuild → Redeploy

## 📝 Prevention

To avoid this in the future:

1. **Always verify** `.env` files before building Android APK
2. **Use environment-specific** files (`.env.production` for releases)
3. **Test backend URL** is accessible before building
4. **Document** which backend URL each APK version uses
