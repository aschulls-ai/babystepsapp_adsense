#!/bin/bash

# Quick script to generate upload keystore for Google Play App Signing
# This creates the upload key that signs the AAB before Google re-signs it

echo "🔐 Generating Upload Keystore for Google Play App Signing"
echo "======================================================"

# Clean up any existing keystore
rm -f upload.keystore

# Generate upload keystore
keytool -genkeypair -v \
  -keystore upload.keystore \
  -alias upload \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass upload2024 \
  -keypass upload2024 \
  -dname "CN=Baby Steps Upload,OU=Baby Steps,O=Baby Steps App,L=Unknown,ST=Unknown,C=US"

echo "✅ Upload keystore generated"

# Show keystore details
echo ""
echo "📋 Upload Keystore Details:"
echo "=========================="
keytool -list -v -keystore upload.keystore -alias upload -storepass upload2024 | grep -E "(Alias|Valid|SHA1|SHA256)"

# Get SHA1 for reference
SHA1_FINGERPRINT=$(keytool -list -v -keystore upload.keystore -alias upload -storepass upload2024 | grep SHA1 | sed 's/.*SHA1: //')

echo ""
echo "🔑 Upload Key SHA1: $SHA1_FINGERPRINT"

# Convert to base64 for GitHub Secrets
echo ""
echo "📤 GitHub Secrets for Android Build:"
echo "===================================="
echo ""
echo "ANDROID_KEYSTORE_BASE64:"
base64 -w 0 upload.keystore
echo ""
echo ""
echo "KEYSTORE_PASSWORD:"
echo "upload2024"
echo ""
echo "KEY_ALIAS:"
echo "upload"
echo ""
echo "KEY_PASSWORD:"
echo "upload2024"

echo ""
echo ""
echo "🎯 Next Steps:"
echo "============="
echo "1. Add the above 4 secrets to GitHub repository settings"
echo "2. Run the Android build workflow"
echo "3. Download the signed AAB from artifacts"
echo "4. Upload to Google Play Console"
echo ""
echo "ℹ️  Note: This is the UPLOAD key. Google Play will use a separate"
echo "   APP SIGNING key for final distribution to users."

# Clean up
rm -f upload.keystore

echo ""
echo "✅ Upload keystore secrets generated successfully!"