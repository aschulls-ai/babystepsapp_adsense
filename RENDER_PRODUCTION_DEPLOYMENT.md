# Render Production Deployment Guide

## 🚀 Backend Deployment Steps

### 1. Deploy to Render

1. **Go to [Render.com](https://render.com)**
2. **Connect your GitHub repository**
3. **Create New Web Service**
4. **Configure deployment:**
   - **Repository**: Your GitHub repo
   - **Branch**: main/master
   - **Root Directory**: `public-server`
   - **Runtime**: Python 3.11+

### 2. Environment Configuration

**Required Environment Variables:**
```
PORT=10000
SECRET_KEY=baby-steps-demo-secret-2025
EMERGENT_LLM_KEY=[Get from emergent_integrations_manager]
```

### 3. Build Configuration

**Build Command:**
```bash
pip install -r requirements.txt && pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

**Start Command:**
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

### 4. Get Emergent LLM Key

The backend will use the Emergent LLM key for cost-effective AI responses. Run this to get the key:

```python
from emergent_integrations_manager import get_key
key = get_key()
```

### 5. Production Backend Features

✅ **Authentication**: JWT-based user auth  
✅ **AI Chat**: `/api/ai/chat` endpoint with gpt-5-nano  
✅ **Baby Management**: Full CRUD operations  
✅ **Food Research**: AI-powered food safety  
✅ **Health Check**: `/api/health` for monitoring  

### 6. Expected Render URL

Your production backend will be available at:
```
https://baby-steps-demo-api.onrender.com
```

### 7. Update Android App

After deployment, update these files with your Render URL:

**Frontend Environment Files:**
- `/app/frontend/.env`
- `/app/frontend/.env.production` 
- `/app/frontend/.env.local`

**GitHub Workflow:**
- `/app/.github/workflows/android-build.yml`

**Android Network Config:**
- `/app/frontend/android/app/src/main/res/xml/network_security_config.xml`

**Capacitor Config:**
- `/app/frontend/capacitor.config.json`

## 🧪 Testing Production Backend

### Test Endpoints:

```bash
# Health Check
curl https://baby-steps-demo-api.onrender.com/api/health

# Register User
curl -X POST https://baby-steps-demo-api.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","name":"Test User"}'

# Login
curl -X POST https://baby-steps-demo-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# AI Chat (with JWT token)
curl -X POST https://baby-steps-demo-api.onrender.com/api/ai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message":"What foods can my baby eat?","baby_age_months":12}'
```

## 📱 Android App Update Process

1. **Update all backend URLs** (use BACKEND_URL_LOCATIONS.md)
2. **Rebuild Android app** with production backend
3. **Test authentication** and AI chat functionality  
4. **Deploy to Google Play** for production release

## 💡 Cost Optimization

- **Free Render Plan**: Good for testing and low traffic
- **Paid Plans**: Upgrade when you reach user limits
- **gpt-5-nano**: Cost-effective AI model for production use
- **Emergent LLM**: Unified key across OpenAI, Claude, Gemini

## 🔧 Monitoring

- **Health Check**: `/api/health` 
- **Logs**: Available in Render dashboard
- **Uptime**: Render handles automatic restarts
- **Scaling**: Auto-scales based on traffic