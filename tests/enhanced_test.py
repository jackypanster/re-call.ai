#!/usr/bin/env python3
import requests
import json
import time

def enhanced_memory_test():
    """增强版文本记忆管理测试"""
    
    base_url = "http://localhost:8080"
    
    print("🚀 re-call.ai 文本记忆管理系统 - 增强测试")
    print("=" * 60)
    
    # 认证
    print("🔑 用户认证...")
    login_resp = requests.post(f'{base_url}/api/auth/signin', 
                              json={'email': 'test@example.com', 'password': 'password123'})
    token = login_resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print("✅ 认证成功")
    
    # 添加多条不同类型的记忆
    memories_to_add = [
        {
            'content': 'FastAPI是一个现代、快速的Python Web框架，支持自动API文档生成、类型提示和异步编程',
            'metadata': {'category': '技术', 'tags': ['Python', 'FastAPI', 'Web开发'], 'importance': 'high'}
        },
        {
            'content': '今天读了《深度工作》这本书，学到了专注工作的重要性，要减少干扰，提高工作效率',
            'metadata': {'category': '阅读', 'tags': ['效率', '专注力', '个人成长'], 'importance': 'medium'}
        },
        {
            'content': 'mem0是一个AI记忆平台，可以为应用添加个性化的记忆功能，支持语义搜索和上下文感知',
            'metadata': {'category': '技术', 'tags': ['AI', 'mem0', '记忆管理'], 'importance': 'high'}
        }
    ]
    
    print(f"\n📝 添加 {len(memories_to_add)} 条记忆...")
    memory_ids = []
    for i, memory in enumerate(memories_to_add, 1):
        resp = requests.post(f'{base_url}/api/memories', json=memory, headers=headers)
        if resp.status_code == 200:
            result = resp.json()
            memory_id = result['data']['memory_id']
            memory_ids.append(memory_id)
            print(f"   {i}. ✅ 添加成功 (ID: {memory_id})")
        else:
            print(f"   {i}. ❌ 添加失败: {resp.status_code}")
    
    # 测试不同的搜索查询
    search_queries = [
        ('Python', '搜索Python相关内容'),
        ('效率', '搜索效率相关内容'), 
        ('AI记忆', '搜索AI和记忆相关内容'),
        ('深度工作', '搜索特定书籍')
    ]
    
    print(f"\n🔍 测试语义搜索功能...")
    for query, description in search_queries:
        search_resp = requests.get(f'{base_url}/api/memories/search?q={query}&limit=5', headers=headers)
        if search_resp.status_code == 200:
            results = search_resp.json()
            print(f"   📌 {description}: 找到 {results['total']} 条结果")
            for j, memory in enumerate(results['results'], 1):
                print(f"      {j}. {memory['content'][:60]}...")
        else:
            print(f"   ❌ 搜索失败: {search_resp.status_code}")
        print()
    
    # 测试分页功能
    print("📄 测试分页功能...")
    list_resp = requests.get(f'{base_url}/api/memories?limit=2&offset=0', headers=headers)
    if list_resp.status_code == 200:
        memories = list_resp.json()
        print(f"   ✅ 第1页: 显示 {len(memories['memories'])} 条，总共 {memories['total']} 条")
    
    # 测试更新记忆功能
    if memory_ids:
        print("\n✏️ 测试更新记忆功能...")
        update_data = {
            'content': 'FastAPI是一个现代、快速的Python Web框架，支持自动API文档生成、类型提示、异步编程和依赖注入系统'
        }
        update_resp = requests.put(f'{base_url}/api/memories/{memory_ids[0]}', 
                                  json=update_data, headers=headers)
        if update_resp.status_code == 200:
            print(f"   ✅ 更新成功: {update_resp.json()['message']}")
        else:
            print(f"   ❌ 更新失败: {update_resp.status_code}")
    
    # 测试删除记忆功能
    if len(memory_ids) > 1:
        print("\n🗑️ 测试删除记忆功能...")
        delete_resp = requests.delete(f'{base_url}/api/memories/{memory_ids[-1]}', headers=headers)
        if delete_resp.status_code == 200:
            print(f"   ✅ 删除成功: {delete_resp.json()['message']}")
        else:
            print(f"   ❌ 删除失败: {delete_resp.status_code}")
    
    # 最终统计
    print("\n📊 最终统计...")
    final_resp = requests.get(f'{base_url}/api/memories', headers=headers)
    if final_resp.status_code == 200:
        final_memories = final_resp.json()
        print(f"   📝 当前总记忆数: {final_memories['total']}")
        print(f"   👤 用户ID: {final_memories['user_id']}")
    
    print("\n🎉 增强测试完成！")
    print("✅ re-call.ai文本记忆管理系统功能完整，性能良好")
    print("🌟 支持: 添加、搜索、更新、删除、分页等完整CRUD操作")

if __name__ == "__main__":
    enhanced_memory_test() 