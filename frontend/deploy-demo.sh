#!/bin/bash

# Baby Steps - Deploy Demo Version for AdSense Review
# This script creates a demo build with auto-login for AdSense reviewers

echo "🍼 Baby Steps - Demo Deployment Script"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must run from /app/frontend directory"
    exit 1
fi

# Backup original files
echo "📦 Backing up original files..."
if [ ! -f "src/index.original.js" ]; then
    cp src/index.js src/index.original.js
    echo "✅ Backed up index.js"
fi

if [ ! -f "src/App.original.js" ]; then
    cp src/App.js src/App.original.js
    echo "✅ Backed up App.js"
fi

# Copy demo files
echo ""
echo "🔄 Copying demo files..."
cp src/index.demo.js src/index.js
cp src/App.demo.js src/App.js
echo "✅ Demo files activated"

# Build
echo ""
echo "🏗️  Building production version..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📤 Ready to deploy!"
    echo ""
    echo "Next steps:"
    echo "1. Deploy build folder to Vercel:"
    echo "   cd build && vercel --prod"
    echo ""
    echo "2. Or push to GitHub and Vercel will auto-deploy"
    echo ""
    echo "3. Verify at: https://babystepsapp.app"
    echo "   - Should auto-login"
    echo "   - Check ads.txt at: https://babystepsapp.app/ads.txt"
    echo ""
    echo "4. After AdSense approval, run: ./restore-main.sh"
else
    echo "❌ Build failed!"
    exit 1
fi
