#!/usr/bin/env python3
"""
Database migration script to add missing columns to PostgreSQL
Run this ONCE on the production database
"""
import os
import psycopg2
from psycopg2 import sql

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable not set")
    exit(1)

# Convert postgres:// to postgresql:// for psycopg2
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"🔗 Connecting to database...")

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("✅ Connected to PostgreSQL database")
    
    # Migration commands
    migrations = [
        # Add profile_image to babies table
        ("babies", "profile_image", "ALTER TABLE babies ADD COLUMN IF NOT EXISTS profile_image VARCHAR"),
        
        # Add activity-specific fields to activities table
        ("activities", "feeding_type", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS feeding_type VARCHAR"),
        ("activities", "amount", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS amount FLOAT"),
        ("activities", "duration", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS duration INTEGER"),
        ("activities", "diaper_type", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS diaper_type VARCHAR"),
        ("activities", "weight", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS weight FLOAT"),
        ("activities", "height", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS height FLOAT"),
        ("activities", "head_circumference", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS head_circumference FLOAT"),
        ("activities", "temperature", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS temperature FLOAT"),
        ("activities", "title", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS title VARCHAR"),
        ("activities", "description", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS description TEXT"),
        ("activities", "category", "ALTER TABLE activities ADD COLUMN IF NOT EXISTS category VARCHAR"),
    ]
    
    print("\n📝 Running migrations...")
    
    for table, column, sql_command in migrations:
        try:
            print(f"   Adding {table}.{column}...", end=" ")
            cur.execute(sql_command)
            conn.commit()
            print("✅")
        except Exception as e:
            print(f"⚠️ {str(e)}")
            conn.rollback()
    
    # Also need to change timestamp column type from VARCHAR to TIMESTAMP
    print(f"\n   Updating activities.timestamp to TIMESTAMP type...", end=" ")
    try:
        # Check current type
        cur.execute("""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'activities' AND column_name = 'timestamp'
        """)
        current_type = cur.fetchone()
        
        if current_type and current_type[0] != 'timestamp without time zone':
            # Need to convert
            cur.execute("""
                ALTER TABLE activities 
                ALTER COLUMN timestamp TYPE TIMESTAMP 
                USING timestamp::timestamp without time zone
            """)
            conn.commit()
            print("✅ Converted to TIMESTAMP")
        else:
            print("✅ Already TIMESTAMP")
    except Exception as e:
        print(f"⚠️ {str(e)}")
        conn.rollback()
    
    print("\n🎉 Migration completed successfully!")
    print("\nYou can now restart your Render service for changes to take effect.")
    
    # Close connection
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Migration failed: {str(e)}")
    exit(1)
