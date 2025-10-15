#!/bin/bash

# Baby Steps - Restore Main App After AdSense Approval
# This script restores the original app with authentication

echo "🍼 Baby Steps - Restore Main App"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must run from /app/frontend directory"
    exit 1
fi

# Check if backups exist
if [ ! -f "src/index.original.js" ] || [ ! -f "src/App.original.js" ]; then
    echo "❌ Error: Original files not found!"
    echo "Cannot restore without backups."
    exit 1
fi

# Restore original files
echo "🔄 Restoring original files..."
mv src/index.original.js src/index.js
mv src/App.original.js src/App.js
echo "✅ Original files restored"

# Build
echo ""
echo "🏗️  Building production version..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📤 Ready to deploy main app!"
    echo ""
    echo "Next steps:"
    echo "1. Deploy to Vercel:"
    echo "   cd build && vercel --prod"
    echo ""
    echo "2. Verify at: https://babystepsapp.app"
    echo "   - Should show login page"
    echo "   - Normal authentication flow"
    echo ""
    echo "✅ Main app restored!"
else
    echo "❌ Build failed!"
    exit 1
fi
