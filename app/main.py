from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api import auth, memories

app = FastAPI(
    title="re-call.ai API",
    description="Backend service for the re-call.ai AI memory management system.",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["认证"])
app.include_router(memories.router, prefix="/api", tags=["记忆管理"])

@app.get("/")
async def root():
    return {"message": "re-call.ai API is running."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "re-call.ai API"}
