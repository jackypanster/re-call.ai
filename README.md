# supermemory-backend

A FastAPI-based backend for the re-call (SuperMemory) project.

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

## Quick Start

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 复制 .env.example 为 .env 并填写配置
3. 启动开发服务器：
   ```bash
   uvicorn app.main:app --reload
   ``` 