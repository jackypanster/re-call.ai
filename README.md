# re-call.ai 项目简介

## 项目目的与意义

re-call.ai（SuperMemory）旨在打造一个基于大语言模型（LLM）的个人第二大脑系统，帮助用户：
- 快速记录生活与工作的片段
- 自动完成信息摘要与智能分类
- 实现高效的语义搜索与记忆回溯
- 保护数据隐私，提升个人知识管理与回顾体验

本项目聚焦于极简、智能、可扩展的后端架构，采用 FastAPI、Supabase、Supermemory.ai、OpenRouter 等现代云服务，快速实现 MVP 并支持后续演进。

## 快速部署与运行

本项目推荐使用 [uv](https://astral.sh/blog/uv) 作为 Python 虚拟环境与依赖管理工具，uv 是一个极快、现代化的 Python 包和虚拟环境管理器，能大幅提升开发体验。

### 1. 安装 uv

- Windows:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- macOS/Linux:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- 或使用 pip：
  ```bash
  pip install uv
  ```

### 2. 创建并激活虚拟环境
```bash
uv venv
uv venv activate
```

### 3. 安装依赖
```bash
uv pip install -r supermemory-backend/requirements.txt
uv pip install -r supermemory-backend/dev-requirements.txt
```

### 4. 配置环境变量
复制 `supermemory-backend/.env.example` 为 `supermemory-backend/.env`，并根据实际填写。

### 5. 启动开发服务器
```bash
cd supermemory-backend
uvicorn app.main:app --reload
```

### 6. 运行测试
```bash
pytest
```

## 参考
- [uv 官方文档](https://astral.sh/blog/uv)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Supermemory.ai](https://docs.supermemory.ai/)
- [Supabase](https://supabase.com/)

---

如需详细技术文档、产品说明和开发进度，请参见 `docs/` 目录。 