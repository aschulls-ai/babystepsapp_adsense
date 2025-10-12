#!/usr/bin/env python3
"""
Baby Steps - Public Demo Server
FastAPI backend with PostgreSQL support for production
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import uuid
import json
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Import database configuration
from database import (
    get_db, init_database, init_demo_data,
    User, Baby, Activity
)

# Try to import AI functionality
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    AI_AVAILABLE = True
    print("✅ AI integration available")
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ AI integration not available - using fallback responses")
    # Create mock classes for deployment without emergentintegrations
    class LlmChat:
        def __init__(self, *args, **kwargs):
            pass
        def with_model(self, *args, **kwargs):
            return self
        async def send_message(self, message):
            return "AI service temporarily unavailable. Please try again later."
    
    class UserMessage:
        def __init__(self, text):
            self.text = text

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "demo-baby-steps-secret-key-2025")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480
EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

# OLD SQLite functions - DEPRECATED - kept for reference only
# Using new SQLAlchemy functions from database.py instead

def init_database_old_sqlite():
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

def get_db_connection_old_sqlite():
    """OLD - Get SQLite database connection - DEPRECATED"""
    import sqlite3
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

# CORS middleware - Enhanced for mobile apps and Android WebView
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],  # Allow all headers for maximum compatibility
    expose_headers=["*"],
    max_age=3600  # Cache preflight requests for 1 hour
)

# Request logging middleware for debugging mobile connections
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"📱 Incoming request: {request.method} {request.url.path}")
    print(f"   Origin: {request.headers.get('origin', 'none')}")
    print(f"   User-Agent: {request.headers.get('user-agent', 'unknown')[:100]}")
    response = await call_next(request)
    print(f"   Response: {response.status_code}")
    return response

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

# OLD SQLite demo data initialization - DEPRECATED
def init_demo_data_old_sqlite():
    """OLD - Initialize demo data if not exists - DEPRECATED"""
    conn = get_db_connection_old_sqlite()
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
# Using new SQLAlchemy-based functions imported from database.py at top of file
init_database()  # This calls the NEW function from database.py
init_demo_data()  # This calls the NEW function from database.py

# Root endpoint
@app.get("/")
async def root(request: Request):
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
async def login(login_data: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    # Enhanced logging for debugging mobile connections
    print(f"Login attempt from: {http_request.client.host if http_request.client else 'unknown'}")
    print(f"User-Agent: {http_request.headers.get('user-agent', 'unknown')}")
    print(f"Email: {login_data.email}")
    
    # Debug: List all users in database
    all_users = db.query(User).all()
    print(f"🔍 DEBUG: Users in database: {[u.email for u in all_users]}")
    
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user:
        print(f"❌ User not found in database: {login_data.email}")
        print(f"✅ Using PostgreSQL - user data persists across restarts!")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.password != login_data.password:
        print(f"❌ Password mismatch for {login_data.email}")
        print(f"🔍 DEBUG: Stored password length: {len(user.password)}, Provided: {len(login_data.password)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": login_data.email})
    print(f"✅ Successful login for {login_data.email}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/register") 
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        email=request.email,
        name=request.name,
        password=request.password  # In production, should be hashed
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        access_token = create_access_token(data={"sub": request.email})
        print(f"✅ New user registered: {request.email} (PostgreSQL - persistent!)")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        db.rollback()
        print(f"❌ Registration failed for {request.email}: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

# User endpoints
@app.get("/api/user/profile")
async def get_profile(current_user_email: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, email, name FROM users WHERE email = ?", (current_user_email,))
    user = cursor.fetchone()
    conn.close()
    
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user
    cursor.execute("SELECT id FROM users WHERE email = ?", (current_user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's babies
    cursor.execute("SELECT id, name, birth_date, gender, profile_image, user_id FROM babies WHERE user_id = ?", (user["id"],))
    babies = cursor.fetchall()
    conn.close()
    
    return [Baby(**dict(baby)) for baby in babies]

@app.post("/api/babies")
async def create_baby(request: BabyCreateRequest, current_user_email: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user
    cursor.execute("SELECT id FROM users WHERE email = ?", (current_user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    baby_id = str(uuid.uuid4())
    try:
        cursor.execute("""
            INSERT INTO babies (id, name, birth_date, gender, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (baby_id, request.name, request.birth_date, request.gender, user["id"]))
        
        conn.commit()
        conn.close()
        
        baby_data = {
            "id": baby_id,
            "name": request.name,
            "birth_date": request.birth_date,
            "gender": request.gender,
            "profile_image": None,
            "user_id": user["id"]
        }
        
        print(f"✅ New baby created: {request.name}")
        return Baby(**baby_data)
        
    except Exception as e:
        conn.close()
        print(f"❌ Baby creation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to create baby")

@app.get("/api/babies/{baby_id}")
async def get_baby(baby_id: str, current_user_email: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user
    cursor.execute("SELECT id FROM users WHERE email = ?", (current_user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get baby
    cursor.execute("SELECT id, name, birth_date, gender, profile_image, user_id FROM babies WHERE id = ? AND user_id = ?", (baby_id, user["id"]))
    baby = cursor.fetchone()
    conn.close()
    
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    return Baby(**dict(baby))

@app.put("/api/babies/{baby_id}")
async def update_baby(baby_id: str, request: BabyCreateRequest, current_user_email: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user
    cursor.execute("SELECT id FROM users WHERE email = ?", (current_user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if baby exists and belongs to user
    cursor.execute("SELECT id FROM babies WHERE id = ? AND user_id = ?", (baby_id, user["id"]))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Baby not found")
    
    # Update baby
    try:
        cursor.execute("""
            UPDATE babies SET name = ?, birth_date = ?, gender = ?
            WHERE id = ? AND user_id = ?
        """, (request.name, request.birth_date, request.gender, baby_id, user["id"]))
        
        conn.commit()
        
        # Get updated baby
        cursor.execute("SELECT id, name, birth_date, gender, profile_image, user_id FROM babies WHERE id = ?", (baby_id,))
        baby = cursor.fetchone()
        conn.close()
        
        print(f"✅ Baby updated: {request.name}")
        return Baby(**dict(baby))
        
    except Exception as e:
        conn.close()
        print(f"❌ Baby update failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to update baby")

# Activity endpoints
@app.get("/api/activities")
async def get_activities(current_user_email: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user
    cursor.execute("SELECT id FROM users WHERE email = ?", (current_user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's activities
    cursor.execute("""
        SELECT id, type, notes, baby_id, user_id, timestamp 
        FROM activities 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    """, (user["id"],))
    activities = cursor.fetchall()
    conn.close()
    
    return [dict(activity) for activity in activities]

@app.post("/api/activities")
async def create_activity(request: ActivityRequest, current_user_email: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user
    cursor.execute("SELECT id FROM users WHERE email = ?", (current_user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify baby belongs to user
    cursor.execute("SELECT id FROM babies WHERE id = ? AND user_id = ?", (request.baby_id, user["id"]))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Baby not found")
    
    activity_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    try:
        cursor.execute("""
            INSERT INTO activities (id, type, notes, baby_id, user_id, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (activity_id, request.type, request.notes, request.baby_id, user["id"], timestamp))
        
        conn.commit()
        conn.close()
        
        activity = {
            "id": activity_id,
            "type": request.type,
            "notes": request.notes,
            "baby_id": request.baby_id,
            "user_id": user["id"],
            "timestamp": timestamp
        }
        
        print(f"✅ Activity created: {request.type}")
        return activity
        
    except Exception as e:
        conn.close()
        print(f"❌ Activity creation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to create activity")

# AI-powered food research endpoint
@app.post("/api/food/research")
async def food_research(request: dict, current_user_email: str = Depends(get_current_user)):
    query = request.get("query", request.get("question", ""))
    baby_age_months = request.get("baby_age_months", 6)
    
    print(f"🔬 Food research request: {query} (baby age: {baby_age_months} months)")
    
    # Try AI-powered response if available
    if AI_AVAILABLE and EMERGENT_LLM_KEY:
        try:
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"food_research_{uuid.uuid4()}",
                system_message=f"You are a pediatric nutrition expert. Provide safe, evidence-based food safety information for a {baby_age_months}-month-old baby. Include safety level (safe/caution/avoid), age recommendations, and trusted sources."
            ).with_model("openai", "gpt-4o-mini")
            
            user_message = UserMessage(text=f"Is '{query}' safe for a {baby_age_months}-month-old baby? Provide detailed safety information including when it can be introduced, preparation tips, and potential risks.")
            
            response = await chat.send_message(user_message)
            
            # Parse AI response and format it
            return {
                "answer": response,
                "safety_level": "ai_assessed",
                "age_recommendation": f"Based on {baby_age_months} months old",
                "sources": ["AI-Powered Pediatric Nutrition Assessment", "Evidence-Based Guidelines"]
            }
            
        except Exception as e:
            print(f"❌ AI food research failed: {e}")
            # Fall through to fallback responses
    
    # Fallback responses for common queries
    responses = {
        "honey": {
            "answer": "🚫 Honey should NOT be given to babies under 12 months old due to the risk of infant botulism. Botulism spores can be found in honey and can cause serious illness in infants whose immune systems aren't fully developed.",
            "safety_level": "avoid",
            "age_recommendation": "12+ months only",
            "sources": ["American Academy of Pediatrics", "CDC Guidelines"]
        },
        "strawberries": {
            "answer": "🍓 Fresh strawberries can be introduced around 6 months when baby starts solids. Cut into small, age-appropriate pieces to prevent choking. Start with small amounts and watch for allergic reactions.",
            "safety_level": "safe",
            "age_recommendation": "6+ months", 
            "sources": ["Pediatric Nutrition Guidelines", "AAP Feeding Guidelines"]
        },
        "nuts": {
            "answer": "🥜 Whole nuts are a choking hazard for babies. Nut butters can be introduced around 6 months but should be thinned with water or breast milk. Watch carefully for allergic reactions.",
            "safety_level": "caution",
            "age_recommendation": "6+ months (as nut butter only)",
            "sources": ["Food Allergy Research Guidelines"]
        },
        "eggs": {
            "answer": "🥚 Eggs can be introduced around 6 months old. Start with well-cooked eggs to reduce allergy risk. Scrambled, hard-boiled, or as part of other foods are good options.",
            "safety_level": "safe",
            "age_recommendation": "6+ months",
            "sources": ["AAP Guidelines", "Food Allergy Prevention Guidelines"]
        }
    }
    
    # Simple keyword matching
    for keyword, response in responses.items():
        if keyword.lower() in query.lower():
            return response
    
    # Default response
    return {
        "answer": f"For safety information about '{query}' for a {baby_age_months}-month-old baby, please consult your pediatrician for personalized advice.",
        "safety_level": "consult_doctor",
        "age_recommendation": "Ask your doctor",
        "sources": ["Pediatric Guidelines"]
    }

# AI-powered meal planner endpoint
@app.post("/api/meals/search")
async def meal_search(request: dict, current_user_email: str = Depends(get_current_user)):
    query = request.get("query", "")
    age_months = request.get("baby_age_months", request.get("age_months", 6))
    
    print(f"🍽️ Meal search request: {query} (baby age: {age_months} months)")
    
    # Try AI-powered response if available
    if AI_AVAILABLE and EMERGENT_LLM_KEY:
        try:
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"meal_search_{uuid.uuid4()}",
                system_message=f"You are a pediatric nutrition expert. Provide age-appropriate meal ideas with detailed recipes, ingredients, instructions, and safety tips for a {age_months}-month-old baby. Focus on nutrition, safety, and development-appropriate textures."
            ).with_model("openai", "gpt-4o-mini")
            
            user_message = UserMessage(text=f"Provide meal ideas for: '{query}' suitable for a {age_months}-month-old baby. Include 3-5 recipe suggestions with ingredients, step-by-step instructions, age appropriateness, prep time, and safety tips.")
            
            response = await chat.send_message(user_message)
            
            # For now, return the AI response in a simple format
            # In a production app, you'd parse this into structured meal objects
            return {
                "results": [{
                    "name": "AI-Generated Meal Ideas",
                    "description": response,
                    "age_appropriate": f"{age_months}+ months",
                    "source": "AI-Powered Nutrition Expert"
                }],
                "query": query,
                "age_months": age_months,
                "ai_powered": True
            }
            
        except Exception as e:
            print(f"❌ AI meal search failed: {e}")
            # Fall through to fallback responses
    
    # Fallback meal suggestions
    if age_months >= 6:
        meals = [
            {
                "name": "Mashed Banana",
                "ingredients": ["1 ripe banana"],
                "instructions": ["Mash banana with fork until smooth", "Ensure no lumps for younger babies", "Serve at room temperature"],
                "age_appropriate": "6+ months",
                "prep_time": "2 minutes",
                "safety_tips": ["Always test temperature", "Supervise eating", "Watch for choking"]
            },
            {
                "name": "Sweet Potato Puree", 
                "ingredients": ["1 sweet potato", "Water or breast milk"],
                "instructions": ["Steam sweet potato until very soft (15-20 min)", "Mash with liquid to desired consistency", "Cool before serving"],
                "age_appropriate": "6+ months",
                "prep_time": "25 minutes", 
                "safety_tips": ["Check temperature", "Start with thin consistency", "No added salt or sugar"]
            },
            {
                "name": "Avocado Mash",
                "ingredients": ["1/2 ripe avocado"],
                "instructions": ["Mash avocado until smooth", "Add breast milk if needed for consistency", "Serve immediately"],
                "age_appropriate": "6+ months",
                "prep_time": "1 minute",
                "safety_tips": ["Use very ripe avocado", "Serve fresh", "Watch for allergies"]
            }
        ]
    else:
        meals = [
            {
                "name": "Breast Milk or Formula",
                "ingredients": ["Breast milk or appropriate infant formula"],
                "instructions": ["Follow feeding schedule as recommended by pediatrician"],
                "age_appropriate": "0+ months",
                "prep_time": "As needed",
                "safety_tips": ["Consult pediatrician for feeding schedule", "No solid foods before 6 months"]
            }
        ]
    
    if age_months >= 8:
        meals.extend([
            {
                "name": "Soft Scrambled Eggs",
                "ingredients": ["1 egg", "1 tbsp milk", "Small amount of butter"],
                "instructions": ["Whisk egg with milk", "Cook on very low heat, stirring constantly", "Ensure very soft texture", "Cool before serving"],
                "age_appropriate": "8+ months",
                "prep_time": "5 minutes",
                "safety_tips": ["Cook thoroughly", "Cool to room temperature", "Watch for egg allergies", "Cut into small pieces"]
            }
        ])
    
    return {"results": meals, "query": query, "age_months": age_months}

# AI-powered general research endpoint
@app.post("/api/research")
async def research(request: dict, current_user_email: str = Depends(get_current_user)):
    query = request.get("query", request.get("question", ""))
    
    print(f"📚 Research request: {query}")
    
    # Try AI-powered response if available
    if AI_AVAILABLE and EMERGENT_LLM_KEY:
        try:
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"research_{uuid.uuid4()}",
                system_message="You are a helpful parenting and child development expert. Provide evidence-based, practical advice for parents. Always remind users to consult healthcare professionals for medical concerns."
            ).with_model("openai", "gpt-4o-mini")
            
            user_message = UserMessage(text=f"Parent question: {query}. Please provide helpful, evidence-based information while reminding them to consult healthcare professionals for medical advice.")
            
            response = await chat.send_message(user_message)
            
            return {
                "answer": response,
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "sources": ["AI-Powered Parenting Expert", "Evidence-Based Guidelines"],
                "ai_powered": True
            }
            
        except Exception as e:
            print(f"❌ AI research failed: {e}")
            # Fall through to fallback
    
    # Fallback response
    return {
        "answer": f"Here's some general parenting information about: {query}. For specific medical advice, please consult your pediatrician. This is a demo response - full AI functionality requires proper setup.",
        "query": query,
        "timestamp": datetime.utcnow().isoformat(),
        "sources": ["Demo Mode"]
    }

# AI Chat endpoint - matches Android app expectations
@app.post("/api/ai/chat")
async def ai_chat(request: dict, current_user_email: str = Depends(get_current_user)):
    """
    AI Chat endpoint for Android app - uses gpt-5-nano model for cost-effectiveness
    Expected request format: {"message": "user question", "baby_age_months": 15}
    """
    message = request.get("message", "")
    baby_age_months = request.get("baby_age_months")
    
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message is required")
    
    print(f"🤖 AI Chat request: {message} (baby age: {baby_age_months} months)")
    
    # Try AI-powered response if available
    if AI_AVAILABLE and EMERGENT_LLM_KEY:
        try:
            # Create specialized system message for baby care
            system_prompt = "You are an expert parenting and baby care assistant. Provide helpful, evidence-based advice about baby care, nutrition, safety, development, and parenting. Always prioritize safety and recommend consulting pediatricians for medical concerns."
            
            # Add baby age context if provided
            if baby_age_months is not None:
                system_prompt += f" The baby is {baby_age_months} months old - tailor your advice appropriately for this age."
            
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"ai_chat_{uuid.uuid4()}",
                system_message=system_prompt
            ).with_model("openai", "gpt-5-nano")  # Use cost-effective gpt-5-nano model
            
            user_message = UserMessage(text=message)
            response = await chat.send_message(user_message)
            
            return {
                "response": response,
                "timestamp": datetime.utcnow().isoformat(),
                "model": "gpt-5-nano"
            }
            
        except Exception as e:
            print(f"❌ AI chat failed: {e}")
            # Fall through to fallback response
    
    # Fallback response when AI is not available
    fallback_response = f"I understand you're asking about: {message}. "
    
    if baby_age_months is not None:
        fallback_response += f"For a {baby_age_months}-month-old baby, "
    
    fallback_response += "I'd recommend consulting with your pediatrician for personalized advice. This is a demo response - full AI functionality requires proper setup."
    
    return {
        "response": fallback_response,
        "timestamp": datetime.utcnow().isoformat(),
        "model": "fallback"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)