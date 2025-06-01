#!/usr/bin/env python
"""
Task 2.3 验证测试: 错误处理和日志系统
验证异常处理和结构化日志功能
"""
import sys
import os
import logging
import json
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_custom_exceptions():
    """测试自定义异常类型"""
    print("1️⃣ 测试自定义异常类型...")
    
    try:
        from app.utils.exceptions import (
            AppException, ValidationException, NotFoundException,
            UnauthorizedException, ForbiddenException, ConflictException,
            ExternalServiceException, RateLimitException,
            MemoryServiceException, AuthServiceException
        )
        
        # 测试基础异常
        app_exc = AppException(detail="测试异常", error_code="TEST_ERROR")
        assert app_exc.error_code == "TEST_ERROR"
        assert app_exc.detail == "测试异常"
        assert app_exc.status_code == 400
        print("✅ AppException基础功能正常")
        
        # 测试验证异常
        validation_exc = ValidationException(detail="字段验证失败", field="content")
        assert validation_exc.error_code == "VALIDATION_ERROR"
        assert validation_exc.status_code == 422
        assert validation_exc.context["field"] == "content"
        print("✅ ValidationException验证异常正常")
        
        # 测试404异常
        not_found_exc = NotFoundException(detail="记忆未找到", resource_type="memory")
        assert not_found_exc.error_code == "RESOURCE_NOT_FOUND"
        assert not_found_exc.status_code == 404
        assert not_found_exc.context["resource_type"] == "memory"
        print("✅ NotFoundException资源异常正常")
        
        # 测试外部服务异常
        memory_exc = MemoryServiceException(detail="mem0服务错误", operation="search")
        assert memory_exc.error_code == "EXTERNAL_SERVICE_ERROR"
        assert memory_exc.context["service_name"] == "mem0"
        assert memory_exc.context["operation"] == "search"
        print("✅ MemoryServiceException服务异常正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 自定义异常测试失败: {e}")
        return False

def test_sensitive_data_filter():
    """测试敏感信息过滤"""
    print("\n2️⃣ 测试敏感信息过滤...")
    
    try:
        from app.utils.logger import SensitiveDataFilter
        
        filter_instance = SensitiveDataFilter()
        
        # 测试API密钥过滤
        test_text = "API_KEY=sk-1234567890abcdef token=bearer-xyz password=secret123"
        masked_text = filter_instance._mask_sensitive_data(test_text)
        
        assert "sk-1234567890abcdef" not in masked_text
        assert "bearer-xyz" not in masked_text
        assert "secret123" not in masked_text
        assert "***MASKED***" in masked_text
        print("✅ 敏感信息过滤正常")
        
        # 测试JSON格式的API密钥
        json_text = '{"api_key": "m0-abcdef123456", "password": "mypassword"}'
        masked_json = filter_instance._mask_sensitive_data(json_text)
        assert "m0-abcdef123456" not in masked_json
        assert "mypassword" not in masked_json
        print("✅ JSON格式敏感信息过滤正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 敏感信息过滤测试失败: {e}")
        return False

def test_structured_logging():
    """测试结构化日志格式"""
    print("\n3️⃣ 测试结构化日志格式...")
    
    try:
        from app.utils.logger import StructuredFormatter, get_logger
        import io
        
        # 创建测试日志记录
        logger = get_logger("test")
        
        # 测试日志消息格式
        logger.info("测试日志消息", extra={
            'user_id': 'test_user',
            'operation': 'test_operation',
            'duration': 123.45
        })
        print("✅ 结构化日志记录正常")
        
        # 测试错误日志
        try:
            raise ValueError("测试错误")
        except ValueError as e:
            logger.error("捕获到测试错误", exc_info=True)
        print("✅ 错误日志记录正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 结构化日志测试失败: {e}")
        return False

def test_log_levels():
    """测试不同环境的日志级别"""
    print("\n4️⃣ 测试日志级别配置...")
    
    try:
        from app.utils.logger import get_log_level
        
        # 模拟获取日志级别
        log_level = get_log_level()
        assert isinstance(log_level, int)
        assert log_level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]
        print("✅ 日志级别配置正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 日志级别测试失败: {e}")
        return False

def test_exception_handlers_import():
    """测试异常处理器导入"""
    print("\n5️⃣ 测试异常处理器...")
    
    try:
        from app.utils.exception_handlers import (
            app_exception_handler, http_exception_handler,
            validation_exception_handler, general_exception_handler,
            setup_exception_handlers
        )
        
        # 验证处理器函数存在且可调用
        assert callable(app_exception_handler)
        assert callable(http_exception_handler)
        assert callable(validation_exception_handler)
        assert callable(general_exception_handler)
        assert callable(setup_exception_handlers)
        print("✅ 异常处理器导入正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 异常处理器测试失败: {e}")
        return False

def test_error_response_models():
    """测试错误响应模型"""
    print("\n6️⃣ 测试错误响应模型...")
    
    try:
        from app.models.memory import ErrorResponse
        
        # 测试错误响应创建
        error_resp = ErrorResponse(
            error="TEST_ERROR",
            message="测试错误消息",
            details={"field": "test_field", "value": "invalid"}
        )
        
        assert error_resp.success == False
        assert error_resp.error == "TEST_ERROR"
        assert error_resp.message == "测试错误消息"
        assert error_resp.details["field"] == "test_field"
        print("✅ 错误响应模型正常")
        
        # 测试模型序列化
        error_dict = error_resp.model_dump()
        assert "success" in error_dict
        assert "error" in error_dict
        assert "message" in error_dict
        assert "details" in error_dict
        print("✅ 错误响应序列化正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误响应模型测试失败: {e}")
        return False

def test_logger_utilities():
    """测试日志工具函数"""
    print("\n7️⃣ 测试日志工具函数...")
    
    try:
        from app.utils.logger import log_api_call, log_error, get_logger
        
        logger = get_logger("test")
        
        # 测试API调用日志
        log_api_call(logger, "test_operation", user_id="test_user", duration=100.5)
        print("✅ API调用日志工具正常")
        
        # 测试错误日志
        try:
            raise ValueError("测试错误")
        except ValueError as e:
            log_error(logger, e, {"context": "test_context"})
        print("✅ 错误日志工具正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 日志工具函数测试失败: {e}")
        return False

def run_all_tests():
    """运行所有Task 2.3验证测试"""
    print("🔄 开始验证Task 2.3: 错误处理和日志系统...")
    
    tests = [
        test_custom_exceptions,
        test_sensitive_data_filter,
        test_structured_logging,
        test_log_levels,
        test_exception_handlers_import,
        test_error_response_models,
        test_logger_utilities
    ]
    
    passed = 0
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 执行失败: {e}")
    
    if passed == len(tests):
        print("\n🎉 Task 2.3验证完成!")
        print("✅ 错误处理和日志系统功能完全正常")
        return True
    else:
        print(f"\n❌ Task 2.3验证失败: {passed}/{len(tests)} 测试通过")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1) 