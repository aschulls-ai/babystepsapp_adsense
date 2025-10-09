# 🌐 Render Deployment Guide for Baby Steps Demo Server

## 🚀 Step-by-Step Deployment

### **1. Create Render Account**
- Go to **https://render.com**
- Sign up with GitHub, Google, or email
- Verify your email address

### **2. Create Web Service**
1. Click **"New"** → **"Web Service"**
2. Choose **"Build and deploy from a Git repository"**
3. Click **"Connect GitHub"** (or upload files manually)

### **3. Repository Setup Options**

#### **Option A: Connect GitHub Repository**
1. Select your Baby Steps repository
2. Set **Root Directory**: `public-server`
3. Click **"Connect"**

#### **Option B: Manual Upload (if no GitHub)**
1. Zip the `/app/public-server` folder
2. Upload the zip file to Render
3. Extract and continue

### **4. Configure Service Settings**

**Basic Settings:**
- **Name**: `baby-steps-demo-api`
- **Environment**: `Python 3`
- **Region**: `Oregon (US West)` (or closest to you)
- **Branch**: `main` (if using GitHub)

**Build & Deploy Settings:**
- **Root Directory**: `public-server` (if using GitHub)
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  uvicorn app:app --host 0.0.0.0 --port $PORT
  ```

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (if using GitHub)
- **Health Check Path**: `/api/health`

### **5. Deploy**
1. Click **"Create Web Service"**
2. Render will start building your service
3. Wait for deployment to complete (2-5 minutes)

### **6. Get Your Public URL**
After deployment, you'll get a URL like:
```
https://baby-steps-demo-api.onrender.com
```

## 🧪 Test Your Deployment

### **Quick Health Check**
```bash
curl https://YOUR-APP.onrender.com/api/health
```

**Expected Response:**
```json
{"status":"healthy","timestamp":"2025-10-08T23:30:00.123456"}
```

### **Test Authentication**
```bash
curl -X POST https://YOUR-APP.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}'
```

**Expected Response:**
```json
{"access_token":"eyJ...", "token_type":"bearer"}
```

### **Test Demo Data**
```bash
# Get token first
TOKEN=$(curl -s -X POST https://YOUR-APP.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}' | \
  grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# Get babies
curl https://YOUR-APP.onrender.com/api/babies \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
[{"id":"demo-baby-456","name":"Emma","birth_date":"2024-01-15","gender":"girl","profile_image":null,"user_id":"demo-user-123"}]
```

## 🔧 Update Android App Configuration

Once your server is deployed and tested:

```bash
# Replace with your actual Render URL
./update-android-config.sh https://baby-steps-demo-api.onrender.com
```

## 📱 Android App Testing

### **1. Rebuild App**
```bash
cd frontend
yarn build
npx cap sync android
```

### **2. Build New AAB**
- Run GitHub Actions "Build Baby Steps Android" workflow
- Download the new AAB file

### **3. Test App**
- Install AAB on test device
- Use demo credentials:
  - **Email**: `demo@babysteps.com`
  - **Password**: `demo123`

## 🎯 Expected Results

After deployment and configuration:
- ✅ Android app connects to public server
- ✅ Login works with demo credentials  
- ✅ Demo baby "Emma" appears in app
- ✅ Activities can be tracked and viewed
- ✅ Food research returns safety information
- ✅ Meal planner provides suggestions

## 🔄 Troubleshooting

### **Deployment Issues**
- Check build logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure start command uses `$PORT` variable

### **Connection Issues**  
- Verify server URL is accessible
- Check Android app configuration
- Test API endpoints manually with curl

### **Authentication Issues**
- Confirm demo credentials work via curl
- Check JWT token format and expiration
- Verify CORS headers are enabled

## 💰 Render Free Tier

- ✅ **750 hours/month free** (enough for testing)
- ✅ **Automatic HTTPS** included
- ✅ **Health checks** and monitoring  
- ✅ **Automatic deployments** from GitHub
- ⚠️ **Sleeps after 15min inactivity** (wakes up quickly)

---

**🎉 Your Baby Steps demo server will be live and ready for Android app testing!**