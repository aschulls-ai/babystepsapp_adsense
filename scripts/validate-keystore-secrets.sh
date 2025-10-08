#!/bin/bash

# Script to validate Android keystore secrets configuration
# This can be used locally to test if a keystore setup is correct

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo -e "${BLUE}"
echo "🔍 Android Keystore Validation"
echo "=============================="
echo -e "${NC}"

# Check if required parameters are provided
if [ $# -lt 4 ]; then
    print_error "Usage: $0 <base64_keystore> <store_password> <key_alias> <key_password>"
    echo
    echo "Example:"
    echo "$0 'MIIKygIBAzCCC...' 'babysteps2024' 'babysteps' 'babysteps2024'"
    echo
    echo "This script validates that keystore secrets will work correctly."
    exit 1
fi

KEYSTORE_BASE64="$1"
STORE_PASSWORD="$2"
KEY_ALIAS="$3"
KEY_PASSWORD="$4"

# Create temporary directory for validation
TEMP_DIR=$(mktemp -d)
TEMP_KEYSTORE="$TEMP_DIR/validate.keystore"

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Validate base64 and decode keystore
print_status "Validating base64 keystore data..."
if echo "$KEYSTORE_BASE64" | base64 -d > "$TEMP_KEYSTORE" 2>/dev/null; then
    print_success "Base64 keystore decoded successfully"
else
    print_error "Failed to decode base64 keystore data"
    exit 1
fi

# Validate keystore integrity
print_status "Validating keystore integrity..."
if keytool -list -keystore "$TEMP_KEYSTORE" -storepass "$STORE_PASSWORD" > /dev/null 2>&1; then
    print_success "Keystore integrity verified"
else
    print_error "Keystore integrity check failed - invalid store password or corrupted keystore"
    exit 1
fi

# Validate key alias exists
print_status "Validating key alias '$KEY_ALIAS'..."
if keytool -list -keystore "$TEMP_KEYSTORE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" > /dev/null 2>&1; then
    print_success "Key alias '$KEY_ALIAS' found"
else
    print_error "Key alias '$KEY_ALIAS' not found in keystore"
    echo "Available aliases:"
    keytool -list -keystore "$TEMP_KEYSTORE" -storepass "$STORE_PASSWORD" | grep "Alias name:" || echo "  No aliases found"
    exit 1
fi

# Validate key password
print_status "Validating key password..."
# Try to export the key (this will fail if password is wrong, but we just check the exit code)
if keytool -exportcert -alias "$KEY_ALIAS" -keystore "$TEMP_KEYSTORE" -storepass "$STORE_PASSWORD" -keypass "$KEY_PASSWORD" -file /dev/null > /dev/null 2>&1; then
    print_success "Key password verified"
else
    print_error "Key password validation failed"
    exit 1
fi

# Show keystore details
print_status "Keystore Details:"
echo "================="
keytool -list -v -keystore "$TEMP_KEYSTORE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" | grep -E "(Alias name|Valid from|SHA1|SHA256)"

# Extract SHA1 fingerprint
SHA1_FINGERPRINT=$(keytool -list -v -keystore "$TEMP_KEYSTORE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" | grep SHA1 | sed 's/.*SHA1: //')

echo
print_success "✅ All validations passed!"
echo
echo "📋 Summary:"
echo "- Keystore: Valid and accessible"
echo "- Store Password: Correct"
echo "- Key Alias: '$KEY_ALIAS' exists"
echo "- Key Password: Correct"
echo "- SHA1 Fingerprint: $SHA1_FINGERPRINT"
echo
print_success "🚀 These secrets should work correctly in GitHub Actions!"

# Generate GitHub secrets format
echo
print_status "GitHub Secrets Format:"
echo "======================"
echo "ANDROID_KEYSTORE_BASE64:"
echo "$KEYSTORE_BASE64"
echo
echo "KEYSTORE_PASSWORD:"
echo "$STORE_PASSWORD"
echo
echo "KEY_ALIAS:"
echo "$KEY_ALIAS"
echo
echo "KEY_PASSWORD:"
echo "$KEY_PASSWORD"