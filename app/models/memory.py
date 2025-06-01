from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum

class MemoryCategory(str, Enum):
    """记忆分类枚举"""
    MISC = "misc"
    PERSONAL = "personal"
    WORK = "work"
    STUDY = "study"
    PROJECT = "project"

class MemoryCreateRequest(BaseModel):
    """创建记忆请求模型"""
    content: str = Field(
        ..., 
        description="记忆内容", 
        min_length=1, 
        max_length=10000,
        example="今天学习了FastAPI的依赖注入系统，非常强大"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="附加元数据",
        example={
            "category": "学习",
            "tags": ["FastAPI", "编程"],
            "source": "课程笔记",
            "importance": "high"
        }
    )
    
    @validator('content')
    def validate_content(cls, v):
        """验证记忆内容"""
        if not v or not v.strip():
            raise ValueError('记忆内容不能为空')
        if len(v.strip()) < 1:
            raise ValueError('记忆内容至少需要1个字符')
        return v.strip()
    
    @validator('metadata')
    def validate_metadata(cls, v):
        """验证元数据格式"""
        if v is None:
            return {}
        if not isinstance(v, dict):
            raise ValueError('元数据必须是字典格式')
        # 限制元数据键值的长度
        for key, value in v.items():
            if len(str(key)) > 100:
                raise ValueError(f'元数据键 "{key}" 长度不能超过100字符')
            if isinstance(value, str) and len(value) > 1000:
                raise ValueError(f'元数据值长度不能超过1000字符')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "今天学习了FastAPI的依赖注入系统，非常强大",
                "metadata": {
                    "category": "学习",
                    "tags": ["FastAPI", "编程"],
                    "source": "课程笔记",
                    "importance": "high"
                }
            }
        }
    }

class MemoryUpdateRequest(BaseModel):
    """更新记忆请求模型"""
    content: str = Field(
        ..., 
        description="更新后的记忆内容", 
        min_length=1, 
        max_length=10000,
        example="今天深入学习了FastAPI的依赖注入系统，包括Depends装饰器的高级用法"
    )
    
    @validator('content')
    def validate_content(cls, v):
        """验证更新内容"""
        if not v or not v.strip():
            raise ValueError('更新内容不能为空')
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "今天深入学习了FastAPI的依赖注入系统，包括Depends装饰器的高级用法"
            }
        }
    }

class MemoryResponse(BaseModel):
    """记忆响应模型 - 映射mem0 Platform API返回格式"""
    id: str = Field(..., description="记忆唯一标识符")
    memory: str = Field(..., description="记忆内容", alias="content")
    user_id: str = Field(..., description="用户ID")
    actor_id: Optional[str] = Field(None, description="执行者ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="记忆元数据")
    categories: List[str] = Field(default_factory=list, description="记忆分类列表")
    created_at: Optional[str] = Field(None, description="创建时间 (ISO格式)")
    updated_at: Optional[str] = Field(None, description="更新时间 (ISO格式)")
    expiration_date: Optional[str] = Field(None, description="过期时间")
    internal_metadata: Optional[Dict[str, Any]] = Field(None, description="内部元数据")
    deleted_at: Optional[str] = Field(None, description="删除时间")
    score: Optional[float] = Field(None, description="相关性评分 (搜索时返回)")

    @validator('memory', pre=True)
    def handle_memory_alias(cls, v, values):
        """处理content字段的别名"""
        # 如果传入的是content字段，转换为memory
        return v

    model_config = {
        "populate_by_name": True,  # 允许使用别名
        "json_schema_extra": {
            "example": {
                "id": "59bcc066-d304-4259-8a26-60da89bf9243",
                "memory": "今天学习了FastAPI的依赖注入系统",
                "user_id": "user123",
                "metadata": {"category": "学习", "tags": ["FastAPI"]},
                "categories": ["misc"],
                "created_at": "2024-12-01T12:00:00Z",
                "updated_at": "2024-12-01T12:00:00Z"
            }
        }
    }

class SearchRequest(BaseModel):
    """搜索记忆请求模型"""
    query: str = Field(
        ..., 
        description="搜索查询字符串", 
        min_length=1, 
        max_length=1000,
        example="FastAPI学习"
    )
    limit: Optional[int] = Field(
        default=10, 
        description="返回结果数量限制", 
        ge=1, 
        le=100,
        example=10
    )
    # 添加更多搜索参数
    categories: Optional[List[str]] = Field(
        default=None,
        description="过滤的记忆分类",
        example=["study", "work"]
    )
    metadata_filter: Optional[Dict[str, Any]] = Field(
        default=None,
        description="元数据过滤条件",
        example={"importance": "high"}
    )
    
    @validator('query')
    def validate_query(cls, v):
        """验证搜索查询"""
        if not v or not v.strip():
            raise ValueError('搜索查询不能为空')
        return v.strip()
    
    @validator('limit')
    def validate_limit(cls, v):
        """验证限制数量"""
        if v is not None and (v < 1 or v > 100):
            raise ValueError('返回结果数量限制必须在1-100之间')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "FastAPI学习",
                "limit": 10,
                "categories": ["study"],
                "metadata_filter": {"importance": "high"}
            }
        }
    }

class SearchResponse(BaseModel):
    """搜索结果响应模型"""
    results: List[MemoryResponse] = Field(..., description="搜索结果列表")
    total: int = Field(..., description="总结果数量")
    query: str = Field(..., description="搜索查询")
    limit: int = Field(..., description="请求的结果数量限制")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "results": [
                    {
                        "id": "59bcc066-d304-4259-8a26-60da89bf9243",
                        "memory": "今天学习了FastAPI的依赖注入系统",
                        "user_id": "user123",
                        "metadata": {"category": "学习"},
                        "categories": ["study"],
                        "created_at": "2024-12-01T12:00:00Z"
                    }
                ],
                "total": 1,
                "query": "FastAPI学习",
                "limit": 10
            }
        }
    }

class MemoryListRequest(BaseModel):
    """记忆列表请求模型"""
    limit: Optional[int] = Field(
        default=50, 
        description="返回结果数量限制", 
        ge=1, 
        le=200,
        example=50
    )
    offset: Optional[int] = Field(
        default=0,
        description="分页偏移量",
        ge=0,
        example=0
    )
    
    @validator('limit')
    def validate_limit(cls, v):
        """验证限制数量"""
        if v is not None and (v < 1 or v > 200):
            raise ValueError('返回结果数量限制必须在1-200之间')
        return v

class MemoryListResponse(BaseModel):
    """记忆列表响应模型"""
    memories: List[MemoryResponse] = Field(..., description="记忆列表")
    total: int = Field(..., description="用户总记忆数量")
    user_id: str = Field(..., description="用户ID")
    limit: int = Field(..., description="请求的结果数量限制")
    offset: int = Field(..., description="分页偏移量")
    has_more: bool = Field(..., description="是否还有更多数据")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "memories": [],
                "total": 100,
                "user_id": "user123",
                "limit": 50,
                "offset": 0,
                "has_more": True
            }
        }
    }

class StandardResponse(BaseModel):
    """标准API响应模型"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "操作成功",
                "data": None
            }
        }
    }

class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = Field(False, description="操作是否成功")
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": False,
                "error": "ValidationError",
                "message": "输入数据验证失败",
                "details": {"field": "content", "issue": "不能为空"}
            }
        }
    } 