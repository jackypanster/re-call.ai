"""
Task 2.1 验证测试: mem0客户端集成
验证mem0 Platform API集成是否正确完成
"""
import asyncio
import logging
from app.services.memory_service import MemoryService

async def test_mem0_integration():
    """验证Task 2.1: mem0客户端集成"""
    print("🔄 开始验证Task 2.1: mem0客户端集成...")
    
    try:
        # 1. 测试MemoryService初始化
        print("1️⃣ 测试MemoryService初始化...")
        service = MemoryService()
        print(f"✅ MemoryService初始化成功")
        print(f"   客户端类型: {type(service.client).__name__}")
        
        # 2. 测试添加记忆功能
        print("\n2️⃣ 测试添加记忆功能...")
        test_user = "test_user_task2_1"
        test_content = "这是Task 2.1的测试记忆内容"
        test_metadata = {"source": "task2_1_test", "category": "验证"}
        
        result = await service.add_memory(
            content=test_content,
            user_id=test_user,
            metadata=test_metadata
        )
        print(f"✅ 添加记忆成功: {result}")
        
        # 3. 测试搜索记忆功能
        print("\n3️⃣ 测试搜索记忆功能...")
        search_results = await service.search_memories(
            query="Task 2.1",
            user_id=test_user,
            limit=5
        )
        print(f"✅ 搜索记忆成功: 找到 {len(search_results)} 条结果")
        if search_results:
            print(f"   第一条结果: {search_results[0]}")
        
        # 4. 测试获取所有记忆功能
        print("\n4️⃣ 测试获取所有记忆功能...")
        all_memories = await service.get_all_memories(user_id=test_user)
        print(f"✅ 获取所有记忆成功: 共 {len(all_memories)} 条记忆")
        
        # 5. 测试错误处理
        print("\n5️⃣ 测试错误处理...")
        try:
            # 使用无效参数测试错误处理
            await service.add_memory("", "", {})
        except Exception as e:
            print(f"✅ 错误处理正常: {e}")
        
        print("\n🎉 Task 2.1验证完成!")
        print("✅ mem0客户端集成功能正常")
        return True
        
    except Exception as e:
        print(f"❌ Task 2.1验证失败: {e}")
        logging.error(f"Task 2.1验证错误: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_mem0_integration()) 