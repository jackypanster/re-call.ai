# CHANGELOG

## [0.0.1] - 2024-05-18

### 初始版本（MVP 原型）
- 完成项目目录结构与依赖管理，采用 uv 作为虚拟环境和依赖管理工具
- 初始化 FastAPI 应用，支持基础健康检查
- 配置环境变量与日志系统，支持多环境切换
- 集成 Supabase，支持基础数据库操作（mock 测试覆盖）
- 集成 OpenRouter LLM 服务，支持摘要与标签提取（mock 测试覆盖）
- 集成 Supermemory.ai，支持内容添加与语义搜索（mock 测试覆盖）
- 实现服务依赖注入，便于后续扩展与测试
- 完善 API 路由结构与基础测试，测试覆盖率高
- 提供详细 README 与开发文档，强调 uv 工具链

---

> 版本号 0.0.1 适用于 MVP 阶段的第一个可用原型，后续功能完善和接口变更将递增版本号。 