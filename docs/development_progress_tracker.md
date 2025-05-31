# re-call.ai 后端开发任务清单

## 📋 项目概述

基于mem0 Platform构建re-call.ai后端API服务，采用FastAPI框架，专注MVP核心功能实现。

### 🎯 技术选型
- **核心服务**: mem0 Platform API
- **后端框架**: FastAPI + Python 3.11+
- **包管理工具**: uv
- **测试框架**: pytest + httpx
- **开发原则**: MVP优先，避免过度工程

### 📊 进度标识
- ⬜ 未开始
- 🟡 进行中
- ✅ 已完成
- ❌ 阻塞
- 🧪 测试中

---

## Phase 1: 项目基础设置

### Task 1.1 ⬜ 环境初始化和项目结构
**目标**: 建立标准的Python项目结构，配置uv环境管理
**前置条件**: 无
**技术要求**: 
- 使用uv创建虚拟环境
- 建立FastAPI项目目录结构
- 配置基础依赖

**验收标准**:
- [ ] `uv venv` 成功创建虚拟环境
- [ ] `uv pip install fastapi uvicorn` 成功安装核心依赖
- [ ] 项目目录结构符合FastAPI最佳实践
- [ ] `pyproject.toml` 配置正确且可安装
- [ ] `.gitignore` 包含Python和uv相关忽略规则

**CLI验证命令**:
```bash
uv venv --python 3.11
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip list
```

**预估工时**: 1小时
**风险点**: uv版本兼容性问题

---

### Task 1.2 ⬜ FastAPI应用骨架创建
**目标**: 创建基础的FastAPI应用，确保服务可启动
**前置条件**: Task 1.1 完成
**技术要求**:
- 创建FastAPI主应用文件
- 配置基础路由和健康检查
- 设置CORS和基础中间件

**验收标准**:
- [ ] `uvicorn app.main:app --reload` 成功启动服务
- [ ] 访问 `http://localhost:8000` 返回200状态
- [ ] 访问 `http://localhost:8000/docs` 显示Swagger文档
- [ ] 健康检查端点 `/health` 正常响应
- [ ] CORS配置允许前端开发调用

**CLI验证命令**:
```bash
uvicorn app.main:app --reload
curl http://localhost:8000/health
curl -I http://localhost:8000/docs
```

**预估工时**: 2小时
**风险点**: 端口冲突或依赖缺失

---

### Task 1.3 ⬜ 环境变量和配置管理
**目标**: 建立环境变量管理系统，支持mem0 API密钥配置
**前置条件**: Task 1.2 完成
**技术要求**:
- 使用pydantic-settings进行配置管理
- 创建.env.example模板
- 实现配置验证和错误处理

**验收标准**:
- [ ] `.env.example` 包含所有必需的环境变量
- [ ] 配置类使用Pydantic进行类型验证
- [ ] 缺少关键配置时应用启动失败并给出清晰错误信息
- [ ] 配置加载成功时日志记录配置状态
- [ ] 敏感信息（API密钥）不出现在日志中

**CLI验证命令**:
```bash
# 测试缺少配置的情况
uvicorn app.main:app --reload
# 配置正确后测试
cp .env.example .env
# 编辑.env添加真实的mem0 API密钥
uvicorn app.main:app --reload
```

**预估工时**: 1.5小时
**风险点**: 环境变量格式或验证逻辑错误

---

## Phase 2: 核心服务集成

### Task 2.1 ⬜ mem0客户端集成
**目标**: 集成mem0 Platform API，实现基础的记忆管理功能
**前置条件**: Task 1.3 完成，需要有效的mem0 API密钥
**技术要求**:
- 安装mem0ai Python SDK
- 创建mem0服务包装类
- 实现连接测试和错误处理

**验收标准**:
- [ ] `uv pip install mem0ai` 成功安装最新版本
- [ ] mem0客户端能够成功连接到Platform API
- [ ] 实现基础的添加记忆功能
- [ ] 实现基础的搜索记忆功能
- [ ] 网络错误和API错误有合适的异常处理
- [ ] 服务层有详细的日志记录

**CLI验证命令**:
```bash
python -c "
from app.services.memory_service import MemoryService
service = MemoryService()
result = service.add_memory('test message', 'test_user')
print(f'Added memory: {result}')
search = service.search_memories('test', 'test_user')
print(f'Search results: {search}')
"
```

**预估工时**: 2小时
**风险点**: mem0 API配额限制或网络连接问题

---

### Task 2.2 ⬜ 数据模型定义
**目标**: 定义核心数据模型，用于API请求和响应
**前置条件**: Task 2.1 完成
**技术要求**:
- 使用Pydantic定义数据模型
- 覆盖记忆添加、搜索、更新操作
- 包含适当的验证和文档

**验收标准**:
- [ ] `MemoryCreateRequest` 模型包含必要字段和验证
- [ ] `MemoryResponse` 模型正确映射mem0返回数据
- [ ] `SearchRequest` 模型支持查询和过滤参数
- [ ] `SearchResponse` 模型包含分页和结果信息
- [ ] 所有模型有适当的文档字符串和示例
- [ ] 模型验证能够捕获无效输入

**CLI验证命令**:
```bash
python -c "
from app.models.memory import MemoryCreateRequest
try:
    valid = MemoryCreateRequest(content='test', user_id='user123')
    print('Valid model created')
    invalid = MemoryCreateRequest(content='', user_id='')
except Exception as e:
    print(f'Validation caught: {e}')
"
```

**预估工时**: 1.5小时
**风险点**: 模型定义与mem0 API不匹配

---

### Task 2.3 ⬜ 错误处理和日志系统
**目标**: 建立统一的错误处理和结构化日志系统
**前置条件**: Task 2.2 完成
**技术要求**:
- 自定义异常类型
- FastAPI异常处理器
- 结构化日志配置

**验收标准**:
- [ ] 自定义异常类型覆盖主要错误场景
- [ ] 全局异常处理器返回标准化错误响应
- [ ] 日志格式包含时间戳、级别、模块和消息
- [ ] 不同环境（开发/生产）有不同的日志级别
- [ ] API调用错误有详细的上下文信息
- [ ] 敏感信息不会被记录到日志中

**CLI验证命令**:
```bash
# 测试错误处理
curl -X POST http://localhost:8000/api/memories \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
# 检查日志输出格式
tail -f app.log
```

**预估工时**: 2小时
**风险点**: 日志配置复杂或性能影响

---

## Phase 3: 核心API端点实现

### Task 3.1 ⬜ 记忆添加API端点
**目标**: 实现添加记忆的API端点，支持文本内容和元数据
**前置条件**: Task 2.3 完成
**技术要求**:
- POST /api/memories 端点
- 请求验证和响应序列化
- mem0 API调用集成

**验收标准**:
- [ ] POST请求能够成功添加记忆到mem0
- [ ] 请求体验证拒绝无效数据
- [ ] 返回标准化的成功响应格式
- [ ] 支持可选的元数据字段
- [ ] API文档在Swagger中正确显示
- [ ] 错误情况返回适当的HTTP状态码

**CLI验证命令**:
```bash
# 成功添加记忆
curl -X POST http://localhost:8000/api/memories \
  -H "Content-Type: application/json" \
  -d '{
    "content": "今天学习了FastAPI的依赖注入系统",
    "user_id": "user123",
    "metadata": {"category": "learning"}
  }'

# 测试验证失败
curl -X POST http://localhost:8000/api/memories \
  -H "Content-Type: application/json" \
  -d '{"content": ""}'
```

**预估工时**: 2小时
**风险点**: mem0 API调用失败或数据格式不匹配

---

### Task 3.2 ⬜ 记忆搜索API端点
**目标**: 实现智能搜索功能，支持语义搜索和过滤
**前置条件**: Task 3.1 完成
**技术要求**:
- GET /api/memories/search 端点
- 支持查询参数和过滤器
- 分页和排序功能

**验收标准**:
- [ ] 支持基础的语义搜索查询
- [ ] 支持用户ID过滤确保数据隔离
- [ ] 支持元数据过滤（如分类、日期范围）
- [ ] 实现分页功能（limit、offset）
- [ ] 返回搜索结果和元信息（总数、页数等）
- [ ] 空查询返回适当的默认结果

**CLI验证命令**:
```bash
# 基础搜索
curl "http://localhost:8000/api/memories/search?q=FastAPI&user_id=user123"

# 带过滤器的搜索
curl "http://localhost:8000/api/memories/search?q=学习&user_id=user123&category=learning&limit=5"

# 分页测试
curl "http://localhost:8000/api/memories/search?user_id=user123&limit=2&offset=0"
```

**预估工时**: 2.5小时
**风险点**: 搜索参数复杂或性能问题

---

### Task 3.3 ⬜ 记忆管理API端点
**目标**: 实现记忆的获取、更新和删除功能
**前置条件**: Task 3.2 完成
**技术要求**:
- GET /api/memories/{memory_id} 端点
- PUT /api/memories/{memory_id} 端点  
- DELETE /api/memories/{memory_id} 端点

**验收标准**:
- [ ] 能够通过ID获取特定记忆详情
- [ ] 能够更新记忆内容和元数据
- [ ] 能够删除指定的记忆
- [ ] 所有操作验证用户权限（只能操作自己的记忆）
- [ ] 不存在的记忆ID返回404错误
- [ ] 权限不足返回403错误

**CLI验证命令**:
```bash
# 获取记忆详情
curl "http://localhost:8000/api/memories/MEMORY_ID?user_id=user123"

# 更新记忆
curl -X PUT http://localhost:8000/api/memories/MEMORY_ID \
  -H "Content-Type: application/json" \
  -d '{
    "content": "更新后的内容",
    "user_id": "user123",
    "metadata": {"category": "updated"}
  }'

# 删除记忆
curl -X DELETE "http://localhost:8000/api/memories/MEMORY_ID?user_id=user123"
```

**预估工时**: 2小时
**风险点**: 权限控制逻辑复杂或mem0 API限制

---

### Task 3.4 ⬜ 用户记忆列表API端点
**目标**: 实现获取用户所有记忆的列表功能
**前置条件**: Task 3.3 完成
**技术要求**:
- GET /api/memories 端点
- 支持分页、排序和基础过滤
- 返回记忆摘要信息

**验收标准**:
- [ ] 能够获取指定用户的所有记忆列表
- [ ] 支持按创建时间或更新时间排序
- [ ] 支持分页功能防止数据量过大
- [ ] 支持按元数据字段进行基础过滤
- [ ] 返回记忆摘要而非完整内容
- [ ] 包含分页元信息（总数、当前页等）

**CLI验证命令**:
```bash
# 获取用户记忆列表
curl "http://localhost:8000/api/memories?user_id=user123&limit=10&offset=0"

# 按时间排序
curl "http://localhost:8000/api/memories?user_id=user123&sort_by=created_at&order=desc"

# 按分类过滤
curl "http://localhost:8000/api/memories?user_id=user123&category=learning"
```

**预估工时**: 1.5小时
**风险点**: 大量数据的性能问题

---

## Phase 4: 测试和质量保证

### Task 4.1 ⬜ 单元测试套件
**目标**: 为所有服务层和工具函数编写单元测试
**前置条件**: Task 3.4 完成
**技术要求**:
- 使用pytest和pytest-asyncio
- Mock外部API调用
- 覆盖主要业务逻辑

**验收标准**:
- [ ] 所有服务类方法有对应的单元测试
- [ ] mem0 API调用被正确Mock，不依赖真实API
- [ ] 数据模型验证逻辑有完整测试覆盖
- [ ] 错误处理路径有对应测试用例
- [ ] 测试覆盖率达到85%以上
- [ ] `pytest tests/unit/` 命令能够成功运行所有测试

**CLI验证命令**:
```bash
# 运行单元测试
pytest tests/unit/ -v

# 检查测试覆盖率
pytest tests/unit/ --cov=app --cov-report=term-missing

# 运行特定测试文件
pytest tests/unit/test_memory_service.py -v
```

**预估工时**: 3小时
**风险点**: Mock配置复杂或测试环境问题

---

### Task 4.2 ⬜ 集成测试套件  
**目标**: 编写API端点的集成测试，验证完整的请求-响应流程
**前置条件**: Task 4.1 完成
**技术要求**:
- 使用FastAPI TestClient
- 测试真实的HTTP请求流程
- 包含错误场景测试

**验收标准**:
- [ ] 所有API端点有对应的集成测试
- [ ] 测试覆盖正常流程和错误场景
- [ ] 使用测试专用的mem0配置或Mock
- [ ] 测试数据隔离，不影响开发环境
- [ ] 响应格式和状态码验证
- [ ] `pytest tests/integration/` 命令能够成功运行

**CLI验证命令**:
```bash
# 运行集成测试
pytest tests/integration/ -v

# 运行特定API测试
pytest tests/integration/test_memory_api.py -v

# 运行所有测试
pytest tests/ -v
```

**预估工时**: 2.5小时
**风险点**: 测试环境配置或API调用限制

---

### Task 4.3 ⬜ API文档完善和验证
**目标**: 完善API文档，确保Swagger文档准确且易用
**前置条件**: Task 4.2 完成
**技术要求**:
- 完善OpenAPI文档字符串
- 添加请求/响应示例
- 验证文档准确性

**验收标准**:
- [ ] 所有API端点有详细的描述和参数说明
- [ ] 请求和响应模型有清晰的示例数据
- [ ] 错误响应格式有文档说明
- [ ] Swagger UI中可以直接测试API调用
- [ ] API文档包含认证和使用说明
- [ ] 文档与实际API行为完全一致

**CLI验证命令**:
```bash
# 启动服务并访问文档
uvicorn app.main:app --reload
# 浏览器访问 http://localhost:8000/docs
# 在Swagger UI中测试各个端点

# 验证OpenAPI规范
curl http://localhost:8000/openapi.json | python -m json.tool
```

**预估工时**: 1.5小时
**风险点**: 文档与实现不一致

---

## Phase 5: 部署和监控准备

### Task 5.1 ⬜ 容器化配置
**目标**: 创建Docker配置，支持容器化部署
**前置条件**: Task 4.3 完成
**技术要求**:
- 多阶段Docker构建
- 生产环境优化
- 健康检查配置

**验收标准**:
- [ ] Dockerfile能够成功构建应用镜像
- [ ] 镜像大小合理（<500MB）
- [ ] 容器启动时间<10秒
- [ ] 健康检查端点正常工作
- [ ] 环境变量正确传递到容器
- [ ] 容器日志输出到stdout

**CLI验证命令**:
```bash
# 构建Docker镜像
docker build -t re-call-api .

# 运行容器
docker run -p 8000:8000 --env-file .env re-call-api

# 测试健康检查
curl http://localhost:8000/health

# 检查容器日志
docker logs <container_id>
```

**预估工时**: 2小时
**风险点**: Docker配置或依赖问题

---

### Task 5.2 ⬜ 生产环境配置
**目标**: 准备生产环境部署配置和监控
**前置条件**: Task 5.1 完成
**技术要求**:
- 生产环境变量配置
- 性能优化设置
- 基础监控配置

**验收标准**:
- [ ] 生产环境配置模板完整
- [ ] 日志级别和格式适合生产环境
- [ ] 性能配置（worker数量、超时等）合理
- [ ] 健康检查和指标端点可用
- [ ] 部署文档清晰完整
- [ ] 安全配置检查清单

**CLI验证命令**:
```bash
# 生产模式启动测试
ENV=production uvicorn app.main:app --host 0.0.0.0 --port 8000

# 性能测试
ab -n 100 -c 10 http://localhost:8000/health

# 检查指标端点
curl http://localhost:8000/metrics
```

**预估工时**: 1.5小时
**风险点**: 生产环境配置错误

---

## 📊 进度总览

| 阶段 | 任务数 | 预估总工时 | 状态 |
|------|--------|------------|------|
| Phase 1: 项目基础设置 | 3 | 4.5小时 | ⬜ |
| Phase 2: 核心服务集成 | 3 | 5.5小时 | ⬜ |
| Phase 3: 核心API端点实现 | 4 | 8小时 | ⬜ |
| Phase 4: 测试和质量保证 | 3 | 7小时 | ⬜ |
| Phase 5: 部署和监控准备 | 2 | 3.5小时 | ⬜ |
| **总计** | **15** | **28.5小时** | **⬜** |

## 🚀 开始执行

### 当前任务
**Task 1.1**: 环境初始化和项目结构

### 执行原则
1. **严格串行执行** - 完成一个任务后才开始下一个
2. **完整验收** - 所有验收标准必须通过
3. **测试驱动** - 每个功能都有对应测试
4. **文档同步** - 及时更新相关文档

### 准备开始
确认以下准备工作已完成：
- [ ] 开发环境已安装uv
- [ ] 获得有效的mem0 API密钥
- [ ] 确认网络可以访问mem0.ai服务

---

**文档更新**: 2024年12月  
**版本**: v2.0 (基于mem0架构)  
**下次更新**: Task完成后同步更新进度 