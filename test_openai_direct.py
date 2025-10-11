#!/usr/bin/env python3
"""
Direct OpenAI API test for gpt-5-nano model
"""

import os
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

def test_gpt5_nano():
    """Test gpt-5-nano model directly"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API key found")
        return False
    
    print(f"🔑 Using API key: {api_key[:20]}...")
    
    try:
        client = OpenAI(api_key=api_key)
        
        print("🤖 Testing gpt-5-nano model...")
        
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in one sentence."}
            ],
            max_completion_tokens=2000,
            reasoning_effort="low"
        )
        
        print(f"✅ Response received:")
        print(f"   Model: {response.model}")
        print(f"   Content: {response.choices[0].message.content}")
        print(f"   Usage: {response.usage}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_gpt5_nano()