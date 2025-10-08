# 🌐 Baby Steps Demo Server Setup

## 📋 Overview

I've created a simplified public demo server for the Baby Steps Android app to connect to, eliminating server connectivity issues.

## 🚀 Demo Server Features

### **Authentication**
- ✅ Login/Register endpoints
- ✅ JWT token-based authentication  
- ✅ Demo user: `demo@babysteps.com` / `demo123`

### **Core API Endpoints**
- ✅ `/api/auth/login` - User authentication
- ✅ `/api/auth/register` - New user registration
- ✅ `/api/babies` - Baby profile management
- ✅ `/api/activities` - Activity tracking
- ✅ `/api/food/research` - Food safety queries
- ✅ `/api/meals/search` - Meal planning
- ✅ `/api/research` - General parenting info

### **Demo Data Included**
- **Demo User**: "Demo Parent" 
- **Demo Baby**: "Emma" (born Jan 15, 2024)
- **Demo Activities**: Feeding, sleep, diaper changes

## 🔧 Deployment Options

### **Option 1: Vercel (Recommended)**

1. **Deploy to Vercel**:
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy from public-server directory
   cd /app/public-server
   vercel --prod
   ```

2. **Get Public URL**: Vercel will provide a URL like `https://baby-steps-demo.vercel.app`

### **Option 2: Railway**

1. **Create Railway Account**: https://railway.app
2. **Deploy from GitHub**: Connect repository and deploy `/public-server` folder
3. **Get Public URL**: Railway provides automatic HTTPS URL

### **Option 3: Render**

1. **Create Render Account**: https://render.com
2. **Create Web Service** from GitHub repository
3. **Set Build Command**: `pip install -r requirements.txt`
4. **Set Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## 📱 Update Android App Configuration

Once you have the public server URL, update the Android app:

### **1. Update Capacitor Config**
```json
// /app/frontend/capacitor.config.json
{
  "server": {
    "url": "https://YOUR-DEMO-SERVER.vercel.app",
    "cleartext": false
  }
}
```

### **2. Update Environment Variables**
```bash
# /app/frontend/.env.production
REACT_APP_BACKEND_URL=https://YOUR-DEMO-SERVER.vercel.app
```

### **3. Rebuild Android App**
```bash
cd frontend
yarn build
npx cap sync android
# Then build AAB in GitHub Actions
```

## 🧪 Testing the Demo Server

### **Quick Test Commands**:

```bash
# Health check
curl https://YOUR-SERVER-URL/api/health

# Login test
curl -X POST https://YOUR-SERVER-URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}'

# Get babies (with auth token)
curl https://YOUR-SERVER-URL/api/babies \
  -H "Authorization: Bearer YOUR-TOKEN"
```

## 📲 Demo Credentials

- **Email**: `demo@babysteps.com`
- **Password**: `demo123`
- **Demo Baby**: Emma (9 months old)
- **Pre-loaded Activities**: Feeding, sleep, diaper changes

## 🔄 Quick Deployment Script

I'll create a script to deploy automatically:

```bash
#!/bin/bash
# Deploy Baby Steps Demo Server

cd /app/public-server

echo "🚀 Deploying Baby Steps Demo Server..."

# Option 1: Deploy to Vercel
if command -v vercel &> /dev/null; then
    echo "Deploying to Vercel..."
    vercel --prod --yes
else
    echo "Install Vercel CLI: npm install -g vercel"
fi

echo "✅ Demo server deployment initiated!"
echo "🔗 Use the provided URL to update Android app configuration"
```

## 🎯 Benefits

- ✅ **No Database Required**: Uses in-memory storage
- ✅ **No Environment Setup**: Self-contained server
- ✅ **CORS Enabled**: Works with mobile apps
- ✅ **Demo Data**: Pre-loaded for immediate testing
- ✅ **All Endpoints**: Covers main app functionality
- ✅ **Free Hosting**: Compatible with free tier services

## 📝 Next Steps

1. **Choose hosting option** (Vercel recommended)
2. **Deploy the demo server**
3. **Update Android app config** with new server URL
4. **Rebuild and test** Android app
5. **Verify connectivity** in Android app

---

**🌟 Result**: Android app will have a working backend server for testing and demo purposes!