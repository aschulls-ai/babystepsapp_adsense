from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
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
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create the main app
app = FastAPI(title="Baby Steps API - Nutrition & Safety for Parents")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Pydantic Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
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

class Baby(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    birth_date: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BabyCreate(BaseModel):
    name: str
    birth_date: datetime

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
    cultural_context: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MealPlanCreate(BaseModel):
    baby_id: str
    age_months: int
    meal_name: str
    ingredients: List[str]
    instructions: List[str]
    nutrition_notes: Optional[str] = None
    cultural_context: Optional[str] = None

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
            if key.endswith(('_at', '_date', 'birth_date')):
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

# Authentication Routes
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
            system_message="""You are a specialized pediatric nutrition assistant following American Academy of Pediatrics (AAP) guidelines and cultural feeding practices. 

IMPORTANT: Always provide:
1. Clear safety assessment (safe/caution/avoid/consult_doctor)
2. Age-appropriate guidance 
3. Cultural sensitivity for diverse feeding practices
4. Evidence-based recommendations

For each response, assess safety level:
- "safe": Generally safe when prepared appropriately
- "caution": Safe but requires specific preparation or timing
- "avoid": Not recommended for this age
- "consult_doctor": Medical consultation recommended

Include both AAP guidelines AND acknowledge cultural feeding variations when relevant."""
        ).with_model("openai", "gpt-5")
        
        user_message = UserMessage(text=age_context + query.question)
        response = await chat.send_message(user_message)
        
        # Parse response for safety level (simple keyword detection)
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
            sources=["AAP Pediatric Guidelines", "Cultural Feeding Practices", "Evidence-based Nutrition"]
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
    # Verify baby belongs to user
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
        
        # Determine safety based on response
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
        # Default to unsafe when in doubt
        safety_check_dict = FoodSafetyCheck(
            user_id=current_user.id,
            **check_data.dict(),
            is_safe=False,
            safety_notes="Unable to assess safety at this time. Please consult your pediatrician."
        ).dict()
        
        safety_check_to_store = prepare_for_mongo(safety_check_dict)
        await db.food_safety_checks.insert_one(safety_check_to_store)
        
        return FoodSafetyCheck(**safety_check_dict)

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
        
        # Parse response into structured format
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
        
        # If parsing failed, put everything in steps
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

# Meal Planning Routes
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

@api_router.get("/meals/suggestions/{age_months}")
async def get_meal_suggestions(age_months: int, cultural_context: Optional[str] = None, current_user: User = Depends(get_current_user)):
    try:
        culture_note = f"with {cultural_context} cultural influences" if cultural_context else "with diverse cultural options"
        
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"meals_{current_user.id}",
            system_message="You are a pediatric nutrition expert specializing in age-appropriate meal planning with cultural diversity. Provide safe, nutritious meal ideas following AAP guidelines while respecting cultural feeding practices."
        ).with_model("openai", "gpt-5")
        
        question = f"Suggest 5 healthy, age-appropriate meal ideas for a {age_months} month old baby {culture_note}. Include ingredients and simple preparation steps."
        user_message = UserMessage(text=question)
        response = await chat.send_message(user_message)
        
        return {"suggestions": response, "age_months": age_months, "cultural_context": cultural_context}
    except Exception as e:
        logging.error(f"Meal suggestions error: {str(e)}")
        return {"suggestions": "Unable to generate meal suggestions at this time. Please consult your pediatrician for feeding guidance.", "age_months": age_months}

# Safety History Routes
@api_router.get("/food/safety-history", response_model=List[FoodSafetyCheck])
async def get_safety_history(baby_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id}
    if baby_id:
        query["baby_id"] = baby_id
    
    checks = await db.food_safety_checks.find(query).sort("checked_at", -1).to_list(length=None)
    return [FoodSafetyCheck(**parse_from_mongo(check)) for check in checks]

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