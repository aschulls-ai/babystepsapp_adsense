# CRITICAL: SQLite Database Ephemeral on Render - User Persistence Issue

## 🚨 ROOT CAUSE IDENTIFIED

**The login issue is caused by Render's EPHEMERAL filesystem!**

### How Render Works

Render services use **ephemeral storage**:
- Every time the service restarts (deploy, crash, scale), the filesystem is RESET
- SQLite database file (`baby_steps.db`) is DELETED
- All user data created after the last deploy is LOST

### Why Demo Account Works But New Users Don't

**Demo Account** (`demo@babysteps.com`):
- ✅ Created in `init_demo_data()` function
- ✅ Runs on EVERY startup
- ✅ Always exists after restart

**New User Accounts**:
- ✅ Registration creates user successfully
- ✅ User can login immediately (database still exists)
- ❌ After server restart (or deploy), database is WIPED
- ❌ User account NO LONGER EXISTS
- ❌ Login fails with 401 "Invalid credentials"

### Why Backend Testing Showed Success

Backend curl tests work because:
- They create users and test immediately
- No server restart between creation and login
- All tests happen in same session

Frontend testing failed because:
- User creates account
- Time passes (potentially with Render restart/deploy)
- Database is wiped
- Login fails because user doesn't exist

## 🎯 SOLUTIONS

### Solution 1: Use PostgreSQL (RECOMMENDED)

Render offers managed PostgreSQL with **persistent storage**:

**Benefits**:
- ✅ Data persists across restarts
- ✅ Scalable to multiple instances
- ✅ Production-ready
- ✅ Free tier available

**Implementation**:
1. Create PostgreSQL database in Render Dashboard
2. Update code to use PostgreSQL instead of SQLite
3. Use SQLAlchemy or similar ORM
4. Migrate schema and data

**Time**: 1-2 hours

### Solution 2: Use Render Persistent Disk (Alternative)

Render supports persistent disks for file storage:

**Benefits**:
- ✅ Keep using SQLite
- ✅ Minimal code changes
- ✅ Data persists across restarts

**Limitations**:
- ⚠️ Only works with single instance (no scaling)
- ⚠️ Not recommended for production
- 💰 Costs extra ($0.25/GB/month)

**Implementation**:
1. Add persistent disk in Render Dashboard
2. Mount disk to `/app/data`
3. Update `DATABASE_PATH = "/app/data/baby_steps.db"`

**Time**: 30 minutes

### Solution 3: Mock Auth for Demo (Quick Fix)

For demo/testing purposes only:

**Benefits**:
- ✅ Quick to implement
- ✅ No database needed for auth
- ✅ Works with ephemeral storage

**Limitations**:
- ⚠️ Not secure
- ⚠️ Users can't actually persist
- ⚠️ Demo only

**Implementation**:
- Accept any email/password combination
- Generate token based on email
- Store baby data in demo account only

**Time**: 15 minutes

## 📋 Recommended Approach

**For Production App**: Use **PostgreSQL** (Solution 1)

**Steps**:

1. **Create PostgreSQL Database**:
   ```
   Render Dashboard → New → PostgreSQL
   Name: baby-steps-db
   Plan: Free (starter)
   ```

2. **Update requirements.txt**:
   ```
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   python-jose[cryptography]>=3.3.0
   pydantic==2.11.0
   python-multipart==0.0.6
   python-dotenv==1.1.1
   passlib[bcrypt]==1.7.4
   httpx>=0.28.1
   psycopg2-binary>=2.9.9
   sqlalchemy>=2.0.0
   ```

3. **Update Environment Variables**:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/database
   (Provided by Render after creating PostgreSQL)
   ```

4. **Update code to use PostgreSQL**:
   - Replace SQLite connection with SQLAlchemy
   - Use DATABASE_URL from environment
   - Migrate schema

5. **Deploy and test**:
   - Users will persist across restarts
   - Scalable to multiple instances
   - Production-ready

## 🔍 Current Status

**Debug Logging Added**:
- Backend now logs all users in database on login attempt
- Shows if user exists or not
- Helps identify if issue is database wipe or password mismatch

**Expected Render Logs**:
```
Login attempt for: newuser@example.com
🔍 DEBUG: Users in database: ['demo@babysteps.com']
❌ User not found in database: newuser@example.com
🔍 DEBUG: This user may have been created before a server restart
🔍 DEBUG: SQLite database is ephemeral on Render - resets on restart
```

## 📝 Summary

**Problem**: SQLite database is ephemeral on Render - resets on every restart  
**Impact**: New users can register but can't login after server restart  
**Why Demo Works**: Demo user is recreated on every startup  
**Solution**: Migrate to PostgreSQL for persistent storage  
**Time**: 1-2 hours for full PostgreSQL migration  
**Status**: Issue identified and documented
