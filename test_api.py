#!/usr/bin/env python3
"""
Test script for the NSS Auth Backend FastAPI
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_health_endpoint():
    """Test the health check endpoint (no auth required)"""
    print("🔍 Testing /api/health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health endpoint works!\n")
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}\n")


def test_protected_endpoint_without_token():
    """Test the protected endpoint without token (should return 403)"""
    print("🔍 Testing /api/helloworld without token...")
    try:
        response = requests.get(f"{BASE_URL}/api/helloworld")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 403:
            print("✅ Protected endpoint correctly returns 403 without token!\n")
        else:
            print(f"❌ Expected 403 but got {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error testing protected endpoint: {e}\n")


def test_protected_endpoint_with_invalid_token():
    """Test the protected endpoint with invalid token (should return 401)"""
    print("🔍 Testing /api/helloworld with invalid token...")
    try:
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = requests.get(f"{BASE_URL}/api/helloworld", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 401:
            print("✅ Protected endpoint correctly returns 401 with invalid token!\n")
        else:
            print(f"❌ Expected 401 but got {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error testing protected endpoint with invalid token: {e}\n")


def test_auth_info_endpoint():
    """Test the auth info endpoint"""
    print("🔍 Testing /api/auth/info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/info")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Auth info endpoint works!\n")
    except Exception as e:
        print(f"❌ Error testing auth info endpoint: {e}\n")


def test_api_docs():
    """Test the automatic API documentation endpoints"""
    print("🔍 Testing FastAPI documentation endpoints...")
    try:
        # Test Swagger UI
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Swagger UI (/docs): {response.status_code}")

        # Test ReDoc
        response = requests.get(f"{BASE_URL}/redoc")
        print(f"ReDoc (/redoc): {response.status_code}")

        # Test OpenAPI schema
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"OpenAPI Schema (/openapi.json): {response.status_code}")

        print("✅ All documentation endpoints work!\n")
    except Exception as e:
        print(f"❌ Error testing documentation endpoints: {e}\n")


if __name__ == "__main__":
    print("🚀 Starting FastAPI Tests...\n")

    test_health_endpoint()
    test_protected_endpoint_without_token()
    test_protected_endpoint_with_invalid_token()
    test_auth_info_endpoint()
    test_api_docs()

    print("📖 FastAPI Documentation:")
    print("   • Swagger UI: http://localhost:5000/docs")
    print("   • ReDoc: http://localhost:5000/redoc")
    print("   • OpenAPI Schema: http://localhost:5000/openapi.json")
    print("")
    print("📝 To test with a valid Microsoft token:")
    print("   1. Get a token from Azure AD")
    print(
        "   2. Run: curl -H 'Authorization: Bearer YOUR_TOKEN' http://localhost:5000/api/helloworld"
    )
    print("\n🎉 Tests completed!")
