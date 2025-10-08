#!/bin/bash

# Solution for creating new app with fresh keystore
# Use this if you can create a new app listing in Google Play Console

echo "🆕 Creating Fresh App Solution"
echo "============================="

# Use the existing keystore we generated
KEYSTORE_FILE="/app/baby-steps-release.keystore"
STORE_PASSWORD="babysteps2024"
KEY_ALIAS="babysteps"

if [ -f "$KEYSTORE_FILE" ]; then
    echo "✅ Using existing keystore: $KEYSTORE_FILE"
    
    # Get the SHA1 fingerprint
    SHA1_FINGERPRINT=$(keytool -list -v -keystore "$KEYSTORE_FILE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" | grep SHA1 | sed 's/.*SHA1: //')
    
    echo "🔑 SHA1 Fingerprint for new app: $SHA1_FINGERPRINT"
    echo
    echo "📋 Steps for Google Play Console:"
    echo "1. Delete the existing app bundle upload (if it's just a test)"
    echo "2. Upload new .aab file with this keystore"
    echo "3. Use this SHA1 fingerprint: $SHA1_FINGERPRINT"
    echo
    
    # Convert to base64 for GitHub secrets
    echo "📤 GitHub Secrets (use these):"
    echo "=============================="
    echo "ANDROID_KEYSTORE_BASE64:"
    base64 -w 0 "$KEYSTORE_FILE"
    echo
    echo
    echo "KEYSTORE_PASSWORD: $STORE_PASSWORD"
    echo "KEY_ALIAS: $KEY_ALIAS" 
    echo "KEY_PASSWORD: $STORE_PASSWORD"
    
else
    echo "❌ Keystore file not found. Run keystore setup first."
    exit 1
fi