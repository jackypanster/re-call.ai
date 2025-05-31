#!/usr/bin/env python3
"""
全面测试mem0 API功能
测试范围：添加记忆、搜索记忆、获取记忆、更新记忆、删除记忆
"""
import time
from mem0 import MemoryClient

# 配置API密钥
API_KEY = "m0-jy0qogy2cP9iWJYNlDAfOp3ANexxorj8xAmI9A1i"

def test_1_basic_connection():
    """测试1：基础连接和客户端初始化"""
    print("🔌 测试1：基础连接...")
    
    try:
        client = MemoryClient(api_key=API_KEY)
        print("✅ mem0客户端初始化成功!")
        return client
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return None

def test_2_add_memories(client):
    """测试2：添加多种类型的记忆"""
    print("\n📝 测试2：添加记忆...")
    
    memories_to_add = [
        {
            "content": "我正在开发re-call.ai项目，这是一个基于AI的个人记忆管理系统。",
            "user_id": "user_001",
            "metadata": {"category": "project", "language": "zh"}
        },
        {
            "content": "Today I learned about FastAPI dependency injection and middleware configuration.",
            "user_id": "user_001", 
            "metadata": {"category": "learning", "language": "en"}
        },
        {
            "content": "Meeting with team about API integration strategy. Decided to use mem0 as primary memory service.",
            "user_id": "user_001",
            "metadata": {"category": "meeting", "priority": "high"}
        }
    ]
    
    added_memories = []
    
    for i, memory_data in enumerate(memories_to_add, 1):
        try:
            result = client.add(
                messages=[{"role": "user", "content": memory_data["content"]}],
                user_id=memory_data["user_id"],
                metadata=memory_data.get("metadata", {})
            )
            
            print(f"✅ 记忆{i}添加成功!")
            print(f"   内容: {memory_data['content'][:50]}...")
            print(f"   结果: {result}")
            added_memories.append(result)
            
        except Exception as e:
            print(f"❌ 记忆{i}添加失败: {e}")
    
    return added_memories

def test_3_search_memories(client):
    """测试3：搜索记忆功能"""
    print("\n🔍 测试3：搜索记忆...")
    
    search_queries = [
        "re-call.ai项目",
        "FastAPI",
        "meeting team",
        "API integration",
        "dependency injection"
    ]
    
    for query in search_queries:
        try:
            results = client.search(
                query=query,
                user_id="user_001",
                limit=5
            )
            
            print(f"✅ 搜索'{query}'成功!")
            print(f"   找到 {len(results)} 条结果")
            
            for i, result in enumerate(results[:2], 1):  # 只显示前2个结果
                print(f"   {i}. {result}")
                
        except Exception as e:
            print(f"❌ 搜索'{query}'失败: {e}")

def test_4_get_all_memories(client):
    """测试4：获取所有记忆"""
    print("\n📋 测试4：获取所有记忆...")
    
    try:
        all_memories = client.get_all(user_id="user_001")
        
        print(f"✅ 获取所有记忆成功!")
        print(f"   总共 {len(all_memories)} 条记忆")
        
        for i, memory in enumerate(all_memories[:3], 1):  # 显示前3条
            print(f"   {i}. ID: {memory.get('id', 'N/A')}")
            print(f"      内容: {str(memory.get('memory', 'N/A'))[:60]}...")
            
        return all_memories
        
    except Exception as e:
        print(f"❌ 获取所有记忆失败: {e}")
        return []

def test_5_update_memory(client, memories):
    """测试5：更新记忆"""
    print("\n✏️ 测试5：更新记忆...")
    
    if not memories:
        print("⚠️ 没有可更新的记忆")
        return
    
    try:
        # 尝试更新第一条记忆
        memory_to_update = memories[0]
        memory_id = memory_to_update.get('id')
        
        if memory_id:
            result = client.update(
                memory_id=memory_id,
                data="Updated: re-call.ai项目进展顺利，已完成mem0 API集成测试。"
            )
            
            print(f"✅ 记忆更新成功!")
            print(f"   记忆ID: {memory_id}")
            print(f"   更新结果: {result}")
        else:
            print("⚠️ 无法找到记忆ID")
            
    except Exception as e:
        print(f"❌ 更新记忆失败: {e}")

def test_6_memory_history(client):
    """测试6：获取记忆历史"""
    print("\n📚 测试6：获取记忆历史...")
    
    try:
        history = client.history(user_id="user_001")
        
        print(f"✅ 获取记忆历史成功!")
        print(f"   历史记录数: {len(history)}")
        
        for i, record in enumerate(history[:3], 1):  # 显示前3条历史
            print(f"   {i}. {record}")
            
    except Exception as e:
        print(f"❌ 获取记忆历史失败: {e}")

def test_7_delete_memory(client, memories):
    """测试7：删除记忆（可选）"""
    print("\n🗑️ 测试7：删除记忆...")
    
    if not memories or len(memories) < 2:
        print("⚠️ 没有足够的记忆可删除")
        return
    
    try:
        # 删除最后一条记忆
        memory_to_delete = memories[-1]
        memory_id = memory_to_delete.get('id')
        
        if memory_id:
            result = client.delete(memory_id=memory_id)
            
            print(f"✅ 记忆删除成功!")
            print(f"   删除的记忆ID: {memory_id}")
            print(f"   删除结果: {result}")
        else:
            print("⚠️ 无法找到要删除的记忆ID")
            
    except Exception as e:
        print(f"❌ 删除记忆失败: {e}")

def test_8_advanced_search(client):
    """测试8：高级搜索功能"""
    print("\n🎯 测试8：高级搜索...")
    
    try:
        # 测试带过滤器的搜索
        results = client.search(
            query="project development",
            user_id="user_001",
            limit=10,
            filters={"category": "project"}
        )
        
        print(f"✅ 高级搜索成功!")
        print(f"   过滤结果数: {len(results)}")
        
    except Exception as e:
        print(f"❌ 高级搜索失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始全面测试mem0 API...")
    print(f"   API密钥: {API_KEY[:20]}...")
    
    # 测试1：基础连接
    client = test_1_basic_connection()
    if not client:
        print("\n❌ 无法建立连接，终止测试")
        return
    
    # 测试2：添加记忆
    added_memories = test_2_add_memories(client)
    
    # 等待处理
    print("\n⏳ 等待3秒让记忆处理完成...")
    time.sleep(3)
    
    # 测试3：搜索记忆
    test_3_search_memories(client)
    
    # 测试4：获取所有记忆
    all_memories = test_4_get_all_memories(client)
    
    # 测试5：更新记忆
    test_5_update_memory(client, all_memories)
    
    # 测试6：记忆历史
    test_6_memory_history(client)
    
    # 测试7：删除记忆（谨慎）
    # test_7_delete_memory(client, all_memories)
    
    # 测试8：高级搜索
    test_8_advanced_search(client)
    
    print("\n🎉 mem0 API全面测试完成!")
    print("📊 测试总结:")
    print("   ✅ 如果大部分测试通过，mem0可以作为supermemory的优秀替代")
    print("   ✅ 特别关注搜索功能是否正常工作")

if __name__ == "__main__":
    main() 