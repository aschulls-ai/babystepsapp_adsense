#!/bin/bash

# Script to create a consistent Android keystore for Baby Steps app
# This keystore should be used for all production builds

echo "🔐 Creating Android Keystore for Baby Steps App"
echo "================================================"

# Keystore configuration
KEYSTORE_FILE="baby-steps-release.keystore"
KEY_ALIAS="babysteps"
STORE_PASSWORD="babysteps2024"
KEY_PASSWORD="babysteps2024"
VALIDITY_DAYS=10000

# Generate the keystore
keytool -genkeypair -v \
  -keystore "$KEYSTORE_FILE" \
  -alias "$KEY_ALIAS" \
  -keyalg RSA \
  -keysize 2048 \
  -validity $VALIDITY_DAYS \
  -storepass "$STORE_PASSWORD" \
  -keypass "$KEY_PASSWORD" \
  -dname "CN=Baby Steps,OU=Baby Steps,O=Baby Steps App,L=Unknown,ST=Unknown,C=US"

echo ""
echo "✅ Keystore created: $KEYSTORE_FILE"
echo ""

# Show keystore details
echo "📋 Keystore Details:"
echo "==================="
keytool -list -v -keystore "$KEYSTORE_FILE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" | grep -E "(Alias|Valid|SHA1|SHA256)"

echo ""
echo "🔒 Security Information:"
echo "======================="
echo "Store Password: $STORE_PASSWORD"
echo "Key Alias: $KEY_ALIAS" 
echo "Key Password: $KEY_PASSWORD"
echo ""

# Convert to base64 for GitHub Secrets
echo "📤 Base64 Encoded Keystore (for GitHub Secrets):"
echo "==============================================="
base64 -i "$KEYSTORE_FILE"
echo ""

echo "🚀 Next Steps:"
echo "=============="
echo "1. Copy the base64 string above"
echo "2. Go to GitHub → Settings → Secrets and Variables → Actions"
echo "3. Add these secrets:"
echo "   - ANDROID_KEYSTORE_BASE64: [paste the base64 string]"
echo "   - KEYSTORE_PASSWORD: $STORE_PASSWORD"
echo "   - KEY_ALIAS: $KEY_ALIAS"
echo "   - KEY_PASSWORD: $KEY_PASSWORD"
echo ""
echo "4. Keep the $KEYSTORE_FILE file secure - you'll need it for future manual builds"
echo ""
echo "⚠️  IMPORTANT: Never commit the keystore file to git!"