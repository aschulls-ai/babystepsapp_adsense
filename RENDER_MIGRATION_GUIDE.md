# Render PostgreSQL Database Migration Guide

## Problem Summary
The Baby Steps production backend on Render is experiencing HTTP 500 errors when creating/retrieving activities. The root cause is a **database schema mismatch**: the PostgreSQL tables are missing columns that the updated application code expects.

### Missing Columns Identified from Render Logs:
- `babies.profile_image` → `psycopg2.errors.UndefinedColumn`
- `activities.feeding_type` → `psycopg2.errors.UndefinedColumn`
- Plus 10 more activity-related columns

## Solution: Run Database Migration Script

We've created a migration script at `/app/public-server/migrate_database.py` that will add all missing columns to your PostgreSQL database.

---

## Option 1: Run Migration via Render Shell (RECOMMENDED)

### Step 1: Access Render Shell
1. Go to your Render Dashboard: https://dashboard.render.com
2. Click on your **baby-steps-demo-api** service
3. Click on the **"Shell"** tab in the left sidebar
4. This opens a terminal connected to your running service

### Step 2: Run the Migration Script
In the Render shell, run:

```bash
cd /app/public-server
python migrate_database.py
```

### Step 3: Verify Migration Success
You should see output like:
```
🔗 Connecting to database...
✅ Connected to PostgreSQL database

📝 Running migrations...
   Adding babies.profile_image... ✅
   Adding activities.feeding_type... ✅
   Adding activities.amount... ✅
   Adding activities.duration... ✅
   Adding activities.diaper_type... ✅
   Adding activities.weight... ✅
   Adding activities.height... ✅
   Adding activities.head_circumference... ✅
   Adding activities.temperature... ✅
   Adding activities.title... ✅
   Adding activities.description... ✅
   Adding activities.category... ✅

   Updating activities.timestamp to TIMESTAMP type... ✅

🎉 Migration completed successfully!
```

### Step 4: Restart Service (if needed)
The migration should take effect immediately, but you can restart the service to be safe:
- Go to your service page
- Click **"Manual Deploy"** → **"Deploy latest commit"** (or just restart)

---

## Option 2: Run Migration Locally with Production Database

If you prefer to run the migration from your local machine:

### Step 1: Get PostgreSQL Connection String
1. Go to Render Dashboard
2. Navigate to your **baby-steps-demo-api** service
3. Click on **"Environment"** in the left sidebar
4. Find and copy the **`DATABASE_URL`** value (starts with `postgres://`)

### Step 2: Run Migration Locally
```bash
# Set the DATABASE_URL environment variable
export DATABASE_URL="postgres://your-connection-string-from-render"

# Navigate to the public-server directory
cd /app/public-server

# Install psycopg2 if not already installed
pip install psycopg2-binary

# Run the migration
python migrate_database.py
```

---

## Option 3: Manual SQL Migration (Advanced)

If you prefer to run the SQL commands manually:

### Step 1: Connect to PostgreSQL
Use the Render Shell or any PostgreSQL client with your DATABASE_URL.

### Step 2: Run SQL Commands
```sql
-- Add missing column to babies table
ALTER TABLE babies ADD COLUMN IF NOT EXISTS profile_image VARCHAR;

-- Add missing columns to activities table
ALTER TABLE activities ADD COLUMN IF NOT EXISTS feeding_type VARCHAR;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS amount FLOAT;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS duration INTEGER;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS diaper_type VARCHAR;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS weight FLOAT;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS height FLOAT;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS head_circumference FLOAT;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS temperature FLOAT;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS title VARCHAR;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE activities ADD COLUMN IF NOT EXISTS category VARCHAR;

-- Update timestamp column type (optional but recommended)
ALTER TABLE activities 
ALTER COLUMN timestamp TYPE TIMESTAMP 
USING timestamp::timestamp without time zone;
```

---

## Verification After Migration

### Test 1: Health Check
```bash
curl https://baby-steps-demo-api.onrender.com/api/health
```
Expected: `{"status":"healthy"}`

### Test 2: Login
```bash
curl -X POST https://baby-steps-demo-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@babysteps.com","password":"demo123"}'
```
Expected: JWT token response

### Test 3: Create Activity (Most Important)
```bash
# First get JWT token from Test 2, then:
curl -X POST https://baby-steps-demo-api.onrender.com/api/activities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "type": "feeding",
    "baby_id": "demo-baby-456",
    "notes": "Test feeding",
    "feeding_type": "breast",
    "amount": 4.0
  }'
```
Expected: HTTP 200/201 with activity details (NOT HTTP 500)

### Test 4: Retrieve Activities
```bash
curl -X GET "https://baby-steps-demo-api.onrender.com/api/activities?baby_id=demo-baby-456" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
Expected: HTTP 200 with list of activities

---

## Expected Results After Migration

✅ **All HTTP 500 errors on activity endpoints will be resolved**
✅ **Activity creation (POST /api/activities) will return HTTP 200/201**
✅ **Activity retrieval (GET /api/activities) will return HTTP 200**
✅ **No more `psycopg2.errors.UndefinedColumn` errors in Render logs**
✅ **Baby profile images can be stored**
✅ **All activity types (feeding, diaper, sleep, etc.) will work correctly**

---

## Troubleshooting

### Error: "DATABASE_URL environment variable not set"
**Solution:** Make sure you're running the script on Render (Option 1) or have exported the DATABASE_URL locally (Option 2).

### Error: "relation 'babies' does not exist"
**Solution:** The database tables haven't been created yet. Deploy your service first to create initial tables, then run the migration.

### Error: "permission denied"
**Solution:** Make sure the PostgreSQL user has ALTER TABLE permissions. This should be the case for the default Render PostgreSQL setup.

### Migration runs but errors persist
**Solution:** 
1. Check Render logs to confirm the migration actually ran
2. Restart the Render service
3. Clear any application caches
4. Verify columns were added using: `\d activities` in PostgreSQL shell

---

## What This Migration Does

### For the `babies` table:
- Adds `profile_image` (VARCHAR) column to store baby profile image URLs

### For the `activities` table:
- Adds `feeding_type` (VARCHAR) - breast, bottle, formula, solid
- Adds `amount` (FLOAT) - feeding amount in oz/ml
- Adds `duration` (INTEGER) - sleep/activity duration in minutes
- Adds `diaper_type` (VARCHAR) - wet, dirty, both
- Adds `weight` (FLOAT) - baby weight measurements
- Adds `height` (FLOAT) - baby height measurements
- Adds `head_circumference` (FLOAT) - head circumference measurements
- Adds `temperature` (FLOAT) - temperature measurements
- Adds `title` (VARCHAR) - milestone titles
- Adds `description` (TEXT) - detailed descriptions
- Adds `category` (VARCHAR) - milestone categories (physical, cognitive, etc.)
- Updates `timestamp` column type from VARCHAR to TIMESTAMP (for proper date handling)

### Safety Features:
- Uses `ADD COLUMN IF NOT EXISTS` - safe to run multiple times
- Won't drop or modify existing data
- Won't cause downtime
- Can be run while the service is running

---

## Next Steps After Migration

1. ✅ Run the migration script using Option 1 (Render Shell - RECOMMENDED)
2. ✅ Verify migration success with the tests above
3. ✅ Report back the results
4. ✅ Once confirmed working, we'll run comprehensive backend testing

---

## Questions?
If you encounter any issues:
1. Share the complete error message from the migration script
2. Share any relevant Render logs
3. Confirm which option you're using (1, 2, or 3)
