# re-call.ai - AI驱动的个人记忆管理系统

## 🎯 项目愿景

re-call.ai 是一个基于AI的个人记忆管理系统，通过集成先进的AI记忆服务（mem0），为用户提供智能化的记录、搜索和记忆管理体验。

### 核心价值
- 🧠 **智能记录**：支持文本和语音输入，自动处理和分类
- 🔍 **语义搜索**：基于AI理解进行智能搜索和匹配  
- 📚 **记忆管理**：自动组织和优化个人记忆库
- 🔒 **隐私安全**：个人数据严格隔离和保护

## 🏗️ 技术架构

### 核心技术栈
- **后端框架**：FastAPI + Python 3.11+
- **AI记忆服务**：mem0 Platform
- **语音处理**：OpenAI Whisper API
- **前端**：Next.js + TailwindCSS
- **部署**：Railway/Vercel

### 系统架构
```
用户输入 → FastAPI → mem0 AI记忆 → 智能索引 → 语义搜索 → 结果展示
```

## 🚀 快速开始

### 1. 环境准备

本项目使用 [uv](https://astral.sh/blog/uv) 作为Python包管理工具：

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或在Windows上
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 项目设置

```bash
# 克隆项目
git clone https://github.com/your-username/re-call.ai.git
cd re-call.ai

# 创建虚拟环境
uv venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate
# 或 (macOS/Linux)
source .venv/bin/activate

# 安装依赖
uv pip install -e .
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# mem0配置
MEM0_API_KEY=m0-your-api-key-here

# OpenAI配置（语音转文本）
OPENAI_API_KEY=sk-your-openai-key

# JWT密钥
JWT_SECRET_KEY=your-secret-key
```

### 4. 运行项目

```bash
# 启动开发服务器
cd re-call-backend
uvicorn app.main:app --reload

# 或运行测试
pytest tests/
```

### 5. 验证安装

访问 http://localhost:8000/docs 查看API文档

## 🧪 功能验证

项目包含完整的mem0集成测试：

```bash
# 运行mem0功能验证
python test_mem0_full_validation.py

# 运行简单测试  
python test_mem0_simple.py
```

## 📚 文档结构

```
docs/
├── re-call_tech_arch.md          # 技术架构设计
├── product.md                    # 产品说明文档
├── development_progress_tracker.md # 开发进度跟踪
├── backend_tech_doc.md           # 后端技术文档
├── mem0_evaluation_report.md     # mem0评估报告
├── market_research.md            # 市场调研
└── user_scenarios.md             # 用户场景分析
```

## 🎯 开发计划

### MVP版本 (v1.0)
- [x] mem0 AI记忆服务集成
- [x] 基础API框架搭建
- [ ] 文本记录和搜索功能
- [ ] 用户认证系统
- [ ] Web界面开发

### 增强版本 (v1.1)  
- [ ] 语音输入支持
- [ ] 高级搜索过滤
- [ ] 记忆分类管理
- [ ] 性能优化

### 专业版本 (v1.2)
- [ ] 智能推荐系统
- [ ] 批量操作
- [ ] 数据导入导出
- [ ] API开放平台

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔗 相关链接

- [mem0 Platform](https://mem0.ai/) - 核心AI记忆服务
- [FastAPI 文档](https://fastapi.tiangolo.com/) - API框架
- [OpenAI Whisper](https://openai.com/research/whisper) - 语音转文本
- [uv 包管理器](https://astral.sh/blog/uv) - Python包管理

---

**项目状态**: 🚧 开发中 | **最后更新**: 2024年12月 