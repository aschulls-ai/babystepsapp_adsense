# Android App Signing Setup Guide

## Problem
GitHub Actions was generating a new signing key with each build, causing Google Play Console to reject uploads due to changing SHA1 fingerprints.

## Solution
Create a permanent keystore file and store it securely in GitHub Secrets for consistent signing across all builds.

---

## Step 1: Create a Permanent Keystore (ONE TIME ONLY)

Run this command on your local machine:

```bash
keytool -genkeypair -v \
  -keystore babysteps-upload.keystore \
  -alias babysteps-upload \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass YourSecurePassword123 \
  -keypass YourSecurePassword123 \
  -dname "CN=Baby Steps,OU=Baby Steps App,O=Baby Steps,L=City,ST=State,C=US"
```

**IMPORTANT:** 
- Replace `YourSecurePassword123` with a strong password
- Save this password - you'll need it for GitHub Secrets
- Keep this keystore file safe - you cannot regenerate it with the same signature

---

## Step 2: Get the SHA1 Fingerprint

```bash
keytool -list -v -keystore babysteps-upload.keystore -alias babysteps-upload
```

Enter your password when prompted. You'll see output like:

```
Certificate fingerprints:
SHA1: A0:B7:D4:97:A7:BE:5F:C4:D1:AA:48:87:75:E9:95:0A:AE:76:0D:5E
SHA256: ...
```

**SAVE THIS SHA1 FINGERPRINT** - You'll need it for Google Play Console.

---

## Step 3: Convert Keystore to Base64

```bash
# On macOS/Linux:
base64 babysteps-upload.keystore > keystore.base64.txt

# On Windows PowerShell:
[Convert]::ToBase64String([IO.File]::ReadAllBytes("babysteps-upload.keystore")) > keystore.base64.txt
```

---

## Step 4: Add Secrets to GitHub

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these 4 secrets:

### 1. ANDROID_KEYSTORE_BASE64
- **Value:** Contents of `keystore.base64.txt` file (the entire base64 string)

### 2. KEYSTORE_PASSWORD
- **Value:** `YourSecurePassword123` (the password you used when creating the keystore)

### 3. KEY_ALIAS
- **Value:** `babysteps-upload` (the alias you used when creating the keystore)

### 4. KEY_PASSWORD  
- **Value:** `YourSecurePassword123` (same as keystore password, or different if you specified one)

---

## Step 5: Configure Google Play Console

### Option 1: Let Google Manage App Signing (RECOMMENDED)

1. Go to Google Play Console → Your App → Setup → App signing
2. Select **"Use Google Play App Signing"**
3. Upload your `babysteps-upload.keystore` file
4. Google will:
   - Extract your upload key certificate
   - Generate a separate app signing key for distribution
   - Display both SHA1 fingerprints

### Option 2: Manual Signing (Not Recommended)

If you want to manage your own app signing key:
1. Use the same keystore for signing
2. Upload the SHA1 fingerprint to Google Play Console
3. Make sure the keystore is never lost or compromised

---

## Step 6: Verify the Build

After setting up the secrets:

1. Push a commit to trigger the build workflow
2. Check the GitHub Actions logs for: `✅ Using keystore from GitHub Secrets`
3. Verify the AAB is signed with the correct SHA1:
   ```bash
   unzip -p app-release.aab META-INF/CERT.RSA | keytool -printcert
   ```

---

## Important Notes

### 🔒 Security
- **NEVER commit the keystore file to Git**
- Keep the keystore file and passwords in a secure location (password manager)
- Only the base64 version should be in GitHub Secrets

### 🔄 Keystore Backup
- Store the keystore file in at least 2 secure locations
- If you lose the keystore, you CANNOT update your app on Google Play
- You would have to publish a new app with a new package name

### 📱 SHA1 for Firebase/Google Services
If you're using Firebase, Google Sign-In, or Google Maps:
1. Add the Upload Key SHA1 to Firebase Console
2. Add the App Signing Key SHA1 (provided by Google Play) to Firebase Console
3. Download the updated `google-services.json`

---

## Troubleshooting

### Build still shows different SHA1?
- Verify the `ANDROID_KEYSTORE_BASE64` secret is correctly set
- Check GitHub Actions logs for: `✅ Using keystore from GitHub Secrets`
- The keystore base64 string should be very long (several KB)

### Google Play rejects the upload?
- Make sure you uploaded the keystore to Google Play Console first
- The SHA1 must match exactly
- Try "Option 1" (Let Google Manage) - it's more flexible

### Forgot the keystore password?
- If the keystore is already in GitHub Secrets and working, you're fine
- If not, you may need to create a new keystore (and new app on Google Play)

---

## Quick Reference

**Keystore Location:** `babysteps-upload.keystore`  
**Alias:** `babysteps-upload`  
**Algorithm:** RSA 2048-bit  
**Validity:** 10,000 days (~27 years)

**GitHub Secrets Required:**
1. `ANDROID_KEYSTORE_BASE64` - Base64 encoded keystore file
2. `KEYSTORE_PASSWORD` - Password for the keystore
3. `KEY_ALIAS` - Alias name (babysteps-upload)
4. `KEY_PASSWORD` - Password for the key

**GitHub Actions Workflow:** `.github/workflows/android-build.yml`

---

## Success Checklist

- [ ] Created permanent keystore file
- [ ] Saved keystore file in secure location
- [ ] Saved SHA1 fingerprint
- [ ] Converted keystore to base64
- [ ] Added all 4 GitHub Secrets
- [ ] Configured Google Play Console app signing
- [ ] Tested build with GitHub Actions
- [ ] Verified SHA1 matches in build output
- [ ] Successfully uploaded AAB to Google Play
