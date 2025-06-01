from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.models.memory import (
    MemoryCreateRequest, MemoryUpdateRequest, MemoryResponse,
    SearchRequest, SearchResponse, MemoryListResponse, StandardResponse
)
from app.services.memory_service import get_memory_service
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/memories", response_model=StandardResponse, summary="添加新记忆")
async def create_memory(
    request: MemoryCreateRequest,
    current_user: str = Depends(get_current_user),
    memory_service = Depends(get_memory_service)
):
    """
    添加新的文本记忆
    
    - **content**: 记忆内容（必填，1-10000字符）
    - **metadata**: 可选的元数据，如分类、标签等
    """
    try:
        result = await memory_service.add_memory(
            content=request.content,
            user_id=current_user,
            metadata=request.metadata
        )
        
        return StandardResponse(
            success=True,
            message="记忆添加成功",
            data={"memory_id": result.get("id", "unknown")}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加记忆失败: {str(e)}")

@router.get("/memories/search", response_model=SearchResponse, summary="搜索记忆")
async def search_memories(
    q: str = Query(..., description="搜索查询", min_length=1),
    limit: int = Query(default=10, description="结果数量限制", ge=1, le=100),
    current_user: str = Depends(get_current_user),
    memory_service = Depends(get_memory_service)
):
    """
    基于语义搜索用户记忆
    
    - **q**: 搜索查询关键词
    - **limit**: 返回结果数量（1-100）
    """
    try:
        results = await memory_service.search_memories(
            query=q,
            user_id=current_user,
            limit=limit
        )
        
        # 转换结果格式
        memory_responses = []
        for item in results:
            memory_responses.append(MemoryResponse(
                id=item.get("id", ""),
                content=item.get("memory", ""),
                user_id=current_user,
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at"),
                updated_at=item.get("updated_at")
            ))
        
        return SearchResponse(
            results=memory_responses,
            total=len(memory_responses),
            query=q
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@router.get("/memories", response_model=MemoryListResponse, summary="获取用户所有记忆")
async def get_user_memories(
    limit: int = Query(default=50, description="结果数量限制", ge=1, le=200),
    offset: int = Query(default=0, description="偏移量", ge=0),
    current_user: str = Depends(get_current_user),
    memory_service = Depends(get_memory_service)
):
    """
    获取当前用户的所有记忆列表
    
    - **limit**: 返回记忆数量（1-200）
    - **offset**: 分页偏移量
    """
    try:
        all_memories = await memory_service.get_all_memories(user_id=current_user)
        
        # 简单分页处理
        paginated_memories = all_memories[offset:offset + limit]
        
        # 转换格式
        memory_responses = []
        for item in paginated_memories:
            memory_responses.append(MemoryResponse(
                id=item.get("id", ""),
                content=item.get("memory", ""),
                user_id=current_user,
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at"),
                updated_at=item.get("updated_at")
            ))
        
        return MemoryListResponse(
            memories=memory_responses,
            total=len(all_memories),
            user_id=current_user
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取记忆列表失败: {str(e)}")

@router.put("/memories/{memory_id}", response_model=StandardResponse, summary="更新记忆")
async def update_memory(
    memory_id: str,
    request: MemoryUpdateRequest,
    current_user: str = Depends(get_current_user),
    memory_service = Depends(get_memory_service)
):
    """
    更新指定记忆的内容
    
    - **memory_id**: 记忆ID
    - **content**: 新的记忆内容
    """
    try:
        result = await memory_service.update_memory(
            memory_id=memory_id,
            data=request.content
        )
        
        return StandardResponse(
            success=True,
            message="记忆更新成功",
            data={"memory_id": memory_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新记忆失败: {str(e)}")

@router.delete("/memories/{memory_id}", response_model=StandardResponse, summary="删除记忆")
async def delete_memory(
    memory_id: str,
    current_user: str = Depends(get_current_user),
    memory_service = Depends(get_memory_service)
):
    """
    删除指定的记忆
    
    - **memory_id**: 要删除的记忆ID
    """
    try:
        result = await memory_service.delete_memory(memory_id=memory_id)
        
        return StandardResponse(
            success=True,
            message="记忆删除成功",
            data={"memory_id": memory_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除记忆失败: {str(e)}") 