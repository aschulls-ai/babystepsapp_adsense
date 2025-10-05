from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
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

# Authentication Routes - Support multiple concurrent sessions
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    user_dict = User(email=user_data.email, name=user_data.name).dict()
    user_dict["hashed_password"] = hashed_password
    
    user_to_store = prepare_for_mongo(user_dict)
    await db.users.insert_one(user_to_store)
    
    # Create token with longer expiry for multi-device support
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await db.users.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token with longer expiry for multi-device support
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
    try:
        age_context = ""
        if query.baby_age_months is not None:
            age_context = f"For a {query.baby_age_months} month old baby: "
        
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"food_research_{current_user.id}",
            system_message="""You are a specialized pediatric nutrition assistant following American Academy of Pediatrics (AAP) guidelines. 

IMPORTANT: Always provide:
1. Clear safety assessment (safe/caution/avoid/consult_doctor)
2. Age-appropriate guidance 
3. Evidence-based recommendations
4. Brief, practical answers

For each response, assess safety level:
- "safe": Generally safe when prepared appropriately
- "caution": Safe but requires specific preparation or timing
- "avoid": Not recommended for this age
- "consult_doctor": Medical consultation recommended"""
        ).with_model("openai", "gpt-5")
        
        user_message = UserMessage(text=age_context + query.question)
        response = await chat.send_message(user_message)
        
        # Parse response for safety level
        safety_level = "safe"
        response_lower = response.lower()
        if any(word in response_lower for word in ["avoid", "not safe", "don't give", "too young"]):
            safety_level = "avoid"
        elif any(word in response_lower for word in ["caution", "careful", "supervise", "small amounts"]):
            safety_level = "caution"
        elif any(word in response_lower for word in ["consult", "doctor", "pediatrician", "medical"]):
            safety_level = "consult_doctor"
        
        age_rec = None
        if query.baby_age_months is not None:
            if query.baby_age_months < 6:
                age_rec = "0-6 months: Breast milk or formula only"
            elif query.baby_age_months < 12:
                age_rec = "6-12 months: Introduction phase"
            else:
                age_rec = "12+ months: Varied diet"
        
        return FoodResponse(
            answer=response,
            safety_level=safety_level,
            age_recommendation=age_rec,
            sources=["AAP Pediatric Guidelines", "Evidence-based Nutrition"]
        )
    except Exception as e:
        logging.error(f"Food research error: {str(e)}")
        return FoodResponse(
            answer="I'm sorry, I'm having trouble accessing nutritional information right now. Please consult your pediatrician for specific feeding questions.",
            safety_level="consult_doctor",
            sources=[]
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
    try:
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"research_{current_user.id}",
            system_message="You are a helpful and knowledgeable parenting assistant specializing in newborn care, infant development, feeding, sleep, and general baby health. Provide accurate, evidence-based information while encouraging parents to consult healthcare providers for medical concerns. Be supportive and understanding of new parent anxieties."
        ).with_model("openai", "gpt-5")
        
        user_message = UserMessage(text=query.question)
        response = await chat.send_message(user_message)
        
        return ResearchResponse(
            answer=response,
            sources=["AI-powered parenting assistant", "Evidence-based medical guidelines"]
        )
    except Exception as e:
        logging.error(f"Research query error: {str(e)}")
        return ResearchResponse(
            answer="I'm sorry, I'm having trouble accessing the research database right now. Please try again later, or consult your pediatrician for specific medical questions.",
            sources=[]
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