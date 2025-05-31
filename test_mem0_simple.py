#!/usr/bin/env python3
"""
简单测试mem0基本功能
"""
import os

# 配置API密钥
API_KEY = "m0-jy0qogy2cP9iWJYNlDAfOp3ANexxorj8xAmI9A1i"

def test_import():
    """测试导入"""
    print("📦 测试导入...")
    
    try:
        from mem0 import MemoryClient
        print("✅ MemoryClient导入成功")
        
        from mem0 import Memory
        print("✅ Memory导入成功")
        
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_local_memory():
    """测试本地Memory（不需要网络）"""
    print("\n🧠 测试本地Memory...")
    
    try:
        from mem0 import Memory
        
        # 创建本地memory实例
        m = Memory()
        
        # 添加记忆
        result = m.add("我正在测试mem0的本地功能", user_id="test_user")
        print(f"✅ 本地添加记忆成功: {result}")
        
        # 搜索记忆
        search_results = m.search(query="测试mem0", user_id="test_user")
        print(f"✅ 本地搜索成功，找到 {len(search_results)} 条结果")
        
        # 获取所有记忆
        all_memories = m.get_all(user_id="test_user")
        print(f"✅ 获取所有记忆成功，共 {len(all_memories)} 条")
        
        return True
        
    except Exception as e:
        print(f"❌ 本地Memory测试失败: {e}")
        return False

def test_client_init():
    """测试客户端初始化（可能需要网络）"""
    print("\n🌐 测试客户端初始化...")
    
    try:
        from mem0 import MemoryClient
        
        # 尝试不同的初始化方式
        client = MemoryClient(api_key=API_KEY)
        print("✅ MemoryClient初始化成功")
        
        return client
        
    except Exception as e:
        print(f"❌ MemoryClient初始化失败: {e}")
        print(f"   错误类型: {type(e)}")
        return None

def test_environment_setup():
    """测试环境变量设置"""
    print("\n⚙️ 测试环境变量...")
    
    # 设置环境变量
    os.environ['MEM0_API_KEY'] = API_KEY
    
    try:
        from mem0 import MemoryClient
        
        # 尝试使用环境变量初始化
        client = MemoryClient()  # 不传递api_key，使用环境变量
        print("✅ 使用环境变量初始化成功")
        
        return client
        
    except Exception as e:
        print(f"❌ 环境变量初始化失败: {e}")
        return None

def main():
    """主测试函数"""
    print("🚀 开始mem0基础测试...")
    
    # 测试1：导入
    if not test_import():
        return
    
    # 测试2：本地Memory
    local_success = test_local_memory()
    
    # 测试3：客户端初始化
    client = test_client_init()
    
    # 测试4：环境变量
    if not client:
        client = test_environment_setup()
    
    # 总结
    print("\n📊 测试总结:")
    print(f"   本地Memory: {'✅ 成功' if local_success else '❌ 失败'}")
    print(f"   客户端连接: {'✅ 成功' if client else '❌ 失败'}")
    
    if local_success:
        print("\n🎉 mem0本地功能正常，可以作为备选方案!")
    
    if client:
        print("🌐 网络客户端也正常，可以使用云端功能!")
    else:
        print("⚠️ 网络客户端有问题，但本地功能可用")

if __name__ == "__main__":
    main() 