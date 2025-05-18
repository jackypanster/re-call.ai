import pytest
from unittest.mock import patch, MagicMock
from app.services.llm_service import LLMService

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_summarize(mock_async_client):
    class MockResponse:
        async def json(self):
            return {"choices": [{"message": {"content": "摘要结果"}}]}
        async def raise_for_status(self):
            return None
    mock_instance = MagicMock()
    mock_instance.__aenter__.return_value.post.return_value = MockResponse()
    mock_async_client.return_value = mock_instance
    service = LLMService()
    result = await service.summarize("测试内容")
    assert result == "摘要结果"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_extract_tags(mock_async_client):
    class MockResponse:
        async def json(self):
            return {"choices": [{"message": {"content": "标签1, 标签2, 标签3"}}]}
        async def raise_for_status(self):
            return None
    mock_instance = MagicMock()
    mock_instance.__aenter__.return_value.post.return_value = MockResponse()
    mock_async_client.return_value = mock_instance
    service = LLMService()
    result = await service.extract_tags("测试内容")
    assert result == ["标签1", "标签2", "标签3"] 