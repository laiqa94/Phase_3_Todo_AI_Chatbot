#!/usr/bin/env python3
"""
Test script to verify the chat endpoint works with mock authentication
"""

import requests
import json

def test_chat_endpoint():
    """Test the chat endpoint with mock authentication"""
    
    # Test data
    url = "http://127.0.0.1:8000/api/v1/1/chat"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer mock-access-token-1768855974357"
    }
    
    payload = {
        "message": "Hello, can you help me create a task?"
    }
    
    try:
        print(f"Making request to: {url}")
        print(f"Headers: {headers}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Success!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print("❌ Failed!")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_chat_endpoint()