from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.exceptions import AppException
import logging

app = FastAPI(
    title="SuperMemory API",
    description="Backend service for the re-call (SuperMemory) project.",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "SuperMemory API is running."}

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
