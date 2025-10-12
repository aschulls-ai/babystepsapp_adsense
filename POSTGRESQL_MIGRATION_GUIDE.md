# PostgreSQL Migration Guide - Baby Steps App

## ✅ Code Changes Complete!

All code has been updated to use PostgreSQL with SQLAlchemy. The app now:
- ✅ Uses PostgreSQL in production (persistent storage)
- ✅ Falls back to SQLite for local development
- ✅ Supports both databases seamlessly

---

## 🚀 Deployment Steps

### Step 1: Create PostgreSQL Database on Render ⏳ (Waiting for you)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `baby-steps-db`
   - **Database**: `baby_steps`
   - **Region**: Same as your web service (Oregon US West recommended)
   - **PostgreSQL Version**: 16 (latest)
   - **Plan**: **Free** (or Starter $7/month for better performance)
4. Click **"Create Database"**
5. Wait ~2 minutes for database creation

### Step 2: Get Database URL

After creation:
1. Click on your new `baby-steps-db` database
2. Scroll down to **"Connections"** section
3. **Copy "Internal Database URL"** (starts with `postgres://`)
   - Example: `postgres://baby_steps_user:xxxx@dpg-xxxx.oregon-postgres.render.com/baby_steps`
4. Keep this URL ready!

### Step 3: Add Database URL to Web Service

1. Go to your `baby-steps-demo-api` web service
2. Click **"Environment"** in left sidebar
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: [Paste the Internal Database URL you copied]
5. **Important**: Also update the Build Command:
   ```bash
   pip install -r requirements.txt && pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
   ```
6. Click **"Save Changes"**

### Step 4: Deploy

Render will automatically redeploy your service with PostgreSQL!

**Watch the logs for**:
```
✅ Using PostgreSQL database (production)
✅ Database tables created/verified
✅ Demo data created successfully
```

---

## 🧪 Testing After Deployment

### Test 1: Demo Account (Should Still Work)
```bash
curl -X POST https://baby-steps-demo-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@babysteps.com","password":"demo123"}'
```

**Expected**: 200 OK with JWT token

### Test 2: Create New User
```bash
curl -X POST https://baby-steps-demo-api.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123"}'
```

**Expected**: 200 OK with JWT token

### Test 3: Login with New User (The Critical Test!)
```bash
curl -X POST https://baby-steps-demo-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

**Expected**: 200 OK with JWT token (even after server restart!)

### Test 4: Verify Persistence

1. Create a new user (as in Test 2)
2. **Manually restart** your Render web service
3. Try to login with that user (as in Test 3)
4. **Should work!** ✅ (This is the key test - proves persistence)

---

## 📊 What Changed in the Code

### New Files Created:
- **`/app/public-server/database.py`**: SQLAlchemy models and configuration

### Updated Files:
- **`/app/public-server/requirements.txt`**: Added `psycopg2-binary` and `sqlalchemy`
- **`/app/public-server/app.py`**: 
  - Replaced SQLite queries with SQLAlchemy ORM
  - Updated login endpoint to use `db: Session = Depends(get_db)`
  - Updated register endpoint to use SQLAlchemy
  - Enhanced logging

### Database Models (SQLAlchemy):
```python
class User(Base):
    id, email, name, password, created_at

class Baby(Base):
    id, name, birth_date, gender, user_id, created_at

class Activity(Base):
    id, type, notes, baby_id, user_id, timestamp, created_at
```

---

## 🎯 Benefits of PostgreSQL

**Before (SQLite)**:
- ❌ Database wiped on every restart
- ❌ Users lost after deploy
- ❌ Demo account only reliable user
- ❌ Not production-ready

**After (PostgreSQL)**:
- ✅ Database persists across restarts
- ✅ Users never lost
- ✅ Scalable to multiple instances
- ✅ Production-ready
- ✅ Free tier available

---

## 🔧 Troubleshooting

### Issue: "No module named 'database'"
**Solution**: Make sure `database.py` is in the same directory as `app.py`

### Issue: "Could not connect to database"
**Solution**: Verify DATABASE_URL environment variable is set correctly in Render

### Issue: "relation 'users' does not exist"
**Solution**: Database tables not created. Check logs for `init_database()` output

### Issue: Build fails with psycopg2 error
**Solution**: Make sure you're using `psycopg2-binary` (not `psycopg2`) in requirements.txt

---

## 📱 After Successful Deployment

1. **Update Render Build Command** (if not done):
   ```bash
   pip install -r requirements.txt && pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
   ```

2. **Build New Android APK**:
   - Go to GitHub Actions
   - Run "Build Baby Steps Android App" workflow
   - Download v1.0123 (or latest)

3. **Test on Android**:
   - Install new APK
   - Create account
   - Logout
   - Login again
   - **Should work!** ✅

---

## 🎉 Success Checklist

- [ ] PostgreSQL database created on Render
- [ ] DATABASE_URL added to web service environment
- [ ] Build command updated (for emergentintegrations)
- [ ] Service deployed successfully
- [ ] Logs show "Using PostgreSQL database"
- [ ] Demo account login works
- [ ] New user registration works
- [ ] New user login works (critical!)
- [ ] User persists after server restart (critical!)
- [ ] AI features work (with emergentintegrations)
- [ ] Android APK rebuilt and tested

---

## 📝 Summary

**Status**: Code ready for PostgreSQL migration  
**Waiting for**: You to create PostgreSQL database on Render  
**Next**: Add DATABASE_URL to environment and deploy  
**Time**: ~10 minutes total  
**Result**: Persistent user storage that survives restarts!
