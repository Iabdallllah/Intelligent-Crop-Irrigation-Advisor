#!/usr/bin/env python3
"""Test script to verify Gemini API Service Account authentication"""

import os
import sys
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

def test_service_account_auth():
    """Test Service Account authentication with Gemini API"""
    
    # Path to service account file
    service_account_path = "frontend/streamlit_dashboard/service-account.json"
    
    if not os.path.exists(service_account_path):
        print(f"❌ Service account file not found: {service_account_path}")
        return False
    
    print(f"✓ Found service account file: {service_account_path}")
    
    try:
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/generative-language.retriever']
        )
        print("✓ Successfully loaded Service Account credentials")
        
        # Refresh to get access token
        credentials.refresh(Request())
        access_token = credentials.token
        print(f"✓ Got access token (first 20 chars): {access_token[:20]}...")
        
        # Test listing models
        print("\n📋 Testing API access by listing available models...")
        response = requests.get(
            "https://generativelanguage.googleapis.com/v1beta/models",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15
        )
        
        if response.ok:
            data = response.json()
            models = data.get("models", [])
            print(f"✅ SUCCESS! Found {len(models)} available models:")
            
            for model in models[:5]:  # Show first 5
                name = model.get("name", "").split("/")[-1]
                methods = model.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    print(f"  - {name}")
            
            if len(models) > 5:
                print(f"  ... and {len(models) - 5} more")
            
            return True
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_generation():
    """Test simple text generation with Gemini API"""
    
    service_account_path = "frontend/streamlit_dashboard/service-account.json"
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/generative-language.retriever']
        )
        credentials.refresh(Request())
        access_token = credentials.token
        
        print("\n🤖 Testing text generation with gemini-1.5-flash...")
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": "Say 'Hello from Gemini!' in a friendly way."}]
                }
            ]
        }
        
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        if response.ok:
            data = response.json()
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            print(f"✅ SUCCESS! Gemini responded:")
            print(f"\n{text}\n")
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Gemini API Service Account Authentication Test")
    print("=" * 60)
    
    # Test 1: Authentication and list models
    success1 = test_service_account_auth()
    
    # Test 2: Simple generation
    success2 = test_simple_generation()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("✅ All tests passed! Your Service Account is working correctly.")
        print("\nYou can now run the Streamlit app:")
        print("  cd frontend/streamlit_dashboard")
        print("  streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
    print("=" * 60)
