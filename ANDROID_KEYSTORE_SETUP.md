# 🔐 Android Keystore Setup Guide

This guide explains how to fix the Android app signing issue and ensure consistent keystore management for the Baby Steps app.

## 🔍 Problem Overview

**Issue**: Google Play Console shows signing key mismatch errors because the Android build generates a new keystore each time.

**Solution**: Use a consistent, secure keystore stored in GitHub Secrets for all builds.

## 🚀 Automated Solution

### Method 1: GitHub Actions Workflow (Recommended)

1. **Run the Keystore Setup Workflow**:
   ```
   GitHub Repository → Actions → "Setup Android Keystore" → Run workflow
   ```

2. **Download the Setup Instructions**:
   - After the workflow completes, download the `keystore-setup-instructions` artifact
   - This contains all the secrets you need to add

3. **Add Secrets to GitHub**:
   - Go to `Repository Settings → Secrets and Variables → Actions`
   - Add the four required secrets from the downloaded instructions

4. **Run Android Build**:
   - The Android build workflow will now use the consistent keystore
   - Upload the generated .aab file to Google Play Console

### Method 2: Local Script

If you prefer to generate the keystore locally:

```bash
# Run the setup script
./scripts/setup-android-keystore.sh

# Follow the on-screen instructions to add secrets to GitHub
```

## 🔑 Required GitHub Secrets

The following secrets must be added to your GitHub repository:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `ANDROID_KEYSTORE_BASE64` | Base64 encoded keystore file | `MIIKygIBAzCCCnQGCS...` |
| `KEYSTORE_PASSWORD` | Keystore password | `babysteps2024` |
| `KEY_ALIAS` | Key alias name | `babysteps` |
| `KEY_PASSWORD` | Key password | `babysteps2024` |

## 🛡️ Security Best Practices

### ✅ Do's
- Store the keystore file securely (offline backup)
- Use GitHub Secrets for sensitive data
- Keep the same keystore for all app updates
- Document the SHA1 fingerprint
- Use strong passwords in production

### ❌ Don'ts
- Never commit keystore files to git
- Don't share keystore credentials publicly
- Don't generate new keystores for updates
- Don't store secrets in code

## 🔄 Workflow Details

### Setup Android Keystore Workflow

**File**: `.github/workflows/setup-android-keystore.yml`

**Features**:
- ✅ Automatic keystore generation
- ✅ Secret validation
- ✅ Setup instructions generation
- ✅ Keystore backup artifacts
- ✅ SHA1 fingerprint extraction

**Triggers**:
- Manual workflow dispatch
- Changes to Android build files

### Enhanced Android Build Workflow

**File**: `.github/workflows/android-build.yml`

**Enhancements**:
- ✅ Secret validation before build
- ✅ Clear error messages for missing secrets
- ✅ Keystore integrity verification
- ✅ SHA1 fingerprint logging
- ✅ Automatic failure handling

## 📋 Troubleshooting

### Common Issues

#### 1. "Missing keystore secrets" Error
**Solution**: Run the keystore setup workflow and add the generated secrets to GitHub.

#### 2. "Keystore integrity verification failed"
**Solution**: Re-generate the keystore and update the `ANDROID_KEYSTORE_BASE64` secret.

#### 3. "SHA1 fingerprint mismatch in Play Console"
**Solution**: Use the SHA1 fingerprint from the build logs to update your Play Console app signing configuration.

### Debug Steps

1. **Check Workflow Logs**:
   ```
   GitHub → Actions → [Failed Workflow] → Check step details
   ```

2. **Verify Secrets**:
   ```
   Repository Settings → Secrets → Ensure all 4 secrets are set
   ```

3. **Validate Keystore Locally**:
   ```bash
   # Test keystore integrity
   echo "BASE64_STRING" | base64 -d > test.keystore
   keytool -list -keystore test.keystore -storepass PASSWORD
   ```

## 📱 Google Play Console Setup

After fixing the keystore:

1. **Upload New .aab File**:
   - Download from GitHub Actions artifacts
   - Upload to Play Console

2. **Verify Signing Certificate**:
   - Check that SHA1 fingerprint matches workflow output
   - Confirm app bundle is signed correctly

3. **Release Process**:
   - Create new release with fixed .aab
   - Previous uploads with different keys can be deleted

## 📞 Support

If you encounter issues:

1. **Check the workflow summary** for specific error messages
2. **Review the setup instructions artifact** for complete details
3. **Verify all secrets are correctly added** to GitHub
4. **Ensure the keystore workflow ran successfully** before building

## 📁 File Structure

```
├── .github/workflows/
│   ├── setup-android-keystore.yml    # Keystore setup workflow
│   └── android-build.yml              # Enhanced Android build
├── scripts/
│   └── setup-android-keystore.sh      # Local setup script
├── ANDROID_KEYSTORE_SETUP.md          # This documentation
└── create-android-keystore.sh         # Original keystore script
```

---

**🔐 Remember**: Keep your keystore secure and use the same one for all future releases!