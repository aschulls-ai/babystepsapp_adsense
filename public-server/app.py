#!/usr/bin/env python3
"""
Baby Steps - Public Demo Server
Simple FastAPI backend for Android app testing
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import uuid
import json
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
import os
import sqlite3
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import AI functionality
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    AI_AVAILABLE = True
    print("✅ AI integration available")
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ AI integration not available")

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "demo-baby-steps-secret-key-2025")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480
EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

# Database setup
DATABASE_PATH = "baby_steps.db"

def init_database():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Babies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS babies (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            gender TEXT,
            profile_image TEXT,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Activities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            notes TEXT,
            baby_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (baby_id) REFERENCES babies (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return conn

# Security
security = HTTPBearer()

# Create FastAPI app
app = FastAPI(
    title="Baby Steps Demo API",
    description="Public demo server for Baby Steps Android app",
    version="1.0.0"
)

# CORS middleware - Enhanced for mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "User-Agent",
        "Cache-Control"
    ],
    expose_headers=["*"]
)

# Pydantic Models
class User(BaseModel):
    id: str
    email: str
    name: str

class Baby(BaseModel):
    id: str
    name: str
    birth_date: str
    gender: Optional[str] = None
    profile_image: Optional[str] = None
    user_id: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class BabyCreateRequest(BaseModel):
    name: str
    birth_date: str
    gender: Optional[str] = None

class ActivityRequest(BaseModel):
    type: str
    notes: Optional[str] = None
    baby_id: str

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Initialize demo data
def init_demo_data():
    """Initialize demo data if not exists"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if demo user exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@babysteps.com",))
    if not cursor.fetchone():
        # Create demo user
        demo_user_id = "demo-user-123"
        cursor.execute("""
            INSERT INTO users (id, email, name, password)
            VALUES (?, ?, ?, ?)
        """, (demo_user_id, "demo@babysteps.com", "Demo Parent", "demo123"))
        
        # Create demo baby
        demo_baby_id = "demo-baby-456"
        cursor.execute("""
            INSERT INTO babies (id, name, birth_date, gender, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (demo_baby_id, "Emma", "2024-01-15", "girl", demo_user_id))
        
        # Create demo activities
        activities = [
            ("activity-1", "feeding", "Formula feeding - 4oz", demo_baby_id, demo_user_id, "2025-10-08T10:00:00Z"),
            ("activity-2", "sleep", "Nap time", demo_baby_id, demo_user_id, "2025-10-08T12:00:00Z"),
            ("activity-3", "diaper", "Wet diaper changed", demo_baby_id, demo_user_id, "2025-10-08T14:30:00Z")
        ]
        
        for activity in activities:
            cursor.execute("""
                INSERT INTO activities (id, type, notes, baby_id, user_id, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, activity)
        
        conn.commit()
        print("✅ Demo data initialized")
    
    conn.close()

# Initialize database and demo data on startup
init_database()
init_demo_data()

# Root endpoint
@app.get("/")
async def root(request):
    # Log request details for debugging
    print(f"Request from: {request.client.host if request.client else 'unknown'}")
    print(f"User-Agent: {request.headers.get('user-agent', 'unknown')}")
    
    return {
        "message": "Baby Steps Demo API",
        "version": "1.0.0",
        "status": "running",
        "server_time": datetime.utcnow().isoformat(),
        "demo_credentials": {
            "email": "demo@babysteps.com",
            "password": "demo123"
        }
    }

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Authentication endpoints
@app.post("/api/auth/login")
async def login(request: LoginRequest, http_request):
    # Enhanced logging for debugging mobile connections
    print(f"Login attempt from: {http_request.client.host if http_request.client else 'unknown'}")
    print(f"User-Agent: {http_request.headers.get('user-agent', 'unknown')}")
    print(f"Email: {request.email}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, email, name, password FROM users WHERE email = ?", (request.email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or user["password"] != request.password:
        print(f"Invalid login for {request.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": request.email})
    print(f"✅ Successful login for {request.email}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/register") 
async def register(request: RegisterRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (request.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    try:
        cursor.execute("""
            INSERT INTO users (id, email, name, password)
            VALUES (?, ?, ?, ?)
        """, (user_id, request.email, request.name, request.password))
        
        conn.commit()
        conn.close()
        
        access_token = create_access_token(data={"sub": request.email})
        print(f"✅ New user registered: {request.email}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        conn.close()
        print(f"❌ Registration failed for {request.email}: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

# User endpoints
@app.get("/api/user/profile")
async def get_profile(current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(
        id=user["id"],
        email=user["email"], 
        name=user["name"]
    )

# Baby endpoints
@app.get("/api/babies")
async def get_babies(current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_babies = []
    for baby in babies_db.values():
        if baby["user_id"] == user["id"]:
            user_babies.append(Baby(**baby))
    
    return user_babies

@app.post("/api/babies")
async def create_baby(request: BabyCreateRequest, current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    baby_id = str(uuid.uuid4())
    baby_data = {
        "id": baby_id,
        "name": request.name,
        "birth_date": request.birth_date,
        "gender": request.gender,
        "profile_image": None,
        "user_id": user["id"]
    }
    
    babies_db[baby_id] = baby_data
    return Baby(**baby_data)

@app.get("/api/babies/{baby_id}")
async def get_baby(baby_id: str, current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    baby = babies_db.get(baby_id)
    if not baby or baby["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    return Baby(**baby)

@app.put("/api/babies/{baby_id}")
async def update_baby(baby_id: str, request: BabyCreateRequest, current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    baby = babies_db.get(baby_id)
    if not baby or baby["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    # Update baby data
    baby.update({
        "name": request.name,
        "birth_date": request.birth_date,
        "gender": request.gender
    })
    
    return Baby(**baby)

# Activity endpoints
@app.get("/api/activities")
async def get_activities(current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_activities = activities_db.get(user["id"], [])
    return user_activities

@app.post("/api/activities")
async def create_activity(request: ActivityRequest, current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify baby belongs to user
    baby = babies_db.get(request.baby_id)
    if not baby or baby["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    activity = {
        "id": str(uuid.uuid4()),
        "type": request.type,
        "notes": request.notes,
        "baby_id": request.baby_id,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if user["id"] not in activities_db:
        activities_db[user["id"]] = []
    
    activities_db[user["id"]].append(activity)
    return activity

# Food research endpoint (simplified)
@app.post("/api/food/research")
async def food_research(request: dict, current_user_email: str = Depends(get_current_user)):
    query = request.get("query", "")
    
    # Simple mock responses for common queries
    responses = {
        "honey": {
            "answer": "Honey should NOT be given to babies under 12 months old due to the risk of infant botulism.",
            "safety_level": "avoid",
            "age_recommendation": "12+ months",
            "sources": ["American Academy of Pediatrics"]
        },
        "strawberries": {
            "answer": "Fresh strawberries can be introduced around 6 months old when baby starts solids.",
            "safety_level": "safe",
            "age_recommendation": "6+ months", 
            "sources": ["Pediatric Guidelines"]
        }
    }
    
    # Simple keyword matching
    for keyword, response in responses.items():
        if keyword.lower() in query.lower():
            return response
    
    # Default response
    return {
        "answer": f"For safety information about '{query}', please consult your pediatrician.",
        "safety_level": "consult_doctor",
        "age_recommendation": "Ask your doctor",
        "sources": ["Pediatric Guidelines"]
    }

# Meal planner endpoint (simplified)
@app.post("/api/meals/search")
async def meal_search(request: dict, current_user_email: str = Depends(get_current_user)):
    query = request.get("query", "")
    age_months = request.get("age_months", 6)
    
    meals = [
        {
            "name": "Mashed Banana",
            "ingredients": ["1 ripe banana"],
            "instructions": ["Mash banana with fork until smooth", "Serve at room temperature"],
            "age_appropriate": "6+ months"
        },
        {
            "name": "Sweet Potato Puree", 
            "ingredients": ["1 sweet potato", "Water"],
            "instructions": ["Steam sweet potato until soft", "Mash with water to desired consistency"],
            "age_appropriate": "6+ months"
        },
        {
            "name": "Avocado Mash",
            "ingredients": ["1/2 ripe avocado"],
            "instructions": ["Mash avocado until smooth", "Serve immediately"],
            "age_appropriate": "6+ months"
        }
    ]
    
    return {"results": meals, "query": query, "age_months": age_months}

# General research endpoint
@app.post("/api/research")
async def research(request: dict, current_user_email: str = Depends(get_current_user)):
    query = request.get("query", "")
    
    return {
        "response": f"Here's some general parenting information about: {query}. For specific medical advice, please consult your pediatrician.",
        "query": query,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)