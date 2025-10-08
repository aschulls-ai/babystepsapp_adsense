#!/bin/bash

# Script to try recreating the original keystore parameters
# This attempts common configurations that might produce the target SHA1

TARGET_SHA1="B4:18:8D:64:6B:1C:42:06:AD:63:CC:5A:C9:EF:62:B2:79:64:50:2D"

echo "🔍 Attempting to recreate keystore with target SHA1: $TARGET_SHA1"
echo "================================================================"

# Common configurations to try
declare -a PASSWORDS=("android" "password" "123456" "babysteps" "babysteps2024" "release" "")
declare -a ALIASES=("androiddebugkey" "release" "key0" "babysteps" "my-release-key" "upload")
declare -a DNAMES=(
    "CN=Android Debug,O=Android,C=US"
    "CN=Unknown,OU=Unknown,O=Unknown,L=Unknown,ST=Unknown,C=Unknown" 
    "CN=Baby Steps,OU=Baby Steps,O=Baby Steps App,L=Unknown,ST=Unknown,C=US"
    "CN=Android,OU=Android,O=Android,L=Mountain View,ST=California,C=US"
)

attempt=1

for password in "${PASSWORDS[@]}"; do
    for alias in "${ALIASES[@]}"; do
        for dname in "${DNAMES[@]}"; do
            
            KEYSTORE_FILE="test_attempt_${attempt}.keystore"
            
            echo "🔧 Attempt $attempt: password='$password', alias='$alias'"
            
            # Generate keystore
            keytool -genkeypair -v \
                -keystore "$KEYSTORE_FILE" \
                -alias "$alias" \
                -keyalg RSA \
                -keysize 2048 \
                -validity 10000 \
                -storepass "$password" \
                -keypass "$password" \
                -dname "$dname" > /dev/null 2>&1
            
            if [ -f "$KEYSTORE_FILE" ]; then
                # Get SHA1
                CURRENT_SHA1=$(keytool -list -v -keystore "$KEYSTORE_FILE" -alias "$alias" -storepass "$password" 2>/dev/null | grep SHA1 | sed 's/.*SHA1: //')
                
                echo "   Generated SHA1: $CURRENT_SHA1"
                
                if [ "$CURRENT_SHA1" = "$TARGET_SHA1" ]; then
                    echo "🎉 MATCH FOUND!"
                    echo "==============="
                    echo "✅ Keystore: $KEYSTORE_FILE"
                    echo "✅ Password: $password"
                    echo "✅ Alias: $alias"
                    echo "✅ DN: $dname"
                    echo "✅ SHA1: $CURRENT_SHA1"
                    
                    # Convert to base64
                    echo
                    echo "📤 Base64 for GitHub Secret:"
                    base64 -w 0 "$KEYSTORE_FILE"
                    echo
                    exit 0
                fi
                
                # Clean up
                rm "$KEYSTORE_FILE"
            fi
            
            ((attempt++))
            
            # Limit attempts to prevent endless loop
            if [ $attempt -gt 50 ]; then
                echo "⚠️  Reached maximum attempts (50)"
                break 3
            fi
        done
    done
done

echo "❌ Could not recreate keystore with target SHA1"
echo "💡 Recommendation: Create new app listing or contact Google Play support"