import logging
from mem0 import MemoryClient
from app.config import settings

class MemoryService:
    def __init__(self):
        self.client = MemoryClient(api_key=settings.mem0_api_key)

    async def add_memory(self, content: str, user_id: str, metadata: dict = None) -> dict:
        """添加记忆到mem0"""
        try:
            messages = [{"role": "user", "content": content}]
            result = self.client.add(
                messages=messages,
                user_id=user_id,
                metadata=metadata or {}
            )
            logging.info(f"Memory added successfully for user {user_id}")
            return result
        except Exception as e:
            logging.error(f"mem0 add_memory error: {e}")
            raise

    async def search_memories(self, query: str, user_id: str, limit: int = 10) -> list:
        """搜索用户记忆"""
        try:
            results = self.client.search(
                query=query,
                user_id=user_id,
                limit=limit
            )
            logging.info(f"Search completed for user {user_id}, found {len(results)} results")
            return results
        except Exception as e:
            logging.error(f"mem0 search_memories error: {e}")
            raise

    async def get_all_memories(self, user_id: str) -> list:
        """获取用户所有记忆"""
        try:
            memories = self.client.get_all(user_id=user_id)
            logging.info(f"Retrieved {len(memories)} memories for user {user_id}")
            return memories
        except Exception as e:
            logging.error(f"mem0 get_all_memories error: {e}")
            raise

    async def update_memory(self, memory_id: str, data: str) -> dict:
        """更新记忆"""
        try:
            result = self.client.update(memory_id=memory_id, data=data)
            logging.info(f"Memory {memory_id} updated successfully")
            return result
        except Exception as e:
            logging.error(f"mem0 update_memory error: {e}")
            raise

    async def delete_memory(self, memory_id: str) -> dict:
        """删除记忆"""
        try:
            result = self.client.delete(memory_id=memory_id)
            logging.info(f"Memory {memory_id} deleted successfully")
            return result
        except Exception as e:
            logging.error(f"mem0 delete_memory error: {e}")
            raise

# 单例实例
memory_service = MemoryService()

def get_memory_service():
    return memory_service
