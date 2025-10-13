"""
Migration script to add left_breast and right_breast columns to activities table
Run this on the Render PostgreSQL database
"""
import os
import sys
from sqlalchemy import create_engine, text

def migrate_database():
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL environment variable not set")
        print("Set it with: export DATABASE_URL='your_postgres_connection_string'")
        sys.exit(1)
    
    # Fix postgres:// to postgresql:// for SQLAlchemy
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    print(f"🔗 Connecting to database...")
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            print("\n📋 Starting migration: Adding left_breast and right_breast columns...")
            
            # Add left_breast column
            print("  ➤ Adding left_breast column...")
            connection.execute(text("""
                ALTER TABLE activities 
                ADD COLUMN IF NOT EXISTS left_breast FLOAT;
            """))
            connection.commit()
            print("  ✅ left_breast column added")
            
            # Add right_breast column
            print("  ➤ Adding right_breast column...")
            connection.execute(text("""
                ALTER TABLE activities 
                ADD COLUMN IF NOT EXISTS right_breast FLOAT;
            """))
            connection.commit()
            print("  ✅ right_breast column added")
            
            # Verify columns exist
            print("\n🔍 Verifying columns...")
            result = connection.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'activities' 
                AND column_name IN ('left_breast', 'right_breast')
                ORDER BY column_name;
            """))
            
            columns = result.fetchall()
            if len(columns) == 2:
                print("✅ Migration successful! Columns verified:")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]}")
            else:
                print(f"⚠️  Warning: Expected 2 columns, found {len(columns)}")
            
            print("\n🎉 Migration completed successfully!")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 70)
    print("PUMPING DATA MIGRATION: Add left_breast and right_breast columns")
    print("=" * 70)
    migrate_database()
