#!/usr/bin/env python
"""
Task 2.2 验证测试: 数据模型定义
验证核心数据模型是否正确定义并通过验证
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_memory_create_request():
    """测试MemoryCreateRequest模型验证"""
    print("1️⃣ 测试MemoryCreateRequest模型...")
    
    try:
        from app.models.memory import MemoryCreateRequest
        from pydantic import ValidationError
        
        # 测试有效数据
        valid_data = {
            "content": "这是一个测试记忆",
            "metadata": {"category": "test", "tags": ["validation"]}
        }
        request = MemoryCreateRequest(**valid_data)
        assert request.content == "这是一个测试记忆"
        assert request.metadata["category"] == "test"
        print("✅ 有效数据验证通过")
        
        # 测试空内容
        try:
            MemoryCreateRequest(content="", metadata={})
            print("❌ 空内容验证失败")
            return False
        except ValidationError:
            print("✅ 空内容验证错误捕获正常")
        
        # 测试内容过长
        try:
            long_content = "a" * 10001
            MemoryCreateRequest(content=long_content)
            print("❌ 长内容验证失败")
            return False
        except ValidationError:
            print("✅ 内容长度限制验证正常")
        
        return True
        
    except Exception as e:
        print(f"❌ MemoryCreateRequest测试失败: {e}")
        return False

def test_memory_response():
    """测试MemoryResponse模型"""
    print("\n2️⃣ 测试MemoryResponse模型...")
    
    try:
        from app.models.memory import MemoryResponse
        
        # 模拟mem0 API返回的数据格式
        mem0_data = {
            "id": "59bcc066-d304-4259-8a26-60da89bf9243",
            "memory": "测试记忆内容",
            "user_id": "test_user",
            "metadata": {"category": "test"},
            "categories": ["misc"],
            "created_at": "2024-12-01T12:00:00Z",
            "updated_at": "2024-12-01T12:00:00Z",
            "score": 0.95
        }
        
        response = MemoryResponse(**mem0_data)
        assert response.id == "59bcc066-d304-4259-8a26-60da89bf9243"
        assert response.memory == "测试记忆内容"
        assert response.user_id == "test_user"
        assert response.score == 0.95
        print("✅ mem0返回数据映射正常")
        
        return True
        
    except Exception as e:
        print(f"❌ MemoryResponse测试失败: {e}")
        return False

def test_search_request():
    """测试SearchRequest模型"""
    print("\n3️⃣ 测试SearchRequest模型...")
    
    try:
        from app.models.memory import SearchRequest
        from pydantic import ValidationError
        
        # 测试有效搜索请求
        valid_search = {
            "query": "FastAPI学习",
            "limit": 10,
            "categories": ["study"],
            "metadata_filter": {"importance": "high"}
        }
        search_req = SearchRequest(**valid_search)
        assert search_req.query == "FastAPI学习"
        assert search_req.limit == 10
        print("✅ 有效搜索请求验证通过")
        
        # 测试空查询
        try:
            SearchRequest(query="")
            print("❌ 空查询验证失败")
            return False
        except ValidationError:
            print("✅ 空查询验证错误捕获正常")
        
        return True
        
    except Exception as e:
        print(f"❌ SearchRequest测试失败: {e}")
        return False

def test_response_models():
    """测试响应模型"""
    print("\n4️⃣ 测试响应模型...")
    
    try:
        from app.models.memory import (
            SearchResponse, MemoryListResponse, 
            StandardResponse, ErrorResponse
        )
        
        # 测试搜索响应
        search_result = {
            "results": [],
            "total": 1,
            "query": "搜索测试",
            "limit": 10
        }
        search_resp = SearchResponse(**search_result)
        assert search_resp.total == 1
        assert search_resp.query == "搜索测试"
        print("✅ 搜索响应模型验证通过")
        
        # 测试标准响应
        std_resp = StandardResponse(
            success=True,
            message="操作成功",
            data={"result": "test"}
        )
        assert std_resp.success == True
        print("✅ 标准响应模型正常")
        
        # 测试错误响应
        err_resp = ErrorResponse(
            error="ValidationError",
            message="验证失败"
        )
        assert err_resp.success == False
        print("✅ 错误响应模型正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 响应模型测试失败: {e}")
        return False

def test_model_documentation():
    """测试模型文档"""
    print("\n5️⃣ 测试模型文档...")
    
    try:
        from app.models.memory import MemoryCreateRequest
        
        # 检查模型文档
        assert MemoryCreateRequest.__doc__ is not None
        assert "创建记忆请求模型" in MemoryCreateRequest.__doc__
        
        # 检查字段schema
        schema = MemoryCreateRequest.model_json_schema()
        assert "properties" in schema
        assert "content" in schema["properties"]
        
        print("✅ 模型文档和示例完整")
        return True
        
    except Exception as e:
        print(f"❌ 文档测试失败: {e}")
        return False

def run_all_tests():
    """运行所有Task 2.2验证测试"""
    print("🔄 开始验证Task 2.2: 数据模型定义...")
    
    tests = [
        test_memory_create_request,
        test_memory_response,
        test_search_request,
        test_response_models,
        test_model_documentation
    ]
    
    passed = 0
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 执行失败: {e}")
    
    if passed == len(tests):
        print("\n🎉 Task 2.2验证完成!")
        print("✅ 所有数据模型定义正确且验证功能正常")
        return True
    else:
        print(f"\n❌ Task 2.2验证失败: {passed}/{len(tests)} 测试通过")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1) 