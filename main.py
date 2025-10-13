import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from authlib.jose import jwt, JsonWebKey
from dotenv import load_dotenv
import requests
from functools import lru_cache
import jwt as pyjwt
from pydantic import BaseModel
from typing import Optional

# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI(
    title="Sample Auth Backend",
    description="A FastAPI application with Microsoft Azure AD token validation",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc",  # ReDoc at /redoc
)

# HTTP Bearer token security
security = HTTPBearer()


# Pydantic models for responses
class HealthResponse(BaseModel):
    status: str
    service: str


class User(BaseModel):
    name: str
    email: str


class HelloWorldResponse(BaseModel):
    message: str
    user: User
    authenticated: bool


class AuthInfoResponse(BaseModel):
    tenant_id: str
    client_id: str
    auth_url: str
    token_url: str
    scope: str


class ErrorResponse(BaseModel):
    error: str


@lru_cache()
def get_settings():
    """Get cached environment settings"""
    return {
        "tenant_id": os.getenv("AZURE_TENANT_ID"),
        "client_id": os.getenv("AZURE_CLIENT_ID"),
    }


async def validate_microsoft_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Dependency to validate Microsoft JWT token"""
    token = credentials.credentials
    settings = get_settings()

    try:
        # Get tenant and client info
        tenant_id = settings["tenant_id"]
        client_id = settings["client_id"]

        print(f"🔍 Debug: tenant_id={tenant_id}, client_id={client_id}")

        if not tenant_id or not client_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Azure configuration missing",
            )

        jwks_url = f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"
        print(f"🔍 Debug: Fetching JWKS from {jwks_url}")

        # Get the JWT header to find the key ID
        header = pyjwt.get_unverified_header(token)
        print(f"🔍 Debug: JWT header: {header}")

        # Fetch the public keys from Microsoft
        response = requests.get(jwks_url)
        response.raise_for_status()
        jwks = response.json()
        print(f"🔍 Debug: Found {len(jwks.get('keys', []))} keys in JWKS")

        # Find the correct key
        key = None
        for jwk in jwks["keys"]:
            if jwk["kid"] == header["kid"]:
                key = JsonWebKey.import_key(jwk)
                print(f"🔍 Debug: Found matching key for kid: {header['kid']}")
                break

        if not key:
            print(f"❌ Debug: No key found for kid: {header['kid']}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token key"
            )

        # Verify and decode the token
        claims = jwt.decode(token, key)
        print(f"🔍 Debug: Token decoded successfully")
        print(f"🔍 Debug: Token claims: {claims}")

        # Validate issuer and audience - support both v1.0 and v2.0 endpoints
        expected_issuer_v1 = f"https://sts.windows.net/{tenant_id}/"
        expected_issuer_v2 = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
        token_issuer = claims.get("iss")

        print(f"🔍 Debug: Token issuer: {token_issuer}")
        print(f"🔍 Debug: Expected v1: {expected_issuer_v1}")
        print(f"🔍 Debug: Expected v2: {expected_issuer_v2}")

        if token_issuer not in [expected_issuer_v1, expected_issuer_v2]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token issuer. Got: {token_issuer}, Expected: {expected_issuer_v1} or {expected_issuer_v2}",
            )

        token_audience = claims.get("aud")
        print(f"🔍 Debug: Token audience: {token_audience}")
        print(f"🔍 Debug: Expected audience: {client_id}")

        if token_audience != client_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token audience. Got: {token_audience}, Expected: {client_id}",
            )

        print("✅ Debug: Token validation successful!")
        return claims

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Debug: Exception during token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}",
        )


@app.get(
    "/api/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and healthy",
)
async def health_check():
    """Health check endpoint that doesn't require authentication"""
    return HealthResponse(status="healthy", service="sample-auth-backend")


@app.get(
    "/api/helloworld",
    response_model=HelloWorldResponse,
    summary="Hello World (Protected)",
    description="Protected endpoint that requires a valid Microsoft token",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized - Invalid or missing token",
        }
    },
)
async def hello_world(claims: dict = Depends(validate_microsoft_token)):
    """Hello World API that requires valid Microsoft token"""
    user_name = claims.get("name", "Unknown User")
    user_email = claims.get("email", "No email")

    return HelloWorldResponse(
        message="Hello, World!",
        user=User(name=user_name, email=user_email),
        authenticated=True,
    )


@app.get(
    "/api/auth/info",
    response_model=AuthInfoResponse,
    summary="Authentication Info",
    description="Get authentication configuration information",
)
async def auth_info():
    """Get authentication configuration info"""
    settings = get_settings()
    tenant_id = settings["tenant_id"]
    client_id = settings["client_id"]

    return AuthInfoResponse(
        tenant_id=tenant_id,
        client_id=client_id,
        auth_url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize",
        token_url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        scope="openid email profile",
    )


def main():
    """Run the FastAPI application"""
    import uvicorn

    print("🚀 Starting sample-auth-backend FastAPI...")
    print("📋 Available endpoints:")
    print("  GET /api/health - Health check (no auth required)")
    print("  GET /api/helloworld - Hello World (requires valid Microsoft token)")
    print("  GET /api/auth/info - Authentication configuration info")
    print("📖 API Documentation:")
    print("  GET /docs - Swagger UI documentation")
    print("  GET /redoc - ReDoc documentation")
    print("")
    print("🔐 To test the protected endpoint, include the Authorization header:")
    print("    Authorization: Bearer <your_microsoft_token>")
    print("")

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, log_level="info")


if __name__ == "__main__":
    main()
