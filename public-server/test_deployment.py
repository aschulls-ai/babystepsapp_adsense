#!/usr/bin/env python3
"""
Test script to verify backend deployment readiness
"""
import sys
import subprocess

def test_imports():
    """Test that all required imports work"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import passlib
        import httpx
        from dotenv import load_dotenv
        print("✅ Standard dependencies imported successfully")
        
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        print("✅ Emergent integrations imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_startup():
    """Test that the app can start without errors"""
    try:
        from app import app
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ App startup error: {e}")
        return False

def main():
    print("🔧 Testing Render deployment readiness...")
    
    # Test imports
    if not test_imports():
        print("❌ Dependency test failed")
        sys.exit(1)
    
    # Test app startup
    if not test_app_startup():
        print("❌ App startup test failed")
        sys.exit(1)
    
    print("✅ All tests passed - ready for Render deployment!")
    print("\n🚀 Deploy steps:")
    print("1. Push changes to GitHub")
    print("2. Redeploy on Render.com")
    print("3. Test endpoints once deployed")

if __name__ == "__main__":
    main()