# 🚀 re-call.ai MVP 快速启动指南

## 📋 5分钟启动MVP

### 1. 获取API密钥

#### mem0 (必需)
```bash
# 访问 https://mem0.ai/
# 注册账号，获取API密钥
MEM0_API_KEY=m0-xxxxxxxx
```

#### Supabase (必需，用于认证)
```bash
# 访问 https://supabase.com/
# 创建新项目，获取URL和Key
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyxxx
```

### 2. 安装和配置

```bash
# 安装依赖
uv pip install -e .

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，填入API密钥

# 启动服务
uvicorn app.main:app --reload --port 8080
```

### 3. 测试API

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
# 浏览器访问：http://localhost:8000/docs

# 注册用户
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# 用户登录
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

## 🎯 MVP架构

```
用户 → FastAPI → Supabase Auth → mem0 Platform
                     ↓               ↓
               用户认证管理      AI记忆存储/搜索
```

## ✅ 为什么选择这个组合？

### Supabase Auth 优势
- ✅ **2分钟集成** - 比JWT快10倍
- ✅ **零维护** - 不用管密码哈希、token刷新
- ✅ **免费额度** - 50,000用户免费
- ✅ **安全性** - 企业级安全标准

### mem0 Platform 优势  
- ✅ **AI智能** - 自动记忆管理
- ✅ **语义搜索** - 智能检索
- ✅ **简单集成** - 几行代码搞定

## 🔄 下一步开发

1. **记忆管理API** - 基于mem0的CRUD操作
2. **前端界面** - Next.js + Tailwind
3. **语音输入** - 集成Whisper API

---

**总开发时间**: 1-2天完成MVP  
**vs JWT方案**: 节省3-5天开发时间 