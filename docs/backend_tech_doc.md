# re-call Backend Technical Documentation

## 📚 Overview

This document outlines the technical implementation details for the re-call.ai backend service, an AI-powered personal memory management system designed to capture, organize, and retrieve textual information using advanced AI services.

**Project Name:** re-call.ai  
**Service Type:** REST API  
**Primary Framework:** FastAPI  
**Core Memory Service:** mem0 Platform  
**Deployment Strategy:** Cloud-native SaaS approach  

## 🏗️ System Architecture

### Logical Architecture

```
┌─────────────────────────────┐
│         Client Layer        │ ◄──── Web/Mobile UI, API Client
└─────────────────────────────┘
                │
                ▼
┌─────────────────────────────┐
│     FastAPI Application     │ ◄──── REST API, Authentication, Routing
└─────────────────────────────┘
                │
      ┌─────────┼─────────┬─────────┐
      ▼                   ▼         ▼
┌────────────┐    ┌─────────────┐  ┌─────────────┐
│ Voice/LLM  │    │Memory Service│  │Database Svc │
│ Services   │    │   (mem0)     │  │             │
└────────────┘    └─────────────┘  └─────────────┘
      │                 │               │
      ▼                 ▼               ▼
┌────────────┐    ┌─────────────┐  ┌─────────────┐
│OpenAI      │    │mem0 Platform│  │Supabase/    │
│Whisper API │    │AI Memory    │  │Railway DB   │
└────────────┘    └─────────────┘  └─────────────┘
```

### Directory Structure

```
re-call-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration (API keys, etc.)
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── memories.py         # Memory management endpoints
│   │   └── search.py           # Search endpoints
│   ├── services/               # Service layer
│   │   ├── __init__.py
│   │   ├── voice_service.py    # Voice-to-text service (Whisper)
│   │   ├── memory_service.py   # mem0 platform integration
│   │   └── database.py         # Database integration
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── memory.py           # Memory model
│   │   └── user.py             # User model
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── logger.py           # Logging configuration
│       └── exceptions.py       # Custom exceptions
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   ├── test_api/               # API tests
│   └── test_services/          # Service tests
├── .env.example                # Example environment variables
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview
```

## 🔧 Technical Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| API Framework | FastAPI | High-performance Python API framework |
| Runtime | Uvicorn | ASGI server for FastAPI |
| Deployment | Railway/Vercel | Cloud platforms for hosting |
| AI Memory | mem0 Platform | Advanced AI memory management service |
| Voice Processing | OpenAI Whisper API | Speech-to-text conversion |
| Authentication | JWT | Token-based authentication |
| Testing | Pytest | Unit and integration testing |
| CI/CD | GitHub Actions | Automated testing and deployment |

## 📋 Core Data Models

### Record Model

```python
class Record:
    id: str                # Unique identifier
    content: str           # Original text content
    summary: str           # One-sentence summary (LLM-generated)
    keywords: List[str]    # 3-5 keywords (LLM-generated)
    tags: List[str]        # Classification tags (LLM-generated)
    memory_id: str         # Reference to memory in mem0
    user_id: str           # Owner of the record
    created_at: datetime   # Creation timestamp
    updated_at: datetime   # Last update timestamp
```

### User Model

```python
class User:
    id: str                # Unique identifier
    email: str             # User email
    created_at: datetime   # Account creation timestamp
    settings: Dict         # User preferences
```

## 🔌 External Integrations

### 1. LLM Service (OpenRouter/OpenAI)

Used for:
- Text summarization (1-sentence summary)
- Keyword extraction (3-5 keywords)
- Automatic classification (generating tags)

Integration method:
- REST API calls via HTTP client
- Authentication via API key in request headers

### 2. mem0 Platform

Used for:
- AI-powered memory storage
- Intelligent semantic search
- Automatic memory organization

Integration method:
- mem0 Python SDK
- Sample integration code:

```python
from mem0 import Memory

# Initialize mem0 client
memory = Memory()

# Adding a memory
async def add_memory(content: str, user_id: str, metadata: dict = None):
    result = memory.add(
        messages=[{"role": "user", "content": content}],
        user_id=user_id,
        metadata=metadata or {}
    )
    return result

# Searching memories
async def search_memories(query: str, user_id: str, limit: int = 10):
    results = memory.search(
        query=query,
        user_id=user_id,
        limit=limit
    )
    return results
```

## 🚪 API Endpoints

### Authentication

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/auth/register` | POST | Register new user | `{email, password}` | `{user_id, token}` |
| `/api/auth/login` | POST | Login existing user | `{email, password}` | `{user_id, token}` |
| `/api/auth/logout` | POST | Logout user | None | `{success}` |

### Records

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/records` | GET | Get user records | Query params: `limit, offset, tag` | List of records |
| `/api/records` | POST | Create new record | `{content}` | Created record |
| `/api/records/{id}` | GET | Get specific record | None | Record details |
| `/api/records/{id}` | PUT | Update record | `{content, tags}` | Updated record |
| `/api/records/{id}` | DELETE | Delete record | None | `{success}` |

### Search

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/search` | GET | Search records | Query param: `q` | List of matching records |
| `/api/search/tags` | GET | Get all user tags | None | List of tags |

## ⚙️ Environment Variables

The following environment variables are required for the application:

```
# FastAPI Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
SECRET_KEY=your-secret-key

# LLM Service
OPENROUTER_API_KEY=your-openrouter-api-key
PREFERRED_MODEL=claude-3-opus-20240229

# mem0 Platform
MEM0_API_KEY=your-mem0-api-key

# Logging
LOG_LEVEL=INFO
```

## 🚀 Deployment

### Development Environment

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example`
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Production Deployment (Railway)

1. Connect your GitHub repository to Railway
2. Configure environment variables in Railway dashboard
3. Railway will automatically build and deploy on push to main branch

## 🔄 Data Flow

### Memory Creation Process

1. Client sends text content to `/api/memories` endpoint
2. Backend processes content and extracts metadata
3. Backend sends content to mem0 for intelligent storage
4. mem0 automatically handles vectorization and organization
5. Backend receives memory ID from mem0
6. Client receives confirmation with memory details

### Search Process

1. Client sends query to `/api/memories/search` endpoint
2. Backend forwards query to mem0 for semantic search
3. mem0 performs intelligent search across user's memories
4. Backend receives ranked results from mem0
5. Client receives list of memories sorted by relevance

## 🧪 Testing

Run tests using pytest:

```bash
pytest
```

### Test Categories:

- **Unit Tests**: Testing individual functions and methods
- **Integration Tests**: Testing service interactions
- **API Tests**: Testing HTTP endpoints

## 🛣️ Roadmap

### Phase 1 (MVP)
- Basic record creation and storage
- LLM-based summarization and tagging
- Simple semantic search

### Phase 2
- User authentication and multi-user support
- Tag-based filtering
- UI enhancements

### Phase 3
- Advanced search features
- Model switching (Claude/GPT)
- API improvements

## 📝 Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [mem0 Platform Documentation](https://docs.mem0.ai/)


---

Last updated: May 18, 2025
