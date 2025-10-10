from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import json
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from emergentintegrations.llm.chat import LlmChat, UserMessage
import secrets
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-key')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours for multiple device support

# Email Configuration
VERIFICATION_TOKEN_EXPIRE_HOURS = 24
RESET_TOKEN_EXPIRE_MINUTES = 60
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

# Create the main app
app = FastAPI(title="Baby Steps - Complete Parenting Companion")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Pydantic Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    email_verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Email-related models
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

class EmailVerification(BaseModel):
    token: str

# Dashboard Widget Models
class DashboardWidget(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # 'baby_profile', 'recent_activities', 'food_safety', 'emergency_training', etc.
    title: str
    size: str = "medium"  # 'small', 'medium', 'large'
    position: Dict[str, Any]  # {x: 0, y: 0, w: 2, h: 2}
    config: Dict[str, Any] = {}  # Widget-specific configuration
    enabled: bool = True

class DashboardLayout(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    widgets: List[DashboardWidget] = []
    layout_config: Dict[str, Any] = {}  # Grid settings, theme, etc.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WidgetCreate(BaseModel):
    type: str
    title: str
    size: str = "medium"
    position: Dict[str, Any]
    config: Dict[str, Any] = {}

class LayoutUpdate(BaseModel):
    widgets: List[DashboardWidget]
    layout_config: Dict[str, Any] = {}

class Baby(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    birth_date: datetime
    birth_weight: Optional[float] = None  # in pounds
    birth_length: Optional[float] = None  # in inches
    gender: Optional[str] = None
    profile_image: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BabyCreate(BaseModel):
    name: str
    birth_date: datetime
    birth_weight: Optional[float] = None
    birth_length: Optional[float] = None
    gender: Optional[str] = None
    profile_image: Optional[str] = None

# Baby Tracking Models
class Feeding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    type: str  # "bottle", "breast", "solid"
    amount: Optional[float] = None  # in oz
    duration: Optional[int] = None  # in minutes
    notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FeedingCreate(BaseModel):
    baby_id: str
    type: str
    amount: Optional[float] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

class Diaper(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    type: str  # "wet", "dirty", "mixed"
    notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DiaperCreate(BaseModel):
    baby_id: str
    type: str
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

class Sleep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[int] = None  # in minutes
    quality: Optional[str] = None  # "good", "fair", "poor"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SleepCreate(BaseModel):
    baby_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    quality: Optional[str] = None
    notes: Optional[str] = None

class Pumping(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    amount: float  # in oz
    duration: int  # in minutes
    notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PumpingCreate(BaseModel):
    baby_id: str
    amount: float
    duration: int
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

class Measurement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    weight: Optional[float] = None  # in pounds
    height: Optional[float] = None  # in inches
    head_circumference: Optional[float] = None  # in inches
    temperature: Optional[float] = None  # in Fahrenheit
    notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MeasurementCreate(BaseModel):
    baby_id: str
    weight: Optional[float] = None
    height: Optional[float] = None
    head_circumference: Optional[float] = None
    temperature: Optional[float] = None
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

class Milestone(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    title: str
    description: Optional[str] = None
    category: str  # "physical", "cognitive", "social", "feeding", "sleep"
    achieved_date: datetime
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MilestoneCreate(BaseModel):
    baby_id: str
    title: str
    description: Optional[str] = None
    category: str
    achieved_date: datetime
    notes: Optional[str] = None

class Reminder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    title: str
    description: Optional[str] = None
    reminder_type: str  # "feeding", "pumping", "diaper_check", "medication", "appointment"
    next_due: datetime
    interval_hours: Optional[int] = None  # for recurring reminders
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReminderCreate(BaseModel):
    baby_id: str
    title: str
    description: Optional[str] = None
    reminder_type: str
    next_due: datetime
    interval_hours: Optional[int] = None

# Food Safety & Meal Planning Models - Simplified
class FoodQuery(BaseModel):
    question: str
    baby_age_months: Optional[int] = None

class FoodResponse(BaseModel):
    answer: str
    safety_level: str  # "safe", "caution", "avoid", "consult_doctor"
    age_recommendation: Optional[str] = None
    sources: List[str] = []

class EmergencyQuery(BaseModel):
    emergency_type: str  # "choking", "cpr", "general"
    baby_age_months: Optional[int] = None

class EmergencyResponse(BaseModel):
    steps: List[str]
    important_notes: List[str]
    disclaimer: str
    when_to_call_911: List[str]

class MealPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    age_months: int
    meal_name: str
    ingredients: List[str]
    instructions: List[str]
    nutrition_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MealPlanCreate(BaseModel):
    baby_id: str
    age_months: int
    meal_name: str
    ingredients: List[str]
    instructions: List[str]
    nutrition_notes: Optional[str] = None

class FoodSafetyCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    baby_id: str
    food_item: str
    age_months: int
    is_safe: bool
    safety_notes: str
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FoodSafetyCheckCreate(BaseModel):
    baby_id: str
    food_item: str
    age_months: int

# Research Models
class ResearchQuery(BaseModel):
    question: str

class ResearchResponse(BaseModel):
    answer: str
    sources: List[str] = []

# Meal Search Model - New simplified search
class MealSearchQuery(BaseModel):
    query: str
    baby_age_months: Optional[int] = None

class MealSearchResponse(BaseModel):
    results: str
    query: str
    age_months: Optional[int] = None

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Add unique token ID to support multiple concurrent sessions
    to_encode.update({"jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return User(**user)

def prepare_for_mongo(data):
    """Convert datetime objects to ISO strings for MongoDB storage"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
    return data

def parse_from_mongo(item):
    """Parse datetime strings back from MongoDB"""
    if isinstance(item, dict):
        result = {}
        for key, value in item.items():
            if key.endswith(('_at', '_time', '_date', 'timestamp', 'next_due', 'achieved_date', 'birth_date', 'start_time', 'end_time', 'checked_at')):
                if isinstance(value, str):
                    try:
                        result[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except (ValueError, TypeError):
                        result[key] = value
                else:
                    result[key] = value
            else:
                result[key] = value
        return result
    return item

# Email utility functions
def create_verification_token(email: str) -> str:
    """Create email verification token"""
    expire = datetime.now(timezone.utc) + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    to_encode = {
        "sub": email,
        "exp": expire,
        "type": "email_verification",
        "jti": secrets.token_urlsafe(16)
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_password_reset_token(email: str) -> str:
    """Create password reset token"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email,
        "exp": expire,
        "type": "password_reset",
        "jti": secrets.token_urlsafe(16)
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, expected_type: str) -> Optional[str]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email is None or token_type != expected_type:
            return None
        
        return email
    except JWTError:
        return None

async def send_verification_email_mock(email: str, verification_token: str):
    """Mock email service - logs instead of sending"""
    verification_url = f"{FRONTEND_URL}/verify-email/{verification_token}"
    
    print("\n🔔 EMAIL VERIFICATION (Mock Service)")
    print(f"📧 To: {email}")
    print("📝 Subject: Verify Your Email Address")
    print(f"🔗 Verification URL: {verification_url}")
    print(f"⏰ Expires: {datetime.now(timezone.utc) + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)}")
    print("=" * 60)
    
    # In production, replace this with actual email sending
    # await send_actual_email(email, verification_url)

async def send_password_reset_email_mock(email: str, reset_token: str):
    """Mock password reset email service"""
    reset_url = f"{FRONTEND_URL}/reset-password/{reset_token}"
    
    print("\n🔔 PASSWORD RESET (Mock Service)")
    print(f"📧 To: {email}")
    print("📝 Subject: Password Reset Request")
    print(f"🔗 Reset URL: {reset_url}")
    print(f"⏰ Expires: {datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)}")
    print("=" * 60)
    
    # In production, replace this with actual email sending
    # await send_actual_email(email, reset_url)

# Authentication Routes - Support multiple concurrent sessions
@api_router.post("/auth/register")
async def register(user_data: UserCreate, background_tasks: BackgroundTasks):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    user_dict = User(email=user_data.email, name=user_data.name, email_verified=False).dict()
    user_dict["hashed_password"] = hashed_password
    
    user_to_store = prepare_for_mongo(user_dict)
    await db.users.insert_one(user_to_store)
    
    # Generate verification token and send email
    verification_token = create_verification_token(user_data.email)
    background_tasks.add_task(send_verification_email_mock, user_data.email, verification_token)
    
    return {
        "message": "Account created successfully! Please check your email for verification.",
        "email": user_data.email,
        "email_verified": False
    }

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await db.users.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Email verification is optional - users can login without verifying
    # This allows immediate access to the app while still supporting email verification
    
    # Create token with longer expiry for multi-device support
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Email Verification Routes
@api_router.get("/auth/verify-email/{token}")
async def verify_email(token: str):
    """Verify email address using token"""
    email = verify_token(token, "email_verification")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Update user verification status
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"email_verified": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "message": "Email verified successfully! You can now log in.",
        "email": email
    }

@api_router.post("/auth/resend-verification")
async def resend_verification(email_data: dict, background_tasks: BackgroundTasks):
    """Resend verification email"""
    email = email_data.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    
    user = await db.users.find_one({"email": email})
    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a verification link has been sent."}
    
    if user.get("email_verified", False):
        return {"message": "Email is already verified"}
    
    # Generate new verification token and send email
    verification_token = create_verification_token(email)
    background_tasks.add_task(send_verification_email_mock, email, verification_token)
    
    return {"message": "Verification email sent successfully"}

# Password Reset Routes
@api_router.post("/auth/request-password-reset")
async def request_password_reset(email_data: PasswordResetRequest, background_tasks: BackgroundTasks):
    """Request password reset email"""
    user = await db.users.find_one({"email": email_data.email})
    
    # Always return success to prevent email enumeration
    if user:
        reset_token = create_password_reset_token(email_data.email)
        background_tasks.add_task(send_password_reset_email_mock, email_data.email, reset_token)
    
    return {"message": "If the email exists, a password reset link has been sent."}

@api_router.post("/auth/reset-password")
async def reset_password(password_data: PasswordReset):
    """Reset password using token"""
    email = verify_token(password_data.token, "password_reset")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Hash new password and update in database
    hashed_password = get_password_hash(password_data.new_password)
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"hashed_password": hashed_password}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "Password reset successfully"}

# Dashboard Management Routes
@api_router.get("/dashboard/layout")
async def get_dashboard_layout(current_user: User = Depends(get_current_user)):
    """Get user's dashboard layout"""
    layout = await db.dashboard_layouts.find_one({"user_id": current_user.id})
    
    if not layout:
        # Create default layout
        default_widgets = [
            {
                "id": str(uuid.uuid4()),
                "type": "baby_profile",
                "title": "Baby Profile",
                "size": "medium",
                "position": {"x": 0, "y": 0, "w": 6, "h": 4},
                "config": {},
                "enabled": True
            },
            {
                "id": str(uuid.uuid4()),
                "type": "recent_activities",
                "title": "Recent Activities",
                "size": "large",
                "position": {"x": 6, "y": 0, "w": 6, "h": 4},
                "config": {},
                "enabled": True
            },
            {
                "id": str(uuid.uuid4()),
                "type": "food_safety_quick",
                "title": "Food Safety Quick Check",
                "size": "medium",
                "position": {"x": 0, "y": 4, "w": 6, "h": 3},
                "config": {},
                "enabled": True
            },
            {
                "id": str(uuid.uuid4()),
                "type": "quick_stats",
                "title": "Today's Stats",
                "size": "medium",
                "position": {"x": 6, "y": 4, "w": 6, "h": 3},
                "config": {},
                "enabled": True
            },
            {
                "id": str(uuid.uuid4()),
                "type": "milestones",
                "title": "Developmental Milestones",
                "size": "medium",
                "position": {"x": 0, "y": 7, "w": 6, "h": 5},
                "config": {},
                "enabled": True
            }
        ]
        
        layout_data = {
            "id": str(uuid.uuid4()),
            "user_id": current_user.id,
            "widgets": default_widgets,
            "layout_config": {"cols": 12, "rowHeight": 60},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        layout_to_store = prepare_for_mongo(layout_data)
        await db.dashboard_layouts.insert_one(layout_to_store)
        return layout_data
    
    return parse_from_mongo(layout)

@api_router.put("/dashboard/layout")
async def update_dashboard_layout(
    layout_data: LayoutUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update user's dashboard layout"""
    update_data = {
        "widgets": [widget.dict() for widget in layout_data.widgets],
        "layout_config": layout_data.layout_config,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    result = await db.dashboard_layouts.update_one(
        {"user_id": current_user.id},
        {"$set": prepare_for_mongo(update_data)}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard layout not found"
        )
    
    return {"message": "Dashboard layout updated successfully"}

@api_router.post("/dashboard/widgets")
async def add_dashboard_widget(
    widget_data: WidgetCreate,
    current_user: User = Depends(get_current_user)
):
    """Add a new widget to user's dashboard"""
    new_widget = DashboardWidget(**widget_data.dict()).dict()
    
    result = await db.dashboard_layouts.update_one(
        {"user_id": current_user.id},
        {"$push": {"widgets": prepare_for_mongo(new_widget)}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard layout not found"
        )
    
    return {"message": "Widget added successfully", "widget": new_widget}

@api_router.delete("/dashboard/widgets/{widget_id}")
async def remove_dashboard_widget(
    widget_id: str,
    current_user: User = Depends(get_current_user)
):
    """Remove a widget from user's dashboard"""
    result = await db.dashboard_layouts.update_one(
        {"user_id": current_user.id},
        {"$pull": {"widgets": {"id": widget_id}}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found"
        )
    
    return {"message": "Widget removed successfully"}

@api_router.get("/dashboard/available-widgets")
async def get_available_widgets():
    """Get list of all available widget types"""
    available_widgets = [
        {
            "type": "baby_profile",
            "name": "Baby Profile",
            "description": "Quick overview of your baby's info and milestones",
            "icon": "👶",
            "defaultSize": "medium",
            "category": "baby"
        },
        {
            "type": "recent_activities",
            "name": "Recent Activities",
            "description": "Latest feeding, sleep, and diaper tracking",
            "icon": "📝",
            "defaultSize": "large",
            "category": "tracking"
        },
        {
            "type": "food_safety_quick",
            "name": "Food Safety Quick Check",
            "description": "Quick search for food safety questions",
            "icon": "🥗",
            "defaultSize": "medium",
            "category": "nutrition"
        },
        {
            "type": "emergency_training",
            "name": "Emergency Training",
            "description": "Quick access to CPR and choking guides",
            "icon": "🚨",
            "defaultSize": "medium",
            "category": "safety"
        },
        {
            "type": "meal_ideas",
            "name": "Meal Ideas",
            "description": "Age-appropriate meal suggestions",
            "icon": "🍼",
            "defaultSize": "medium",
            "category": "nutrition"
        },
        {
            "type": "growth_charts",
            "name": "Growth Charts",
            "description": "Baby growth trends and percentiles",
            "icon": "📊",
            "defaultSize": "large",
            "category": "tracking"
        },
        {
            "type": "quick_stats",
            "name": "Today's Stats",
            "description": "Daily summary of activities",
            "icon": "📈",
            "defaultSize": "medium",
            "category": "tracking"
        },
        {
            "type": "milestones",
            "name": "Developmental Milestones",
            "description": "Track your baby's developmental progress and upcoming milestones",
            "icon": "⭐",
            "defaultSize": "medium",
            "category": "baby"
        },
        {
            "type": "research_bookmarks",
            "name": "Research Bookmarks",
            "description": "Your saved research topics and articles",
            "icon": "🔖",
            "defaultSize": "medium",
            "category": "research"
        }
    ]
    
    return {"widgets": available_widgets}

# Temporary testing endpoint - remove in production
@api_router.post("/auth/manual-verify")
async def manual_verify_user(email_data: dict):
    """Manually verify a user for testing purposes"""
    email = email_data.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"email_verified": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User verified successfully"}

# Baby Management Routes
@api_router.post("/babies", response_model=Baby)
async def create_baby(baby_data: BabyCreate, current_user: User = Depends(get_current_user)):
    baby_dict = Baby(**baby_data.dict(), user_id=current_user.id).dict()
    baby_to_store = prepare_for_mongo(baby_dict)
    await db.babies.insert_one(baby_to_store)
    return Baby(**baby_dict)

@api_router.get("/babies", response_model=List[Baby])
async def get_babies(current_user: User = Depends(get_current_user)):
    babies = await db.babies.find({"user_id": current_user.id}).to_list(length=None)
    return [Baby(**parse_from_mongo(baby)) for baby in babies]

@api_router.put("/babies/{baby_id}", response_model=Baby)
async def update_baby(baby_id: str, baby_data: BabyCreate, current_user: User = Depends(get_current_user)):
    # Check if baby exists and belongs to current user
    existing_baby = await db.babies.find_one({"id": baby_id, "user_id": current_user.id})
    if not existing_baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    # Update baby data
    update_data = baby_data.dict()
    update_data = prepare_for_mongo(update_data)
    
    # Update the baby in database
    await db.babies.update_one(
        {"id": baby_id, "user_id": current_user.id},
        {"$set": update_data}
    )
    
    # Fetch and return updated baby
    updated_baby = await db.babies.find_one({"id": baby_id, "user_id": current_user.id})
    return Baby(**parse_from_mongo(updated_baby))

# Baby Tracking Routes (keeping all existing routes for feedings, diapers, sleep, pumping, measurements, milestones, reminders)
@api_router.post("/feedings", response_model=Feeding)
async def create_feeding(feeding_data: FeedingCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": feeding_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    feeding_dict = Feeding(**feeding_data.dict(), user_id=current_user.id).dict()
    if feeding_data.timestamp:
        feeding_dict['timestamp'] = feeding_data.timestamp
    
    feeding_to_store = prepare_for_mongo(feeding_dict)
    await db.feedings.insert_one(feeding_to_store)
    return Feeding(**feeding_dict)

@api_router.get("/feedings", response_model=List[Feeding])
async def get_feedings(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    feedings = await db.feedings.find(query).sort("timestamp", -1).to_list(length=None)
    return [Feeding(**parse_from_mongo(feeding)) for feeding in feedings]

@api_router.post("/diapers", response_model=Diaper)
async def create_diaper(diaper_data: DiaperCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": diaper_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    diaper_dict = Diaper(**diaper_data.dict(), user_id=current_user.id).dict()
    if diaper_data.timestamp:
        diaper_dict['timestamp'] = diaper_data.timestamp
    
    diaper_to_store = prepare_for_mongo(diaper_dict)
    await db.diapers.insert_one(diaper_to_store)
    return Diaper(**diaper_dict)

@api_router.get("/diapers", response_model=List[Diaper])
async def get_diapers(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    diapers = await db.diapers.find(query).sort("timestamp", -1).to_list(length=None)
    return [Diaper(**parse_from_mongo(diaper)) for diaper in diapers]

@api_router.post("/sleep", response_model=Sleep)
async def create_sleep(sleep_data: SleepCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": sleep_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    sleep_dict = Sleep(**sleep_data.dict(), user_id=current_user.id).dict()
    
    if sleep_data.end_time and sleep_data.start_time:
        duration = (sleep_data.end_time - sleep_data.start_time).total_seconds() / 60
        sleep_dict['duration'] = int(duration)
    
    sleep_to_store = prepare_for_mongo(sleep_dict)
    await db.sleep_sessions.insert_one(sleep_to_store)
    return Sleep(**sleep_dict)

@api_router.get("/sleep", response_model=List[Sleep])
async def get_sleep(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    sleep_sessions = await db.sleep_sessions.find(query).sort("start_time", -1).to_list(length=None)
    return [Sleep(**parse_from_mongo(session)) for session in sleep_sessions]

@api_router.post("/pumping", response_model=Pumping)
async def create_pumping(pumping_data: PumpingCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": pumping_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    pumping_dict = Pumping(**pumping_data.dict(), user_id=current_user.id).dict()
    if pumping_data.timestamp:
        pumping_dict['timestamp'] = pumping_data.timestamp
    
    pumping_to_store = prepare_for_mongo(pumping_dict)
    await db.pumping_sessions.insert_one(pumping_to_store)
    return Pumping(**pumping_dict)

@api_router.get("/pumping", response_model=List[Pumping])
async def get_pumping(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    pumping_sessions = await db.pumping_sessions.find(query).sort("timestamp", -1).to_list(length=None)
    return [Pumping(**parse_from_mongo(session)) for session in pumping_sessions]

@api_router.post("/measurements", response_model=Measurement)
async def create_measurement(measurement_data: MeasurementCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": measurement_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    measurement_dict = Measurement(**measurement_data.dict(), user_id=current_user.id).dict()
    if measurement_data.timestamp:
        measurement_dict['timestamp'] = measurement_data.timestamp
    
    measurement_to_store = prepare_for_mongo(measurement_dict)
    await db.measurements.insert_one(measurement_to_store)
    return Measurement(**measurement_dict)

@api_router.get("/measurements", response_model=List[Measurement])
async def get_measurements(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    measurements = await db.measurements.find(query).sort("timestamp", -1).to_list(length=None)
    return [Measurement(**parse_from_mongo(measurement)) for measurement in measurements]

@api_router.post("/milestones", response_model=Milestone)
async def create_milestone(milestone_data: MilestoneCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": milestone_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    milestone_dict = Milestone(**milestone_data.dict(), user_id=current_user.id).dict()
    milestone_to_store = prepare_for_mongo(milestone_dict)
    await db.milestones.insert_one(milestone_to_store)
    return Milestone(**milestone_dict)

@api_router.get("/milestones", response_model=List[Milestone])
async def get_milestones(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    milestones = await db.milestones.find(query).sort("achieved_date", -1).to_list(length=None)
    return [Milestone(**parse_from_mongo(milestone)) for milestone in milestones]

@api_router.post("/reminders", response_model=Reminder)
async def create_reminder(reminder_data: ReminderCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": reminder_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    reminder_dict = Reminder(**reminder_data.dict(), user_id=current_user.id).dict()
    reminder_to_store = prepare_for_mongo(reminder_dict)
    await db.reminders.insert_one(reminder_to_store)
    return Reminder(**reminder_dict)

@api_router.get("/reminders", response_model=List[Reminder])
async def get_reminders(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id, "is_active": True}
    if baby_id:
        query["baby_id"] = baby_id
    
    reminders = await db.reminders.find(query).sort("next_due", 1).to_list(length=None)
    return [Reminder(**parse_from_mongo(reminder)) for reminder in reminders]

@api_router.patch("/reminders/{reminder_id}")
async def update_reminder(reminder_id: str, update_data: dict, current_user: User = Depends(get_current_user)):
    # Check if reminder exists and belongs to current user
    existing_reminder = await db.reminders.find_one({"id": reminder_id, "user_id": current_user.id})
    if not existing_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Update reminder
    await db.reminders.update_one(
        {"id": reminder_id, "user_id": current_user.id},
        {"$set": prepare_for_mongo(update_data)}
    )
    
    return {"message": "Reminder updated successfully"}

@api_router.patch("/reminders/{reminder_id}/notified")
async def mark_reminder_notified(reminder_id: str, current_user: User = Depends(get_current_user)):
    # Check if reminder exists and belongs to current user
    existing_reminder = await db.reminders.find_one({"id": reminder_id, "user_id": current_user.id})
    if not existing_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Calculate next notification time based on frequency
    current_next_due = datetime.fromisoformat(existing_reminder['next_due'].replace('Z', '+00:00'))
    interval_hours = existing_reminder.get('interval_hours', 24)  # Default to daily
    next_due = current_next_due + timedelta(hours=interval_hours)
    
    # Update reminder with next due time
    await db.reminders.update_one(
        {"id": reminder_id, "user_id": current_user.id},
        {"$set": {"next_due": next_due.isoformat()}}
    )
    
    return {"message": "Reminder marked as notified and next due time updated"}

@api_router.delete("/reminders/{reminder_id}")
async def delete_reminder(reminder_id: str, current_user: User = Depends(get_current_user)):
    # Check if reminder exists and belongs to current user
    existing_reminder = await db.reminders.find_one({"id": reminder_id, "user_id": current_user.id})
    if not existing_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Delete reminder (or mark as inactive)
    await db.reminders.update_one(
        {"id": reminder_id, "user_id": current_user.id},
        {"$set": {"is_active": False}}
    )
    
    return {"message": "Reminder deleted successfully"}

# Dashboard/Analytics Routes
@api_router.get("/dashboard/{baby_id}")
async def get_dashboard(baby_id: str, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    now = datetime.now(timezone.utc)
    recent_feedings = await db.feedings.find(
        {"baby_id": baby_id, "user_id": current_user.id}
    ).sort("timestamp", -1).limit(5).to_list(length=None)
    
    recent_diapers = await db.diapers.find(
        {"baby_id": baby_id, "user_id": current_user.id}
    ).sort("timestamp", -1).limit(5).to_list(length=None)
    
    recent_sleep = await db.sleep_sessions.find(
        {"baby_id": baby_id, "user_id": current_user.id}
    ).sort("start_time", -1).limit(5).to_list(length=None)
    
    last_feeding_time = None
    if recent_feedings:
        last_feeding_time = recent_feedings[0]['timestamp']
        if isinstance(last_feeding_time, str):
            last_feeding_time = datetime.fromisoformat(last_feeding_time.replace('Z', '+00:00'))
    
    next_feeding_prediction = None
    if last_feeding_time:
        next_feeding_prediction = (last_feeding_time + timedelta(hours=3)).isoformat()
    
    recent_pumping = await db.pumping_sessions.find(
        {"baby_id": baby_id, "user_id": current_user.id}
    ).sort("timestamp", -1).limit(1).to_list(length=None)
    
    next_pumping_prediction = None
    if recent_pumping:
        last_pump_time = recent_pumping[0]['timestamp']
        if isinstance(last_pump_time, str):
            last_pump_time = datetime.fromisoformat(last_pump_time.replace('Z', '+00:00'))
        next_pumping_prediction = (last_pump_time + timedelta(hours=2.5)).isoformat()
    
    return {
        "baby": parse_from_mongo(baby),
        "recent_feedings": [parse_from_mongo(f) for f in recent_feedings],
        "recent_diapers": [parse_from_mongo(d) for d in recent_diapers],
        "recent_sleep": [parse_from_mongo(s) for s in recent_sleep],
        "next_feeding_prediction": next_feeding_prediction,
        "next_pumping_prediction": next_pumping_prediction,
        "stats": {
            "total_feedings_today": len([f for f in recent_feedings if 
                datetime.fromisoformat(f['timestamp'].replace('Z', '+00:00')).date() == now.date()]) if recent_feedings else 0,
            "total_diapers_today": len([d for d in recent_diapers if 
                datetime.fromisoformat(d['timestamp'].replace('Z', '+00:00')).date() == now.date()]) if recent_diapers else 0
        }
    }

# Food Research & Safety Routes
@api_router.post("/food/research", response_model=FoodResponse)
async def food_research(query: FoodQuery, current_user: User = Depends(get_current_user)):
    """
    Food safety research using ONLY JSON knowledge base (no AI)
    Returns answers from designated question IDs in food_research.json
    """
    try:
        # Load food research knowledge base JSON file
        json_file_path = "/app/frontend/public/knowledge-base/food_research.json"
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                food_kb = json.load(file)
        except FileNotFoundError:
            logging.error(f"Food research JSON file not found: {json_file_path}")
            return FoodResponse(
                answer="Food safety database is currently unavailable. Please consult your pediatrician.",
                safety_level="consult_doctor",
                age_recommendation="Unknown",
                sources=["Database Error"]
            )
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format in food research file: {str(e)}")
            return FoodResponse(
                answer="Food safety database format error. Please consult your pediatrician.",
                safety_level="consult_doctor", 
                age_recommendation="Unknown",
                sources=["Database Error"]
            )
        
        # Search for matching question in JSON knowledge base
        query_lower = query.question.lower()
        best_match = None
        best_score = 0
        
        for food_item in food_kb:
            question_lower = food_item.get('question', '').lower()
            answer_lower = food_item.get('answer', '').lower()
            
            # Calculate match score
            score = 0
            
            # Exact question match (highest priority)
            if query_lower == question_lower:
                score = 100
            elif query_lower in question_lower or question_lower in query_lower:
                score = 80
            
            # Specific food name matching with exact matching priority
            specific_food_match = False
            food_score_bonus = 0
            
            # Direct food name matching (most specific first)
            food_mappings = [
                (['strawberr', 'strawberry'], ['strawberr']),  # strawberry variations
                (['honey'], ['honey']),
                (['egg', 'eggs'], ['egg']),
                (['avocado'], ['avocado']),
                (['peanut', 'nut', 'nuts'], ['peanut', 'nut']),
                (['fish'], ['fish']),
                (['milk'], ['milk']),
                (['cheese'], ['cheese'])
            ]
            
            for query_terms, kb_terms in food_mappings:
                query_has_food = any(term in query_lower for term in query_terms)
                kb_has_food = any(term in (question_lower + ' ' + answer_lower) for term in kb_terms)
                
                if query_has_food and kb_has_food:
                    # Exact food match gets highest score
                    for query_term in query_terms:
                        for kb_term in kb_terms:
                            if query_term in query_lower and kb_term in (question_lower + ' ' + answer_lower):
                                food_score_bonus = 80  # High bonus for exact food match
                                specific_food_match = True
                                break
                        if specific_food_match:
                            break
                if specific_food_match:
                    break
            
            if specific_food_match:
                score += food_score_bonus
            
            # Only add safety keyword points if food was found
            if food_found:
                safety_keywords = ['safe', 'eat', 'when', 'can', 'baby', 'babies']
                for keyword in safety_keywords:
                    if keyword in query_lower and keyword in question_lower:
                        score += 10
            
            if score > best_score:
                best_score = score
                best_match = food_item
        
        # Return result based on match quality
        if best_match and best_score >= 50:  # Require minimum match score with food name
            question_id = best_match.get('id', 'Unknown')
            answer = best_match.get('answer', '')
            category = best_match.get('category', 'General')
            age_range = best_match.get('age_range', 'Consult pediatrician')
            
            # Extract safety level from answer content
            answer_lower = answer.lower()
            if 'not safe' in answer_lower or 'never' in answer_lower or 'avoid' in answer_lower:
                safety_level = "avoid"
            elif 'caution' in answer_lower or 'careful' in answer_lower or 'watch' in answer_lower:
                safety_level = "caution"
            elif 'safe' in answer_lower:
                safety_level = "safe"
            else:
                safety_level = "consult_doctor"
            
            return FoodResponse(
                answer=f"**{category}** ({age_range})\n\n{answer}",
                safety_level=safety_level,
                age_recommendation=age_range,
                sources=[f"Knowledge Base Question ID: {question_id}", "Verified Food Safety Database"]
            )
        else:
            # No match found - return "not available" message
            available_foods = []
            for item in food_kb[:10]:  # Show first 10 available foods
                if 'question' in item:
                    # Extract food name from question
                    question = item['question'].lower()
                    if 'honey' in question:
                        available_foods.append('Honey (12+ months)')
                    elif 'egg' in question:
                        available_foods.append('Eggs (6+ months)')
                    elif 'avocado' in question:
                        available_foods.append('Avocado (6+ months)')
                    elif 'strawberr' in question:
                        available_foods.append('Strawberries (6+ months)')
                    elif 'peanut' in question or 'nut' in question:
                        available_foods.append('Nuts/Peanuts (6+ months)')
            
            available_list = '\n'.join([f"• {food}" for food in available_foods[:5]])
            
            return FoodResponse(
                answer=f"**Food Safety Information Not Available**\n\nSorry, we don't have specific safety information for your query in our verified database.\n\n**Available in our database:**\n{available_list}\n\n**For other foods:** Please consult your pediatrician for guidance.",
                safety_level="consult_doctor",
                age_recommendation="Consult pediatrician", 
                sources=["Knowledge Base - No entry found"]
            )
            
    except Exception as e:
        logging.error(f"Food research JSON processing error: {str(e)}")
        return FoodResponse(
            answer="Unable to access food safety database. Please consult your pediatrician for specific feeding questions.",
            safety_level="consult_doctor",
            age_recommendation="Unknown",
            sources=["Database Error"]
        )

@api_router.post("/food/safety-check", response_model=FoodSafetyCheck)
async def check_food_safety(check_data: FoodSafetyCheckCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": check_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    try:
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"safety_check_{current_user.id}",
            system_message="You are a pediatric nutrition safety expert. Provide clear yes/no safety assessments for specific foods at specific ages, following AAP guidelines. Be conservative and prioritize safety."
        ).with_model("openai", "gpt-5")
        
        question = f"Is {check_data.food_item} safe for a {check_data.age_months} month old baby? Provide a brief safety assessment."
        user_message = UserMessage(text=question)
        response = await chat.send_message(user_message)
        
        is_safe = not any(word in response.lower() for word in ["no", "not safe", "avoid", "too young", "don't"])
        
        safety_check_dict = FoodSafetyCheck(
            user_id=current_user.id,
            **check_data.dict(),
            is_safe=is_safe,
            safety_notes=response
        ).dict()
        
        safety_check_to_store = prepare_for_mongo(safety_check_dict)
        await db.food_safety_checks.insert_one(safety_check_to_store)
        
        return FoodSafetyCheck(**safety_check_dict)
    except Exception as e:
        logging.error(f"Safety check error: {str(e)}")
        safety_check_dict = FoodSafetyCheck(
            user_id=current_user.id,
            **check_data.dict(),
            is_safe=False,
            safety_notes="Unable to assess safety at this time. Please consult your pediatrician."
        ).dict()
        
        safety_check_to_store = prepare_for_mongo(safety_check_dict)
        await db.food_safety_checks.insert_one(safety_check_to_store)
        
        return FoodSafetyCheck(**safety_check_dict)

@api_router.get("/food/safety-history", response_model=List[FoodSafetyCheck])
async def get_safety_history(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    checks = await db.food_safety_checks.find(query).sort("checked_at", -1).to_list(length=None)
    return [FoodSafetyCheck(**parse_from_mongo(check)) for check in checks]

# Emergency Training Routes
@api_router.post("/emergency/training", response_model=EmergencyResponse)
async def get_emergency_training(query: EmergencyQuery, current_user: User = Depends(get_current_user)):
    try:
        age_context = ""
        if query.baby_age_months is not None:
            age_context = f"for a {query.baby_age_months} month old baby"
        
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"emergency_{current_user.id}",
            system_message=f"""You are an emergency training instructor following American Heart Association (AHA) guidelines for infant emergencies.

CRITICAL: This is educational content only. Always emphasize:
1. This is NOT a substitute for formal CPR/First Aid training
2. Recommend professional certification courses
3. When in doubt, call 911 immediately
4. Provide step-by-step AHA guidelines

Format responses as:
- Clear numbered steps
- Important safety notes
- When to call 911
- Liability disclaimer

Topic: {query.emergency_type} {age_context}"""
        ).with_model("openai", "gpt-5")
        
        user_message = UserMessage(text=f"Provide step-by-step {query.emergency_type} instructions {age_context} following AHA guidelines.")
        response = await chat.send_message(user_message)
        
        lines = response.split('\n')
        steps = []
        notes = []
        call_911 = []
        
        current_section = "steps"
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if "important" in line.lower() or "note" in line.lower():
                current_section = "notes"
            elif "911" in line or "call" in line.lower():
                current_section = "911"
            elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '•', '-')):
                if current_section == "steps":
                    steps.append(line)
                elif current_section == "notes":
                    notes.append(line)
                elif current_section == "911":
                    call_911.append(line)
        
        if not steps:
            steps = [response]
        
        disclaimer = "⚠️ IMPORTANT DISCLAIMER: This information is for educational purposes only and is NOT a substitute for formal CPR/First Aid training. We strongly recommend taking an AHA-certified course. In any emergency, call 911 immediately. This app and its creators are not liable for any outcomes from using this information."
        
        return EmergencyResponse(
            steps=steps,
            important_notes=notes or ["Always call 911 in a real emergency", "This is educational content only"],
            disclaimer=disclaimer,
            when_to_call_911=call_911 or ["Baby is unconscious", "No response to intervention", "You are unsure about the situation"]
        )
        
    except Exception as e:
        logging.error(f"Emergency training error: {str(e)}")
        return EmergencyResponse(
            steps=["CALL 911 IMMEDIATELY"],
            important_notes=["Emergency information unavailable - seek immediate professional help"],
            disclaimer="Emergency information system unavailable. Call 911 for any emergency.",
            when_to_call_911=["ALWAYS - when emergency information is unavailable"]
        )

# Simplified Meal Planning Routes
@api_router.post("/meals", response_model=MealPlan)
async def create_meal_plan(meal_data: MealPlanCreate, current_user: User = Depends(get_current_user)):
    baby = await db.babies.find_one({"id": meal_data.baby_id, "user_id": current_user.id})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    meal_dict = MealPlan(**meal_data.dict(), user_id=current_user.id).dict()
    meal_to_store = prepare_for_mongo(meal_dict)
    await db.meal_plans.insert_one(meal_to_store)
    return MealPlan(**meal_dict)

@api_router.get("/meals", response_model=List[MealPlan])
async def get_meal_plans(baby_id: Optional[str] = None, age_months: Optional[int] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    if age_months is not None:
        query["age_months"] = age_months
    
    meals = await db.meal_plans.find(query).sort("created_at", -1).to_list(length=None)
    return [MealPlan(**parse_from_mongo(meal)) for meal in meals]

# New Simplified Meal Search Route
@api_router.post("/meals/search", response_model=MealSearchResponse)
async def search_meals_and_food_safety(search_query: MealSearchQuery, current_user: User = Depends(get_current_user)):
    try:
        age_context = ""
        if search_query.baby_age_months is not None:
            age_context = f"for a {search_query.baby_age_months} month old baby"
        
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"meal_search_{current_user.id}",
            system_message="""You are a pediatric nutrition expert. Provide helpful, safe meal ideas and food safety information following AAP guidelines. 

For meal searches: Include age-appropriate recipes with simple preparation steps.
For food safety questions: Provide clear safety assessments and age recommendations.
Always be concise and practical."""
        ).with_model("openai", "gpt-5")
        
        user_message = UserMessage(text=f"{search_query.query} {age_context}")
        response = await chat.send_message(user_message)
        
        return MealSearchResponse(
            results=response,
            query=search_query.query,
            age_months=search_query.baby_age_months
        )
    except Exception as e:
        logging.error(f"Meal search error: {str(e)}")
        return MealSearchResponse(
            results="Unable to search at this time. Please consult your pediatrician for feeding guidance.",
            query=search_query.query,
            age_months=search_query.baby_age_months
        )

# General Research Routes
@api_router.post("/research", response_model=ResearchResponse)
async def ask_research_question(query: ResearchQuery, current_user: User = Depends(get_current_user)):
    """
    AI Assistant research using JSON-only knowledge bases
    Searches both ai_assistant.json (general parenting) and food_research.json (food safety)
    Combines responses when both are relevant
    """
    try:
        # Load both knowledge base JSON files
        ai_assistant_path = "/app/frontend/public/knowledge-base/ai_assistant.json"
        food_research_path = "/app/frontend/public/knowledge-base/food_research.json"
        
        try:
            with open(ai_assistant_path, 'r', encoding='utf-8') as file:
                ai_assistant_kb = json.load(file)
        except FileNotFoundError:
            logging.error(f"AI Assistant JSON file not found: {ai_assistant_path}")
            ai_assistant_kb = []
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format in AI Assistant file: {str(e)}")
            ai_assistant_kb = []
            
        try:
            with open(food_research_path, 'r', encoding='utf-8') as file:
                food_research_kb = json.load(file)
        except FileNotFoundError:
            logging.error(f"Food Research JSON file not found: {food_research_path}")
            food_research_kb = []
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format in Food Research file: {str(e)}")
            food_research_kb = []
        
        # Search for matching questions in both knowledge bases
        query_lower = query.question.lower()
        matches = []
        
        # Check for clearly unrelated topics (exclude from parenting search)
        unrelated_keywords = [
            'smartphone', 'phone', 'computer', 'laptop', 'internet', 'social media', 'facebook', 'instagram',
            'car', 'driving', 'license', 'work', 'job', 'career', 'money', 'finance', 'investment',
            'weather', 'sports', 'football', 'basketball', 'politics', 'election', 'government',
            'cooking', 'recipe', 'restaurant', 'travel', 'vacation', 'hotel', 'movie', 'music',
            'adult', 'teenager', 'elderly', 'senior', 'college', 'university', 'homework'
        ]
        
        # Check if query is about clearly unrelated topics
        has_unrelated_content = any(keyword in query_lower for keyword in unrelated_keywords)
        
        # Only search AI Assistant knowledge base if query seems baby/parenting related
        parenting_context_keywords = ['baby', 'babies', 'newborn', 'infant', 'child', 'parenting', 'parent']
        has_parenting_context = any(keyword in query_lower for keyword in parenting_context_keywords)
        
        if not has_unrelated_content and has_parenting_context:
            # Search AI Assistant knowledge base
            for item in ai_assistant_kb:
                question_lower = item.get('question', '').lower()
                answer_lower = item.get('answer', '').lower()
                
                score = 0
                # Exact question match (highest priority)
                if query_lower == question_lower:
                    score = 100
                elif query_lower in question_lower or question_lower in query_lower:
                    score = 80
                
                # Require both parenting context AND topic match for scoring
                parenting_keywords = ['baby', 'newborn', 'infant', 'feed', 'feeding', 'sleep', 'sleeping', 'cry', 'crying', 'diaper', 'milk', 'development', 'milestone', 'burp', 'burping']
                parenting_match_count = 0
                for keyword in parenting_keywords:
                    if keyword in query_lower and keyword in (question_lower + ' ' + answer_lower):
                        parenting_match_count += 1
                        score += 20  # Higher points for each parenting match
                
                # Require at least one strong parenting keyword match
                if parenting_match_count > 0:
                    # Additional points for question structure (but only if parenting context exists)
                    question_keywords = ['how', 'when', 'what', 'why', 'should', 'can', 'is', 'are']
                    question_match_count = 0
                    for keyword in question_keywords:
                        if keyword in query_lower and keyword in question_lower:
                            question_match_count += 1
                    
                    # Only add question structure points if we have good parenting match
                    if question_match_count > 0 and parenting_match_count >= 1:
                        score += min(question_match_count * 3, 10)  # Max 10 points from question structure
                
                # Only include matches with meaningful parenting relevance
                if score >= 20:  # Require minimum threshold
                    matches.append({
                        'source': 'ai_assistant',
                        'item': item,
                        'score': score
                    })
        
        # Search Food Research knowledge base (only for food safety related queries)
        food_safety_context = any(keyword in query_lower for keyword in [
            'food', 'eat', 'safe', 'safety', 'feed', 'feeding', 'nutrition', 'allergy', 'allergic'
        ])
        
        # Specific food items that should trigger food research
        specific_foods = ['avocado', 'honey', 'egg', 'eggs', 'strawberr', 'nut', 'peanut', 'fish', 'milk', 'cheese', 'banana', 'apple', 'carrot']
        has_specific_food = any(food in query_lower for food in specific_foods)
        
        if (food_safety_context or has_specific_food) and not has_unrelated_content:
            for item in food_research_kb:
                question_lower = item.get('question', '').lower()
                answer_lower = item.get('answer', '').lower()
                
                score = 0
                # Exact question match (highest priority)
                if query_lower == question_lower:
                    score = 100
                elif query_lower in question_lower or question_lower in query_lower:
                    score = 80
                
                # Food name matching (REQUIRED for relevance)
                food_match_count = 0
                for food in specific_foods:
                    if food in query_lower and food in (question_lower + ' ' + answer_lower):
                        food_match_count += 1
                        score += 40  # Higher score for specific food matches
                
                # Require specific food match for food research
                if food_match_count > 0:
                    # Baby safety context (only if food was matched)
                    baby_safety_keywords = ['baby', 'babies', 'infant', 'newborn', 'child']
                    safety_keywords = ['safe', 'safety', 'eat', 'when', 'can']
                    
                    baby_context = any(keyword in query_lower for keyword in baby_safety_keywords)
                    safety_context = any(keyword in query_lower for keyword in safety_keywords)
                    
                    # Bonus points for proper baby + food safety context
                    if baby_context and safety_context:
                        score += 20
                    elif baby_context or safety_context:
                        score += 10
                
                # Only include if we have strong food + baby safety relevance
                if score >= 40:  # Higher threshold for food research
                    matches.append({
                        'source': 'food_research',
                        'item': item,
                        'score': score
                    })
        
        # Sort matches by score (highest first)
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        # Determine response strategy based on matches
        if not matches:
            # No matches found
            return ResearchResponse(
                answer="**Information Not Available**\n\nI don't have specific information about your question in our knowledge base. Our database covers common parenting topics like feeding, sleep, development milestones, and food safety.\n\n**For reliable answers:** Please consult your pediatrician, search reputable parenting websites, or check with healthcare professionals who can provide personalized guidance.",
                sources=["Knowledge Base - No entry found"]
            )
        
        # Get best matches from each source with updated thresholds
        ai_match = next((m for m in matches if m['source'] == 'ai_assistant' and m['score'] >= 20), None)
        food_match = next((m for m in matches if m['source'] == 'food_research' and m['score'] >= 40), None)
        
        combined_answer = ""
        combined_sources = []
        
        # Combine responses if both are relevant
        if ai_match and food_match and ai_match['score'] >= 20 and food_match['score'] >= 40:
            # Both are relevant - combine responses
            ai_item = ai_match['item']
            food_item = food_match['item']
            
            combined_answer = f"**General Parenting Guidance**\n"
            combined_answer += f"**{ai_item.get('category', 'General')}** ({ai_item.get('age_range', 'All ages')})\n\n"
            combined_answer += f"{ai_item.get('answer', '')}\n\n"
            
            combined_answer += f"**Food Safety Information**\n"
            combined_answer += f"**{food_item.get('category', 'Safety')}** ({food_item.get('age_range', 'Consult pediatrician')})\n\n"
            combined_answer += f"{food_item.get('answer', '')}"
            
            combined_sources = [
                f"AI Assistant Knowledge Base Question ID: {ai_item.get('id', 'Unknown')}",
                f"Food Safety Knowledge Base Question ID: {food_item.get('id', 'Unknown')}",
                "Verified Parenting & Food Safety Database"
            ]
        
        elif ai_match and ai_match['score'] >= 20:
            # Primary AI Assistant match
            item = ai_match['item']
            combined_answer = f"**{item.get('category', 'General Parenting')}** ({item.get('age_range', 'All ages')})\n\n{item.get('answer', '')}"
            combined_sources = [f"AI Assistant Knowledge Base Question ID: {item.get('id', 'Unknown')}", "Verified Parenting Guidelines"]
            
        elif food_match and food_match['score'] >= 40:
            # Primary Food Safety match
            item = food_match['item']
            combined_answer = f"**{item.get('category', 'Food Safety')}** ({item.get('age_range', 'Consult pediatrician')})\n\n{item.get('answer', '')}"
            combined_sources = [f"Food Safety Knowledge Base Question ID: {item.get('id', 'Unknown')}", "Verified Food Safety Database"]
            
        else:
            # Use best available match even if score is lower
            best_match = matches[0]
            item = best_match['item']
            source_name = "AI Assistant" if best_match['source'] == 'ai_assistant' else "Food Safety"
            combined_answer = f"**{item.get('category', source_name)}** ({item.get('age_range', 'All ages')})\n\n{item.get('answer', '')}"
            combined_sources = [f"{source_name} Knowledge Base Question ID: {item.get('id', 'Unknown')}", f"Verified {source_name} Database"]
        
        return ResearchResponse(
            answer=combined_answer,
            sources=combined_sources
        )
        
    except Exception as e:
        logging.error(f"Research query JSON processing error: {str(e)}")
        return ResearchResponse(
            answer="Unable to access parenting database. Please consult your pediatrician for specific questions about baby care, feeding, or development.",
            sources=["Database Error"]
        )

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Baby Steps API", "timestamp": datetime.now(timezone.utc).isoformat()}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()