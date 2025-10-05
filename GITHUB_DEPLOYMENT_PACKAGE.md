# Complete Baby Steps App - GitHub Deployment Package

## 📦 **Files to Include in Your GitHub Repository**

### **Root Directory Structure**
```
baby-steps-app/
├── frontend/                 # Main React app
├── backend/                  # FastAPI backend (optional - can deploy separately)
├── vercel.json              # Vercel configuration
├── README.md                # Project description
├── VERCEL_DEPLOYMENT_GUIDE.md
├── ADSENSE_SETUP_GUIDE.md
└── GOOGLE_PLAY_SETUP.md
```

## 🎯 **Priority: Frontend Files (Required for Vercel)**

### **Essential Frontend Files:**
```
frontend/
├── public/
│   ├── index.html           # ✅ Updated with AdSense script
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── ads/             # ✅ NEW: AdSense components
│   │   │   ├── AdBanner.js
│   │   │   ├── BottomBannerAd.js
│   │   │   ├── InContentAd.js
│   │   │   └── SidebarAd.js
│   │   ├── ui/              # Shadcn UI components
│   │   ├── widgets/         # Dashboard widgets
│   │   ├── AuthPage.js
│   │   ├── Dashboard.js
│   │   ├── CustomizableDashboard.js  # ✅ Updated with ads
│   │   ├── BabyProfile.js
│   │   ├── TrackingPage.js
│   │   ├── FoodResearch.js
│   │   ├── EmergencyTraining.js
│   │   ├── MealPlanner.js
│   │   ├── Research.js
│   │   ├── PrivacyPolicy.js  # ✅ Updated with AdSense info
│   │   ├── EmailVerification.js
│   │   ├── PasswordReset.js
│   │   ├── Navbar.js
│   │   └── Layout.js
│   ├── services/
│   │   └── MobileService.js
│   ├── hooks/
│   │   ├── use-toast.js
│   │   └── useOfflineData.js
│   ├── App.js              # ✅ Updated with BottomBannerAd
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json            # ✅ Updated with correct name
├── yarn.lock
├── .env                    # ✅ With AdSense client ID
├── .vercelignore
├── vercel.json             # ✅ Vercel configuration
├── tailwind.config.js
├── postcss.config.js
└── craco.config.js
```

## 📝 **Step-by-Step GitHub Upload**

### **Method 1: Using Emergent's "Save to GitHub"**
1. Click "Save to GitHub" in Emergent interface
2. Create repository: `baby-steps-app`
3. Include all files from `/app/frontend/` directory
4. Done! Skip to Vercel deployment.

### **Method 2: Manual GitHub Upload**

1. **Create GitHub Repository**
   - Go to github.com → New Repository
   - Name: `baby-steps-app`
   - Public repository (required for free Vercel)

2. **Download/Copy These Key Files:**