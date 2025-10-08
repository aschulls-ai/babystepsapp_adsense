# Baby Steps Demo Server

## 🚀 Quick Deploy

### Deploy to Railway (1-Click)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/baby-steps-demo)

### Deploy to Render (1-Click)  
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR-REPO/baby-steps)

### Deploy to Vercel
```bash
npm install -g vercel
vercel --prod
```

## 📋 Server Info

- **Demo Email**: demo@babysteps.com
- **Demo Password**: demo123
- **API Base**: Your deployed URL + `/api`

## 🔗 Endpoints

- `GET /` - Server info & demo credentials
- `POST /api/auth/login` - Login
- `GET /api/babies` - Get user's babies
- `POST /api/activities` - Track activities
- `POST /api/food/research` - Food safety
- `POST /api/meals/search` - Meal planning

## 🧪 Quick Test

```bash
# Health check
curl YOUR_URL/api/health

# Login  
curl -X POST YOUR_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@babysteps.com", "password": "demo123"}'
```

## 🔧 Android App Setup

After deployment, update your Android app:

```bash
# Use your deployed URL
./update-android-config.sh https://your-app.railway.app
```