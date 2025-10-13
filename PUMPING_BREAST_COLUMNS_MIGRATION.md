# Pumping Left/Right Breast Columns Migration Guide

## Problem
The Analysis page Express section is designed to show separate left and right breast totals, but the database is missing the required columns (`left_breast` and `right_breast`). Currently, only the combined `amount` is being saved.

## What This Migration Does
Adds two new columns to the `activities` table:
- `left_breast` (FLOAT) - stores left breast pumped amount in oz
- `right_breast` (FLOAT) - stores right breast pumped amount in oz

## Migration Steps

### Option 1: Run Migration on Render Shell (RECOMMENDED)

1. **Open Render Shell**:
   - Go to your Render dashboard
   - Select your "baby-steps-demo-api" service
   - Click "Shell" tab

2. **Run Migration**:
   ```bash
   cd /opt/render/project/src/public-server
   python3 add_breast_columns_migration.py
   ```

3. **Verify Success**:
   You should see:
   ```
   ✅ left_breast column added
   ✅ right_breast column added
   ✅ Migration successful! Columns verified:
      - left_breast: double precision
      - right_breast: double precision
   ```

### Option 2: Run Locally with Production Database URL

1. **Get Database URL from Render**:
   - Go to Render dashboard → your service
   - Click "Environment" tab
   - Copy the `DATABASE_URL` value

2. **Set Environment Variable**:
   ```bash
   export DATABASE_URL='your_postgres_connection_string_here'
   ```

3. **Run Migration**:
   ```bash
   cd /app/public-server
   python3 add_breast_columns_migration.py
   ```

### Option 3: Manual SQL (If Direct Database Access Available)

```sql
-- Add columns
ALTER TABLE activities 
ADD COLUMN IF NOT EXISTS left_breast FLOAT;

ALTER TABLE activities 
ADD COLUMN IF NOT EXISTS right_breast FLOAT;

-- Verify
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'activities' 
AND column_name IN ('left_breast', 'right_breast');
```

## After Migration

### Backend Changes Already Applied
- ✅ `database.py` updated with new columns
- ✅ Frontend already sends `left_breast` and `right_breast` data
- ✅ Analysis page already displays left/right breast metrics

### What Will Work After Migration
1. **Activity History**: Will show left/right breast amounts for pumping logs
2. **Analysis Express Tab - Today's Overview**:
   - Left breast total (blue)
   - Right breast total (purple)
   - Total amount (orange)
3. **Analysis Express Tab - 7-Day Trends**:
   - Avg. left breast per day
   - Avg. right breast per day
   - Avg. total ounces per day

### Testing After Migration
1. Log a new pumping session with left and right breast amounts
2. Check Activity History - should show separate amounts
3. Go to Analysis > EXPRESS tab
4. Verify today's totals show left/right breakdown
5. Verify 7-day trends show left/right averages

## Important Notes

- **Existing Data**: Old pumping records will show `0.0 oz` for left/right until new sessions are logged
- **Frontend**: Already configured to send left_breast/right_breast data
- **No Restart Needed**: Database migration doesn't require service restart
- **Safe Operation**: Uses `ADD COLUMN IF NOT EXISTS` - safe to run multiple times

## Rollback (If Needed)

If you need to remove the columns:
```sql
ALTER TABLE activities DROP COLUMN IF EXISTS left_breast;
ALTER TABLE activities DROP COLUMN IF EXISTS right_breast;
```

## Support

If migration fails, check:
1. DATABASE_URL is correctly set
2. Database connection is working
3. User has ALTER TABLE permissions
4. No active queries blocking the table
