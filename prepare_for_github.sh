#!/bin/bash

# Baby Steps - GitHub Preparation Script
echo "🚀 Preparing Baby Steps App for GitHub Deployment..."

# Create deployment directory
mkdir -p /app/github_deploy/baby-steps-app

# Copy frontend (main app)
echo "📁 Copying frontend files..."
cp -r /app/frontend /app/github_deploy/baby-steps-app/

# Copy configuration files
echo "⚙️ Copying configuration files..."
cp /app/vercel.json /app/github_deploy/baby-steps-app/
cp /app/VERCEL_DEPLOYMENT_GUIDE.md /app/github_deploy/baby-steps-app/README.md
cp /app/ADSENSE_SETUP_GUIDE.md /app/github_deploy/baby-steps-app/
cp /app/GOOGLE_PLAY_SETUP.md /app/github_deploy/baby-steps-app/

# Create main README
cat > /app/github_deploy/baby-steps-app/README.md << 'EOF'
# Baby Steps - Parenting Made Easy

A comprehensive parenting app with baby tracking, nutrition guidance, and AI-powered features.

## 🚀 Features
- 👶 Baby profile and milestone tracking
- 📊 Customizable dashboard with widgets
- 🍎 AI-powered food research and meal planning
- 🆘 Emergency training and safety guidance
- 📱 Mobile app (Android APK/AAB generation)
- 💰 Google AdSense integration for monetization
- 🔐 Secure authentication with optional email verification

## 🌐 Live Demo
Visit: [Your Vercel URL will go here]

## 💰 Monetization
- Google AdSense integration
- Revenue potential: $50-2000+/month
- COPPA compliant for parenting apps

## 🛠️ Tech Stack
- **Frontend**: React, Tailwind CSS, Shadcn UI
- **Backend**: FastAPI, MongoDB
- **Mobile**: Capacitor (Android/iOS)
- **Deployment**: Vercel
- **Monetization**: Google AdSense

## 🚀 Quick Deploy to Vercel

1. Fork this repository
2. Connect to Vercel
3. Set Root Directory: `frontend`
4. Add environment variables:
   ```
   REACT_APP_BACKEND_URL=https://smart-parent.preview.emergentagent.com
   REACT_APP_ADSENSE_CLIENT_ID=ca-pub-0000000000000000
   ```
5. Deploy!

## 📚 Documentation
- [Vercel Deployment Guide](./VERCEL_DEPLOYMENT_GUIDE.md)
- [Google AdSense Setup](./ADSENSE_SETUP_GUIDE.md)
- [Android App Generation](./GOOGLE_PLAY_SETUP.md)

## 📄 License
MIT License - Feel free to use for your own parenting app!
EOF

# List deployment files
echo "📋 Files ready for GitHub:"
find /app/github_deploy/baby-steps-app -type f | head -20

echo "✅ Ready! Your files are in: /app/github_deploy/baby-steps-app"
echo ""
echo "🎯 Next Steps:"
echo "1. Copy all files from /app/github_deploy/baby-steps-app to your GitHub repo"
echo "2. Or use Emergent's 'Save to GitHub' feature"
echo "3. Deploy to Vercel with Root Directory: 'frontend'"
echo "4. Get your Vercel URL for AdSense!"