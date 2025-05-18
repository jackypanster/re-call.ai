# re-call Backend Technical Documentation

## 📚 Overview

This document outlines the technical implementation details for the re-call (SuperMemory) backend service, a personal second-brain system designed to capture, summarize, classify, and retrieve textual information using AI.

**Project Codename:** re-call  
**Service Type:** REST API  
**Primary Framework:** FastAPI  
**Deployment Strategy:** SaaS-first approach  

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
│ LLM Service│    │Memory Service│  │Database Svc │
│(Summary/Tag)│    │(Supermemory)│  │(Supabase)   │
└────────────┘    └─────────────┘  └─────────────┘
      │                 │               │
      ▼                 ▼               ▼
┌────────────┐    ┌─────────────┐  ┌─────────────┐
│OpenRouter/ │    │Supermemory.ai│  │PostgreSQL   │
│OpenAI      │    │Vector Store  │  │(via Supabase)│
└────────────┘    └─────────────┘  └─────────────┘
```

### Directory Structure

```
supermemory-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration (API keys, etc.)
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── records.py          # Record management endpoints
│   │   └── search.py           # Search endpoints
│   ├── services/               # Service layer
│   │   ├── __init__.py
│   │   ├── llm_service.py      # LLM service for summarization/tagging
│   │   ├── memory_service.py   # Supermemory.ai integration
│   │   └── database.py         # Supabase integration
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── record.py           # Record model
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
| Deployment | Railway/Render | Cloud platforms for hosting |
| LLM Integration | OpenRouter API | Unified API for accessing multiple LLMs |
| Vector Storage | Supermemory.ai | RAG system for vector search |
| Database | Supabase (PostgreSQL) | Storage for user data and metadata |
| Authentication | JWT + Supabase Auth | Token-based authentication |
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
    embedding_id: str      # Reference to vector in Supermemory
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

### 2. Supermemory.ai

Used for:
- Vector storage of text content
- Semantic search capabilities

Integration method:
- REST API calls to Supermemory.ai endpoints
- Sample integration code:

```python
# Adding a memory
async def add_memory(content: str, metadata: dict = None):
    url = "https://api.supermemory.ai/v3/memories"
    headers = {
        "Authorization": f"Bearer {config.SUPERMEMORY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": content,
        "metadata": metadata or {}
    }
    response = await httpx.post(url, json=payload, headers=headers)
    return response.json()

# Searching memories
async def search_memories(query: str, limit: int = 10):
    url = "https://api.supermemory.ai/v3/memories"
    headers = {
        "Authorization": f"Bearer {config.SUPERMEMORY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "limit": limit
    }
    response = await httpx.get(url, json=payload, headers=headers)
    return response.json()
```

### 3. Supabase

Used for:
- User authentication
- Storing record metadata
- Managing relationships between entities

Integration method:
- Supabase Python client
- Connection established at application startup

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

# Supermemory.ai
SUPERMEMORY_API_KEY=your-supermemory-api-key

# Supabase
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

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

### Record Creation Process

1. Client sends text content to `/api/records` endpoint
2. Backend saves raw content to Supabase
3. Backend sends content to LLM service for summarization and tagging
4. Backend updates record with summary and tags
5. Backend sends content to Supermemory.ai for vectorization
6. Backend updates record with vector reference ID
7. Client receives complete record details

### Search Process

1. Client sends query to `/api/search` endpoint
2. Backend forwards query to Supermemory.ai for semantic search
3. Backend retrieves matching vector IDs
4. Backend queries Supabase for full record details using IDs
5. Client receives list of records sorted by relevance

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
- [Supermemory.ai API Documentation](https://docs.supermemory.ai/)
- [Supabase Documentation](https://supabase.io/docs)

---

Last updated: May 18, 2025
