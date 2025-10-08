# 🔧 Android Keystore Troubleshooting

## Common Errors & Solutions

### 1. "Key pair not generated, alias already exists"

**Error**: `java.lang.Exception: Key pair not generated, alias <babysteps> already exists`

**Cause**: Trying to create a key with an alias that already exists in the keystore.

**Solutions**:

#### Option A: Use the Clean Fix Workflow (Recommended)
1. Go to **Actions → "Clean & Fix Keystore"**
2. Type **"YES"** to confirm cleaning
3. Run the workflow
4. Download the new setup instructions
5. Update GitHub secrets with new values

#### Option B: Force Regenerate
1. Go to **Actions → "Setup Android Keystore"**
2. Check **"Force regenerate keystore"** option
3. Run the workflow
4. Update secrets with new values

#### Option C: Local Fix
```bash
# Delete existing keystore and regenerate
rm -f baby-steps-*.keystore
./scripts/setup-android-keystore.sh
```

### 2. "Keystore integrity verification failed"

**Cause**: Corrupted keystore or wrong password.

**Solutions**:
1. Run the **Clean & Fix Keystore** workflow
2. Regenerate keystore with new passwords
3. Update all GitHub secrets

### 3. "Missing keystore secrets"

**Cause**: Required GitHub secrets not configured.

**Solutions**:
1. Run **Setup Android Keystore** workflow
2. Add all 4 secrets to repository settings:
   - `ANDROID_KEYSTORE_BASE64`
   - `KEYSTORE_PASSWORD`  
   - `KEY_ALIAS`
   - `KEY_PASSWORD`

### 4. "SHA1 fingerprint mismatch in Play Console"

**Cause**: Using different keystore than expected.

**Solutions**:
1. Get SHA1 from build logs
2. Update Google Play Console with new fingerprint
3. Or regenerate keystore to match existing fingerprint

## 🚀 Quick Fix Commands

### Clean Start (Recommended for persistent issues)
```bash
# 1. Run clean workflow
GitHub Actions → Clean & Fix Keystore → Type "YES" → Run

# 2. Update secrets with downloaded values
Repository Settings → Secrets → Update all 4 secrets

# 3. Run Android build
Actions → Build Baby Steps Android → Run workflow
```

### Local Troubleshooting
```bash
# Check Java installation
java -version
keytool -help

# Clean and regenerate locally
rm -f *.keystore
./scripts/setup-android-keystore.sh

# Validate secrets work
./scripts/validate-keystore-secrets.sh "BASE64" "PASSWORD" "ALIAS" "KEYPASSWORD"
```

## 🔍 Debugging Steps

### 1. Check Workflow Logs
- Look for specific error messages
- Note the exact line where failure occurs
- Check if Java/keytool is available

### 2. Verify Environment
```bash
# In GitHub Actions runner:
java -version                    # Should be Java 17+
keytool -help                   # Should be available
ls -la *.keystore              # Check existing files
```

### 3. Test Locally
```bash
# Generate test keystore
keytool -genkeypair -keystore test.keystore -alias test -validity 1000 \
  -keyalg RSA -keysize 2048 -storepass test123 -keypass test123 \
  -dname "CN=Test,O=Test"

# Verify it works
keytool -list -keystore test.keystore -storepass test123

# Clean up
rm test.keystore
```

## 📋 Prevention Tips

### 1. Consistent Naming
- Use unique aliases with timestamps if needed
- Clean old keystores before generating new ones
- Document keystore parameters

### 2. Backup Strategy
- Download keystore artifacts from GitHub Actions
- Store keystore files securely offline
- Document passwords in password manager

### 3. Testing
- Always validate keystore before using in production
- Test signing process locally first
- Verify SHA1 fingerprints match expectations

## 🆘 Emergency Recovery

If you've lost the keystore or it's completely broken:

### 1. For New Apps
- Run **Clean & Fix Keystore** workflow
- Use new keystore for fresh app upload
- Document new SHA1 fingerprint

### 2. For Existing Apps (Play Console)
- Contact Google Play support if keystore is lost
- Consider creating new app listing if recovery isn't possible
- Always backup keystores going forward

### 3. Prevention for Future
- Enable keystore backup artifacts in workflows
- Store keystore in secure cloud storage
- Document recovery procedures in team docs

---

**💡 Pro Tip**: When in doubt, use the "Clean & Fix Keystore" workflow - it handles most edge cases automatically!