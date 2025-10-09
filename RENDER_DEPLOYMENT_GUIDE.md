# Render Deployment Guide for Baby Steps Backend - UPDATED

## Quick Deployment Steps

1. **Create a new Render Web Service**
   - Go to https://render.com
   - Click "New" → "Web Service"
   - Connect your repository or upload the `/app/public-server` folder

2. **Configuration**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.9+

3. **Environment Variables**
   ```
   PORT=10000
   SECRET_KEY=baby-steps-demo-secret-2025
   EMERGENT_LLM_KEY=sk-emergent-41bA272B05dA9709c3
   ```

4. **Health Check**
   - Path: `/api/health`

## Files to Deploy

Copy these files from `/app/public-server/` to your Render deployment:

- `app.py` - Main FastAPI application with SQLite database
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration (optional)
- `Procfile` - For Heroku-style deployment (optional)
- `runtime.txt` - Python version specification

## Features Included

- ✅ SQLite database for data persistence
- ✅ JWT authentication
- ✅ User registration and login
- ✅ Baby profile management
- ✅ Activity tracking
- ✅ AI-powered food research (with fallback)
- ✅ Meal planning suggestions
- ✅ General parenting research
- ✅ CORS enabled for frontend integration

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/user/profile` - Get user profile
- `GET /api/babies` - Get user's babies
- `POST /api/babies` - Create new baby
- `PUT /api/babies/{baby_id}` - Update baby
- `GET /api/activities` - Get activities
- `POST /api/activities` - Log activity
- `POST /api/food/research` - AI food safety research
- `POST /api/meals/search` - AI meal planning
- `POST /api/research` - General parenting research

## Testing After Deployment

Use the test script:

```bash
python test_deployed_backend.py
```

## Troubleshooting

1. **Build Fails**: Check requirements.txt syntax
2. **Server Won't Start**: Verify PORT environment variable
3. **Database Issues**: SQLite file will be created automatically
4. **AI Features**: Will use fallback responses if emergentintegrations unavailable

## Production Considerations

- Database is stored in container (ephemeral on free tier)
- For persistent data, upgrade to paid plan with persistent disk
- Monitor logs for any issues
- Consider adding rate limiting for production use