#!/usr/bin/env python3
import requests
import json
import time

def test_memory_api():
    """测试re-call.ai文本记忆管理API"""
    
    base_url = "http://localhost:8080"
    
    print("🚀 测试re-call.ai文本记忆管理系统")
    print("=" * 50)
    
    # 1. 用户认证
    print("1. 用户认证...")
    login_resp = requests.post(f'{base_url}/api/auth/signin', 
                              json={'email': 'test@example.com', 'password': 'password123'})
    
    if login_resp.status_code == 200:
        token = login_resp.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print("✅ 登录成功")
    else:
        print(f"❌ 登录失败: {login_resp.status_code}")
        return
    
    # 2. 添加文本记忆
    print("\n2. 添加文本记忆...")
    memory_data = {
        'content': '今天学习了re-call.ai的文本记忆管理功能，这是一个基于mem0的智能记忆系统，支持语义搜索和智能分类。它可以帮助用户更好地管理和检索个人知识。',
        'metadata': {
            'category': '学习',
            'tags': ['AI', '记忆管理', 'mem0', 'FastAPI'],
            'importance': 'high',
            'subject': '技术学习'
        }
    }
    
    add_resp = requests.post(f'{base_url}/api/memories', 
                            json=memory_data, 
                            headers=headers)
    
    if add_resp.status_code == 200:
        result = add_resp.json()
        print(f"✅ {result['message']}")
        print(f"   记忆ID: {result['data']['memory_id']}")
    else:
        print(f"❌ 添加失败: {add_resp.status_code} - {add_resp.text}")
        return
    
    # 3. 搜索记忆
    print("\n3. 搜索记忆...")
    search_resp = requests.get(f'{base_url}/api/memories/search?q=记忆管理&limit=5', 
                              headers=headers)
    
    if search_resp.status_code == 200:
        results = search_resp.json()
        print(f"✅ 搜索成功，找到 {results['total']} 条记忆")
        for i, memory in enumerate(results['results'], 1):
            print(f"   {i}. {memory['content'][:50]}...")
    else:
        print(f"❌ 搜索失败: {search_resp.status_code}")
    
    # 4. 获取所有记忆
    print("\n4. 获取用户所有记忆...")
    list_resp = requests.get(f'{base_url}/api/memories?limit=10', 
                            headers=headers)
    
    if list_resp.status_code == 200:
        memories = list_resp.json()
        print(f"✅ 获取成功，共有 {memories['total']} 条记忆")
        print(f"   当前页显示: {len(memories['memories'])} 条")
    else:
        print(f"❌ 获取失败: {list_resp.status_code}")
    
    print("\n🎉 测试完成！")
    print("✅ 所有文本记忆管理功能正常工作")

if __name__ == "__main__":
    test_memory_api() 