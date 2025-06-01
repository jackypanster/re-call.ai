"""
FastAPI全局异常处理器
提供标准化的错误响应格式
"""
import traceback
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.exceptions import AppException
from app.utils.logger import get_logger, log_error
from app.models.memory import ErrorResponse

logger = get_logger("exception_handler")

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """处理自定义应用异常"""
    error_response = ErrorResponse(
        success=False,
        error=exc.error_code,
        message=exc.detail,
        details=exc.context
    )
    
    # 记录错误日志
    log_error(logger, exc, {
        "request_url": str(request.url),
        "request_method": request.method,
        "error_code": exc.error_code,
        "status_code": exc.status_code
    })
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """处理FastAPI HTTP异常"""
    error_response = ErrorResponse(
        success=False,
        error="HTTP_ERROR",
        message=exc.detail,
        details={"status_code": exc.status_code}
    )
    
    # 记录错误日志（4xx错误用WARNING，5xx错误用ERROR）
    if exc.status_code >= 500:
        log_error(logger, exc, {
            "request_url": str(request.url),
            "request_method": request.method,
            "status_code": exc.status_code
        })
    else:
        logger.warning(f"HTTP {exc.status_code}: {exc.detail}", extra={
            "request_url": str(request.url),
            "request_method": request.method,
            "status_code": exc.status_code
        })
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """处理请求验证异常"""
    # 提取验证错误详情
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error.get("loc", []))
        error_details.append({
            "field": field,
            "message": error.get("msg", ""),
            "type": error.get("type", "")
        })
    
    error_response = ErrorResponse(
        success=False,
        error="VALIDATION_ERROR",
        message="Request validation failed",
        details={"errors": error_details}
    )
    
    logger.warning(f"Validation error: {len(error_details)} field(s) failed validation", extra={
        "request_url": str(request.url),
        "request_method": request.method,
        "validation_errors": error_details
    })
    
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )

async def pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """处理Pydantic验证异常"""
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error.get("loc", []))
        error_details.append({
            "field": field,
            "message": error.get("msg", ""),
            "type": error.get("type", "")
        })
    
    error_response = ErrorResponse(
        success=False,
        error="VALIDATION_ERROR",
        message="Data validation failed",
        details={"errors": error_details}
    )
    
    logger.warning(f"Pydantic validation error: {len(error_details)} field(s) failed", extra={
        "request_url": str(request.url),
        "request_method": request.method,
        "validation_errors": error_details
    })
    
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """处理未捕获的通用异常"""
    error_response = ErrorResponse(
        success=False,
        error="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred",
        details={"type": type(exc).__name__}
    )
    
    # 记录详细的错误信息
    log_error(logger, exc, {
        "request_url": str(request.url),
        "request_method": request.method,
        "traceback": traceback.format_exc()
    })
    
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )

def setup_exception_handlers(app):
    """设置异常处理器到FastAPI应用"""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler) 