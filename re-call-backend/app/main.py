from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.exceptions import AppException
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, records, search

app = FastAPI(
    title="re-call.ai API",
    description="Backend service for the re-call.ai AI memory management system.",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(records.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "re-call.ai API is running."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "re-call.ai API"}

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logging.error(f"AppException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.exception(f"Unhandled Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
