"""
Database configuration and utilities
Supports both SQLite (local) and PostgreSQL (production)
"""
import os
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Get database URL from environment or use SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Production: Use PostgreSQL
    # Render provides DATABASE_URL starting with postgres://, but SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(DATABASE_URL)
    print(f"✅ Using PostgreSQL database (production)")
else:
    # Development: Use SQLite
    DATABASE_URL = "sqlite:///./baby_steps.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    print(f"✅ Using SQLite database (development)")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)  # In production, should be hashed
    created_at = Column(DateTime, default=datetime.utcnow)

class Baby(Base):
    __tablename__ = "babies"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    gender = Column(String)
    profile_image = Column(String)  # Added missing field
    user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    notes = Column(Text)
    baby_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Feeding-specific fields
    feeding_type = Column(String)  # breast, bottle, formula, solid
    amount = Column(Float)  # in oz or ml
    
    # Pumping-specific fields (for tracking left/right breast separately)
    left_breast = Column(Float)  # left breast amount in oz
    right_breast = Column(Float)  # right breast amount in oz
    
    # Sleep-specific fields
    duration = Column(Integer)  # in minutes
    
    # Diaper-specific fields
    diaper_type = Column(String)  # wet, dirty, both
    
    # Measurement-specific fields
    weight = Column(Float)  # in lbs or kg
    height = Column(Float)  # in inches or cm
    head_circumference = Column(Float)  # in inches or cm
    temperature = Column(Float)  # in F or C
    
    # Milestone-specific fields
    title = Column(String)
    description = Column(Text)
    category = Column(String)  # physical, cognitive, social, language

class DeletionRequest(Base):
    __tablename__ = "deletion_requests"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    reason = Column(Text)
    status = Column(String, default="pending")  # pending, processing, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)

# Database initialization
def init_database():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_demo_data():
    """Initialize demo data if not exists"""
    db = SessionLocal()
    try:
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == "demo@babysteps.com").first()
        
        if not demo_user:
            print("📝 Creating demo data...")
            
            # Create demo user
            demo_user = User(
                id="demo-user-123",
                email="demo@babysteps.com",
                name="Demo Parent",
                password="demo123"
            )
            db.add(demo_user)
            
            # Create demo baby
            demo_baby = Baby(
                id="demo-baby-456",
                name="Emma",
                birth_date="2024-01-15",
                gender="girl",
                user_id="demo-user-123"
            )
            db.add(demo_baby)
            
            # Create demo activities
            activities = [
                Activity(
                    id="activity-1",
                    type="feeding",
                    notes="Formula feeding - 4oz",
                    baby_id="demo-baby-456",
                    user_id="demo-user-123",
                    timestamp="2025-10-08T10:00:00Z"
                ),
                Activity(
                    id="activity-2",
                    type="sleep",
                    notes="Nap time",
                    baby_id="demo-baby-456",
                    user_id="demo-user-123",
                    timestamp="2025-10-08T12:00:00Z"
                ),
                Activity(
                    id="activity-3",
                    type="diaper",
                    notes="Wet diaper changed",
                    baby_id="demo-baby-456",
                    user_id="demo-user-123",
                    timestamp="2025-10-08T14:30:00Z"
                )
            ]
            
            for activity in activities:
                db.add(activity)
            
            db.commit()
            print("✅ Demo data created successfully")
        else:
            print("✅ Demo data already exists")
            
    except Exception as e:
        print(f"❌ Error initializing demo data: {e}")
        db.rollback()
    finally:
        db.close()
