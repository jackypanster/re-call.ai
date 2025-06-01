#!/usr/bin/env python3
"""
测试mem0平台功能 - 按照官方文档的正确方法
"""
import os
from mem0 import MemoryClient

# 配置API密钥
API_KEY = "m0-jy0qogy2cP9iWJYNlDAfOp3ANexxorj8xAmI9A1i"

def test_platform_connection():
    """测试平台连接"""
    print("🔌 测试mem0平台连接...")
    
    try:
        # 设置环境变量
        os.environ["MEM0_API_KEY"] = API_KEY
        
        # 创建客户端
        client = MemoryClient()
        print("✅ mem0平台客户端创建成功!")
        
        return client
    except Exception as e:
        print(f"❌ 平台连接失败: {e}")
        return None

def test_add_memories(client):
    """测试添加记忆"""
    print("\n📝 测试添加记忆...")
    
    test_cases = [
        {
            "messages": [
                {"role": "user", "content": "我正在开发re-call.ai项目，这是一个基于AI的个人记忆管理系统。"},
                {"role": "assistant", "content": "很棒的项目！我会记住你正在开发re-call.ai这个AI记忆管理系统。"}
            ],
            "user_id": "developer_001",
            "metadata": {"category": "project", "language": "zh"}
        },
        {
            "messages": [
                        {"role": "user", "content": "I'm building re-call.ai, an AI-powered personal memory management system using mem0."},
        {"role": "assistant", "content": "That's exciting! I'll remember you're building re-call.ai with mem0 as the core memory service."}
            ],
            "user_id": "developer_001", 
            "metadata": {"category": "evaluation", "language": "en"}
        },
        {
            "messages": [
                {"role": "user", "content": "The search functionality is crucial for our use case."},
                {"role": "assistant", "content": "Understood! Search functionality is a key requirement for your project."}
            ],
            "user_id": "developer_001",
            "metadata": {"category": "requirements", "priority": "high"}
        }
    ]
    
    added_memories = []
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            result = client.add(
                messages=test_case["messages"],
                user_id=test_case["user_id"],
                metadata=test_case.get("metadata", {})
            )
            
            print(f"✅ 记忆{i}添加成功!")
            print(f"   内容: {test_case['messages'][0]['content'][:50]}...")
            print(f"   结果: {result}")
            added_memories.append(result)
            
        except Exception as e:
            print(f"❌ 记忆{i}添加失败: {e}")
    
    return added_memories

def test_search_memories(client):
    """测试搜索功能"""
    print("\n🔍 测试搜索功能...")
    
    search_queries = [
        "re-call.ai项目",
                    "AI memory management", 
        "search functionality",
        "AI memory management",
        "project evaluation"
    ]
    
    for query in search_queries:
        try:
            # 使用v2版本的搜索，支持更多过滤器
            filters = {
                "AND": [
                    {"user_id": "developer_001"}
                ]
            }
            
            results = client.search(
                query=query,
                version="v2",
                filters=filters
            )
            
            print(f"✅ 搜索'{query}'成功!")
            print(f"   找到 {len(results)} 条结果")
            
            # 显示前2个结果的详细信息
            for i, result in enumerate(results[:2], 1):
                print(f"   {i}. {result}")
                
        except Exception as e:
            print(f"❌ 搜索'{query}'失败: {e}")

def test_get_all_memories(client):
    """测试获取所有记忆"""
    print("\n📋 测试获取所有记忆...")
    
    try:
        # 使用v2版本获取所有记忆
        filters = {
            "AND": [
                {"user_id": "developer_001"}
            ]
        }
        
        all_memories = client.get_all(
            version="v2",
            filters=filters,
            page=1,
            page_size=50
        )
        
        print(f"✅ 获取所有记忆成功!")
        print(f"   总共 {len(all_memories)} 条记忆")
        
        # 显示前3条记忆
        for i, memory in enumerate(all_memories[:3], 1):
            print(f"   {i}. ID: {memory.get('id', 'N/A')}")
            print(f"      内容: {str(memory.get('memory', 'N/A'))[:60]}...")
            
        return all_memories
        
    except Exception as e:
        print(f"❌ 获取所有记忆失败: {e}")
        return []

def test_advanced_search(client):
    """测试高级搜索功能"""
    print("\n🎯 测试高级搜索...")
    
    try:
        # 测试带元数据过滤的搜索
        filters = {
            "AND": [
                {"user_id": "developer_001"},
                {"metadata": {"category": "project"}}
            ]
        }
        
        results = client.search(
            query="development project",
            version="v2",
            filters=filters
        )
        
        print(f"✅ 高级搜索成功!")
        print(f"   项目相关结果数: {len(results)}")
        
        # 测试按优先级过滤
        priority_filters = {
            "AND": [
                {"user_id": "developer_001"},
                {"metadata": {"priority": "high"}}
            ]
        }
        
        priority_results = client.search(
            query="requirements",
            version="v2", 
            filters=priority_filters
        )
        
        print(f"✅ 优先级过滤搜索成功!")
        print(f"   高优先级结果数: {len(priority_results)}")
        
    except Exception as e:
        print(f"❌ 高级搜索失败: {e}")

def test_users_and_agents(client):
    """测试用户和代理管理"""
    print("\n👥 测试用户和代理管理...")
    
    try:
        # 获取所有用户
        users = client.users()
        print(f"✅ 获取用户列表成功!")
        print(f"   用户数量: {len(users)}")
        
        for user in users[:3]:  # 显示前3个用户
            print(f"   - {user}")
            
    except Exception as e:
        print(f"❌ 获取用户列表失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始全面测试mem0平台功能...")
    print(f"   API密钥: {API_KEY[:20]}...")
    
    # 测试1：平台连接
    client = test_platform_connection()
    if not client:
        print("\n❌ 无法连接到mem0平台，终止测试")
        return
    
    # 测试2：添加记忆
    added_memories = test_add_memories(client)
    
    # 等待处理
    print("\n⏳ 等待3秒让记忆处理完成...")
    import time
    time.sleep(3)
    
    # 测试3：搜索记忆
    test_search_memories(client)
    
    # 测试4：获取所有记忆
    all_memories = test_get_all_memories(client)
    
    # 测试5：高级搜索
    test_advanced_search(client)
    
    # 测试6：用户管理
    test_users_and_agents(client)
    
    print("\n🎉 mem0平台测试完成!")
    print("📊 测试总结:")
    print("   ✅ 如果大部分测试通过，mem0是re-call.ai项目的理想选择")
    print("   ✅ 特别关注搜索功能的稳定性和准确性")
    print("   ✅ mem0提供了更丰富的过滤和管理功能")

if __name__ == "__main__":
    main() 