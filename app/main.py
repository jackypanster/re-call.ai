from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api import auth, memories

# Import exception handlers and logging
from app.utils.exception_handlers import setup_exception_handlers
from app.utils.logger import get_logger

# Initialize logger
logger = get_logger("main")

app = FastAPI(
    title="re-call.ai API",
    description="Backend service for the re-call.ai AI memory management system.",
    version="1.0.0"
)

# Setup exception handlers
setup_exception_handlers(app)

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
    logger.info("Root endpoint accessed")
    return {"message": "re-call.ai API is running."}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "re-call.ai API"}

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("🚀 re-call.ai API starting up...")
    logger.info("📝 Exception handlers configured")
    logger.info("🔒 CORS middleware enabled")
    logger.info("✅ Application ready to serve requests")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("🛑 re-call.ai API shutting down...")
    logger.info("✅ Shutdown complete")
