#!/usr/bin/env python3
import requests

# Your token
token = "your_token_here"

headers = {"Authorization": f"Bearer {token}"}

print("🧪 Testing your Microsoft token...")

try:
    response = requests.get("http://localhost:5001/api/helloworld", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        print("✅ SUCCESS! Your token is working!")
    else:
        print("❌ Still getting an error. Let's check details...")

except Exception as e:
    print(f"❌ Error: {e}")
