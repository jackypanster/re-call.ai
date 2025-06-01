from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class MemoryCreateRequest(BaseModel):
    """创建记忆请求模型"""
    content: str = Field(..., description="记忆内容", min_length=1, max_length=10000)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="附加元数据")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "今天学习了FastAPI的依赖注入系统，非常强大",
                "metadata": {
                    "category": "学习",
                    "tags": ["FastAPI", "编程"],
                    "source": "课程笔记"
                }
            }
        }
    }

class MemoryUpdateRequest(BaseModel):
    """更新记忆请求模型"""
    content: str = Field(..., description="更新后的记忆内容", min_length=1, max_length=10000)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "今天深入学习了FastAPI的依赖注入系统，包括Depends装饰器的高级用法"
            }
        }
    }

class MemoryResponse(BaseModel):
    """记忆响应模型"""
    id: str = Field(..., description="记忆ID")
    content: str = Field(..., description="记忆内容")
    user_id: str = Field(..., description="用户ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    created_at: Optional[str] = Field(None, description="创建时间")
    updated_at: Optional[str] = Field(None, description="更新时间")

class SearchRequest(BaseModel):
    """搜索记忆请求模型"""
    query: str = Field(..., description="搜索查询", min_length=1, max_length=1000)
    limit: Optional[int] = Field(default=10, description="返回结果数量限制", ge=1, le=100)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "FastAPI学习",
                "limit": 10
            }
        }
    }

class SearchResponse(BaseModel):
    """搜索结果响应模型"""
    results: List[MemoryResponse] = Field(..., description="搜索结果列表")
    total: int = Field(..., description="总结果数量")
    query: str = Field(..., description="搜索查询")

class MemoryListResponse(BaseModel):
    """记忆列表响应模型"""
    memories: List[MemoryResponse] = Field(..., description="记忆列表")
    total: int = Field(..., description="总记忆数量")
    user_id: str = Field(..., description="用户ID")

class StandardResponse(BaseModel):
    """标准API响应模型"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据") 