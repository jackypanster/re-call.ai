# re-call-backend

A FastAPI-based backend for the re-call.ai project, powered by mem0 AI memory platform.

## Directory Structure

```
app/
  main.py           # FastAPI entry point
  config.py         # Configuration
  api/              # API routes
  services/         # Service layer
  models/           # Data models
  utils/            # Utility functions

tests/              # Unit and integration tests

.env.example        # Example environment variables
Dockerfile          # Docker configuration
docker-compose.yml  # Docker Compose configuration
requirements.txt    # Python dependencies
README.md           # Project overview
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- uv package manager

### Installation
```bash
# Install dependencies
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your mem0 API key

# Run the application
uvicorn app.main:app --reload
```

### Environment Variables
```bash
MEM0_API_KEY=your-mem0-api-key
JWT_SECRET_KEY=your-secret-key
```

## 📚 API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🧪 Testing

```bash
pytest tests/
``` 