# 🔐 Python Auth Backend

A FastAPI application with Microsoft Azure AD token validation using the authlib library.

## 🚀 Setup

1. **Configure Environment Variables**
   
   Update the `.env` file with your Azure AD application details:
   ```
   AZURE_CLIENT_ID=your_client_id_here
   AZURE_TENANT_ID=your_tenant_id_here
   ```

   Note: 
   - Client secret is not required since we're only validating JWT tokens, not performing OAuth flows

2. **Install Dependencies**
   ```bash
   uv sync
   ```

3. **Run the Application**
   ```bash
   uv run python main.py
   ```

## 🐋 Docker

### Building the Docker Image

Build the Docker image using the included Dockerfile:

```bash
docker build -t python-auth-backend .
```

### Running the Container

Run the container with environment variables:

```bash
docker run -d \
  -p 5000:5000 \
  -e AZURE_CLIENT_ID=your_client_id_here \
  -e AZURE_TENANT_ID=your_tenant_id_here \
  --name auth-backend \
  python-auth-backend
```

Or use an `.env` file:

```bash
docker run -d \
  -p 5000:5000 \
  --env-file .env \
  --name auth-backend \
  python-auth-backend
```

### Docker Image Details

The Dockerfile uses a multi-stage build:
- **Builder stage**: Uses Python 3.14-slim with uv for fast dependency installation
- **Runtime stage**: Minimal Python 3.14-slim image with only the compiled application
- **Port**: Exposes port 5000
- **Working directory**: `/app`
- **Entrypoint**: Runs the FastAPI application using the virtual environment's Python

### Docker Commands Reference

```bash
# Build the image
docker build -t python-auth-backend .

# Run the container
docker run -d -p 5000:5000 --env-file .env --name auth-backend python-auth-backend

# View container logs
docker logs auth-backend

# Follow container logs
docker logs -f auth-backend

# Stop the container
docker stop auth-backend

# Remove the container
docker rm auth-backend

# Remove the image
docker rmi python-auth-backend

# Access container shell
docker exec -it auth-backend /bin/bash
```

## 🌐 API Endpoints

### Public Endpoints (No Authentication Required)

- `GET /api/health` - Health check endpoint
- `GET /api/auth/info` - Get authentication configuration info

### Protected Endpoints (Requires Microsoft Token)

- `GET /api/helloworld` - Hello World endpoint that requires valid Microsoft token

### 📚 Documentation Endpoints

- `GET /docs` - Interactive Swagger UI documentation
- `GET /redoc` - ReDoc documentation
- `GET /openapi.json` - OpenAPI schema

## 💡 Usage

### Testing the Protected Endpoint

1. **Without Token (Should return 403)**
   ```bash
   curl http://localhost:5000/api/helloworld
   ```

2. **With Valid Microsoft Token**
   ```bash
   curl -H "Authorization: Bearer YOUR_MICROSOFT_TOKEN" http://localhost:5000/api/helloworld
   ```

Note: If running with uv, use `uv run python main.py` to start the server.

### 📖 Interactive API Documentation

FastAPI automatically generates interactive documentation:

1. **Swagger UI**: Visit `http://localhost:5000/docs`
   - Interactive API explorer
   - Test endpoints directly in the browser
   - Try out authentication with Bearer tokens

2. **ReDoc**: Visit `http://localhost:5000/redoc`
   - Clean, three-panel documentation
   - Better for reading API specifications

### 🔑 Getting a Microsoft Token

To get a Microsoft token for testing, you can:

1. Use Azure CLI:
   ```bash
   az login
   az account get-access-token --resource YOUR_CLIENT_ID
   ```

2. Or use the Microsoft Graph Explorer or Azure Portal to generate a token.

## ✨ Features

- ✅ **Fast Performance** - Built on FastAPI/Starlette for high performance
- ✅ **Automatic Documentation** - Interactive Swagger UI and ReDoc
- ✅ **Type Safety** - Pydantic models for request/response validation
- ✅ **Microsoft Azure AD token validation**
- ✅ **JWT token verification** with Microsoft's public keys
- ✅ **Protected endpoints** return 403/401 without valid token
- ✅ **User information extraction** from valid tokens
- ✅ **Environment-based configuration**
- ✅ **Clean dependency injection** for token validation
- ✅ **Comprehensive error handling**

## ⚡ FastAPI Benefits

- **Better Performance** - 2-3x faster than Flask
- **Automatic API Documentation** - No need to write docs manually
- **Type Hints** - Built-in validation and better IDE support
- **Modern Python** - Async/await support
- **Industry Standard** - OpenAPI/JSON Schema compliance

## 🔒 Security

The application validates Microsoft tokens by:
1. Checking the Authorization header format (Bearer token)
2. Fetching Microsoft's public keys (JWKS)
3. Verifying the JWT signature
4. Validating the issuer and audience claims
5. Extracting user information from validated tokens

## 🛠️ Development

### Using uv for Package Management

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management:

**Installing Dependencies:**
```bash
uv sync  # Install all dependencies from uv.lock
```

**Adding New Packages:**
```bash
uv add package_name              # Add a regular dependency
uv add --dev package_name        # Add a development dependency
uv add "package_name>=1.0.0"     # Add with version constraint
```

**Upgrading Dependencies:**
```bash
uv sync --upgrade               # Upgrade all dependencies
uv add package_name --upgrade   # Upgrade specific package
```

**Running Commands:**
```bash
uv run python main.py          # Run Python with project environment
uv run pytest                  # Run tests with project environment
```

**Other Useful Commands:**
```bash
uv pip list                    # List installed packages
uv pip show package_name       # Show package information
uv lock                        # Update the lock file
```

### 🧪 Testing

Run tests:
```bash
uv run python test_api.py
```

The test script will verify all endpoints and documentation routes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.