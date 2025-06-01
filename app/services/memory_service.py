import logging
from app.config import settings

try:
    from mem0 import MemoryClient
except ImportError:
    try:
        from mem0ai import MemoryClient
    except ImportError:
        # Demo模式的Mock客户端
        class MemoryClient:
            def __init__(self, api_key):
                self.api_key = api_key
                self._memories = {}
                logging.warning("Using demo MemoryClient - mem0 not available")
            
            def add(self, messages, user_id, metadata=None):
                memory_id = f"demo-memory-{len(self._memories)}"
                content = messages[0]["content"] if messages else ""
                self._memories[memory_id] = {
                    "id": memory_id,
                    "memory": content,
                    "user_id": user_id,
                    "metadata": metadata or {},
                    "created_at": "2024-12-01T12:00:00Z"
                }
                return {"id": memory_id}
            
            def search(self, query, user_id, limit=10):
                results = []
                for mem_id, mem_data in self._memories.items():
                    if (mem_data["user_id"] == user_id and 
                        query.lower() in mem_data["memory"].lower()):
                        results.append(mem_data)
                return results[:limit]
            
            def get_all(self, user_id):
                return [mem for mem in self._memories.values() 
                       if mem["user_id"] == user_id]
            
            def update(self, memory_id, data):
                if memory_id in self._memories:
                    self._memories[memory_id]["memory"] = data
                    return {"id": memory_id}
                return {"error": "Memory not found"}
            
            def delete(self, memory_id):
                if memory_id in self._memories:
                    del self._memories[memory_id]
                    return {"deleted": True}
                return {"error": "Memory not found"}

class MemoryService:
    def __init__(self):
        try:
            self.client = MemoryClient(api_key=settings.mem0_api_key)
        except Exception as e:
            logging.warning(f"Failed to initialize mem0 client: {e}")
            self.client = MemoryClient(api_key="demo")

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
