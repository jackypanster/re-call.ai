"""
自定义异常类型定义
覆盖re-call.ai应用的主要错误场景
"""
from fastapi import HTTPException, status
from typing import Optional, Dict, Any

class AppException(HTTPException):
    """应用基础异常类"""
    def __init__(self, status_code: int = 400, detail: str = "Application error", 
                 error_code: str = "APP_ERROR", context: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.context = context or {}

class ValidationException(AppException):
    """数据验证异常"""
    def __init__(self, detail: str = "Validation failed", field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=detail,
            error_code="VALIDATION_ERROR",
            context={"field": field} if field else {}
        )

class NotFoundException(AppException):
    """资源未找到异常"""
    def __init__(self, detail: str = "Resource not found", resource_type: str = "resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail,
            error_code="RESOURCE_NOT_FOUND",
            context={"resource_type": resource_type}
        )

class UnauthorizedException(AppException):
    """认证失败异常"""
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=detail,
            error_code="AUTHENTICATION_REQUIRED"
        )

class ForbiddenException(AppException):
    """权限不足异常"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=detail,
            error_code="INSUFFICIENT_PERMISSIONS"
        )

class ConflictException(AppException):
    """资源冲突异常"""
    def __init__(self, detail: str = "Resource conflict", resource_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=detail,
            error_code="RESOURCE_CONFLICT",
            context={"resource_id": resource_id} if resource_id else {}
        )

class ExternalServiceException(AppException):
    """外部服务异常"""
    def __init__(self, detail: str = "External service error", service_name: str = "unknown"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=detail,
            error_code="EXTERNAL_SERVICE_ERROR",
            context={"service_name": service_name}
        )

class RateLimitException(AppException):
    """频率限制异常"""
    def __init__(self, detail: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED",
            context={"retry_after": retry_after} if retry_after else {}
        )

class MemoryServiceException(ExternalServiceException):
    """记忆服务专用异常"""
    def __init__(self, detail: str = "Memory service error", operation: str = "unknown"):
        super().__init__(
            detail=detail, 
            service_name="mem0"
        )
        self.context["operation"] = operation

class AuthServiceException(ExternalServiceException):
    """认证服务专用异常"""
    def __init__(self, detail: str = "Authentication service error"):
        super().__init__(
            detail=detail, 
            service_name="supabase_auth"
        )
