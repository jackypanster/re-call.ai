import httpx
import logging
from app.config import settings

class MemoryService:
    def __init__(self):
        self.api_key = settings.supermemory_api_key
        self.base_url = "https://api.supermemory.ai/v3/memories"

    async def add_memory(self, content: str, metadata: dict = None) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "content": content,
            "metadata": metadata or {}
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(self.base_url, json=payload, headers=headers, timeout=30)
                await resp.raise_for_status()
                return await resp.json()
        except Exception as e:
            logging.error(f"Supermemory add_memory error: {e}")
            raise

    async def search_memories(self, query: str, limit: int = 10) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        params = {
            "q": query,
            "limit": limit
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.base_url, params=params, headers=headers, timeout=30)
                await resp.raise_for_status()
                return await resp.json()
        except Exception as e:
            logging.error(f"Supermemory search_memories error: {e}")
            raise

# 单例实例
memory_service = MemoryService()

def get_memory_service():
    return memory_service
