#!/bin/bash

# Baby Steps Android Keystore Setup Script
# This script helps setup Android keystore for consistent app signing

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
KEYSTORE_FILE="baby-steps-release.keystore"
KEY_ALIAS="babysteps"
STORE_PASSWORD="babysteps2024"
KEY_PASSWORD="babysteps2024"
VALIDITY_DAYS=10000

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "🔐 Baby Steps Android Keystore Setup"
    echo "===================================="
    echo -e "${NC}"
}

# Check if Java is installed
check_java() {
    if ! command -v keytool &> /dev/null; then
        print_error "Java/keytool not found. Please install Java Development Kit (JDK)"
        echo "Ubuntu/Debian: sudo apt-get install default-jdk"
        echo "macOS: brew install openjdk"
        exit 1
    fi
    
    print_success "Java/keytool found: $(keytool -help 2>&1 | head -1)"
}

# Generate keystore
generate_keystore() {
    print_status "Generating Android keystore..."
    
    if [ -f "$KEYSTORE_FILE" ]; then
        read -p "Keystore file already exists. Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_warning "Keeping existing keystore"
            
            # Verify existing keystore works
            if keytool -list -keystore "$KEYSTORE_FILE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" > /dev/null 2>&1; then
                print_success "Existing keystore verified and will be used"
                return 0
            else
                print_warning "Existing keystore appears corrupted. Will regenerate..."
            fi
        fi
        rm "$KEYSTORE_FILE"
    fi
    
    # Generate keystore with error handling
    if keytool -genkeypair -v \
      -keystore "$KEYSTORE_FILE" \
      -alias "$KEY_ALIAS" \
      -keyalg RSA \
      -keysize 2048 \
      -validity $VALIDITY_DAYS \
      -storepass "$STORE_PASSWORD" \
      -keypass "$KEY_PASSWORD" \
      -dname "CN=Baby Steps,OU=Baby Steps,O=Baby Steps App,L=Unknown,ST=Unknown,C=US"; then
      print_success "Keystore generated: $KEYSTORE_FILE"
    else
      print_error "Failed to generate keystore with standard alias"
      
      # Try with unique alias if standard fails
      TIMESTAMP=$(date +%s)
      UNIQUE_ALIAS="${KEY_ALIAS}_${TIMESTAMP}"
      print_status "Trying with unique alias: $UNIQUE_ALIAS"
      
      if keytool -genkeypair -v \
        -keystore "$KEYSTORE_FILE" \
        -alias "$UNIQUE_ALIAS" \
        -keyalg RSA \
        -keysize 2048 \
        -validity $VALIDITY_DAYS \
        -storepass "$STORE_PASSWORD" \
        -keypass "$KEY_PASSWORD" \
        -dname "CN=Baby Steps,OU=Baby Steps,O=Baby Steps App,L=Unknown,ST=Unknown,C=US"; then
        
        KEY_ALIAS="$UNIQUE_ALIAS"
        print_success "Keystore generated with unique alias: $KEYSTORE_FILE"
        print_warning "Note: Key alias changed to '$KEY_ALIAS'"
      else
        print_error "Failed to generate keystore. Please check Java installation."
        exit 1
      fi
    fi
}

# Show keystore details
show_keystore_details() {
    print_status "Keystore Details:"
    echo "================="
    
    keytool -list -v -keystore "$KEYSTORE_FILE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" | grep -E "(Alias|Valid|SHA1|SHA256)"
    
    # Get SHA1 fingerprint for easy copying
    SHA1_FINGERPRINT=$(keytool -list -v -keystore "$KEYSTORE_FILE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" | grep SHA1 | sed 's/.*SHA1: //')
    
    echo
    print_success "SHA1 Fingerprint: $SHA1_FINGERPRINT"
}

# Generate base64 encoded keystore
generate_base64() {
    print_status "Generating base64 encoded keystore for GitHub Secrets..."
    
    if command -v base64 &> /dev/null; then
        KEYSTORE_BASE64=$(base64 -w 0 "$KEYSTORE_FILE" 2>/dev/null || base64 -b 0 "$KEYSTORE_FILE")
        echo
        echo "📤 Base64 Encoded Keystore (copy this for ANDROID_KEYSTORE_BASE64 secret):"
        echo "=================================================================="
        echo "$KEYSTORE_BASE64"
        echo
    else
        print_warning "base64 command not found. You'll need to encode the keystore manually."
    fi
}

# Generate setup instructions
generate_instructions() {
    cat << EOF > keystore-setup-instructions.txt

🔐 Baby Steps Android Keystore Setup Instructions
================================================

Your Android keystore has been generated successfully!

GitHub Secrets Configuration:
-----------------------------
Add these secrets to your GitHub repository (Settings → Secrets and Variables → Actions):

1. ANDROID_KEYSTORE_BASE64
   Value: (Use the base64 string shown above)

2. KEYSTORE_PASSWORD
   Value: $STORE_PASSWORD

3. KEY_ALIAS
   Value: $KEY_ALIAS

4. KEY_PASSWORD
   Value: $KEY_PASSWORD

SHA1 Fingerprint: $(keytool -list -v -keystore "$KEYSTORE_FILE" -alias "$KEY_ALIAS" -storepass "$STORE_PASSWORD" | grep SHA1 | sed 's/.*SHA1: //')

Security Notes:
--------------
- Keep the keystore file ($KEYSTORE_FILE) secure and backed up
- Never commit the keystore to git
- Use this same keystore for all future app releases
- The SHA1 fingerprint above should be used in Google Play Console

Next Steps:
----------
1. Add all four secrets to your GitHub repository
2. Run the Android build workflow
3. Upload the generated .aab file to Google Play Console
4. Verify the SHA1 fingerprint matches in Play Console

EOF

    print_success "Instructions saved to: keystore-setup-instructions.txt"
}

# Main execution
main() {
    print_header
    
    # Check prerequisites
    check_java
    
    # Generate keystore
    generate_keystore
    
    # Show details
    show_keystore_details
    
    # Generate base64
    generate_base64
    
    # Generate instructions
    generate_instructions
    
    echo
    print_success "Android keystore setup complete!"
    print_status "Next: Add the secrets to GitHub and run the Android build workflow"
    
    # Security reminder
    echo
    print_warning "SECURITY REMINDER:"
    echo "- Keep $KEYSTORE_FILE file secure (don't commit to git)"
    echo "- Store credentials in a password manager"
    echo "- Use the same keystore for all future releases"
}

# Run main function
main "$@"