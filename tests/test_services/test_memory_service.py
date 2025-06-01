import pytest
from unittest.mock import patch, MagicMock
from app.services.memory_service import MemoryService

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_add_memory(mock_async_client):
    class MockResponse:
        async def json(self):
            return {"id": "123", "content": "测试内容"}
        async def raise_for_status(self):
            return None
    mock_instance = MagicMock()
    mock_instance.__aenter__.return_value.post.return_value = MockResponse()
    mock_async_client.return_value = mock_instance
    service = MemoryService()
    result = await service.add_memory("测试内容", {"meta": "data"})
    assert result == {"id": "123", "content": "测试内容"}

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_search_memories(mock_async_client):
    class MockResponse:
        async def json(self):
            return {"results": ["记忆1", "记忆2"]}
        async def raise_for_status(self):
            return None
    mock_instance = MagicMock()
    mock_instance.__aenter__.return_value.get.return_value = MockResponse()
    mock_async_client.return_value = mock_instance
    service = MemoryService()
    result = await service.search_memories("测试查询", limit=2)
    assert result == {"results": ["记忆1", "记忆2"]} 