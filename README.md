# Mindflow - Personal AI Assistant

🧠 **心流（Mindflow）** 是一个个人AI助理系统，帮助你记录生活、规划目标、进行每日复盘。

## ✨ 核心特性

- **生活记录**：通过对话式输入自动提取和分类生活事件
- **计划管理**：创建、跟踪和推动目标达成
- **每日复盘**：4层递进式提示，引导深度反思
- **用户画像**：系统逐步学习你的特征，提供个性化帮助
- **灵活的LLM支持**：支持Claude、OpenAI、DeepSeek等多个LLM提供商快速切换

## 🚀 快速开始

### 前置要求

- Python 3.9+
- pip 或 conda
- Claude API密钥（从 [Anthropic](https://console.anthropic.com/) 获取）

### 安装方式

#### 方式1：本地开发环境

1. **克隆项目并进入目录**
```bash
cd mindflow
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
nano .env  # 或使用你喜欢的编辑器
```

5. **运行应用**
```bash
python -m src.ui.main
```

访问 `http://localhost:7860` 在浏览器打开应用。

#### 方式2：使用 Docker

1. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件
```

2. **构建并运行 Docker 容器**
```bash
docker-compose up -d
```

3. **查看日志**
```bash
docker-compose logs -f mindflow
```

4. **访问应用**
```
http://localhost:7860
```

## 📋 项目结构

```
mindflow/
├── src/
│   ├── ui/              # Gradio Web应用
│   │   └── main.py      # 应用入口
│   ├── llm/             # LLM配置和提供商
│   │   ├── provider.py  # 抽象基类
│   │   ├── claude.py    # Claude实现
│   │   └── config.py    # LLM配置管理
│   ├── database/        # 数据库相关
│   │   ├── models.py    # SQLAlchemy ORM模型
│   │   └── connection.py # 数据库连接
│   ├── agents/          # LangGraph Agent（Phase 2+）
│   ├── services/        # 业务逻辑服务（Phase 2+）
│   └── config.py        # 全局配置
├── tests/               # 测试文件
├── data/                # 数据存储（SQLite数据库）
├── logs/                # 应用日志
├── requirements.txt     # Python依赖
├── .env.example        # 环境变量示例
├── Dockerfile          # Docker配置
└── docker-compose.yml  # Docker Compose配置
```

## 🔧 配置

### LLM 提供商配置

编辑 `.env` 文件选择你的LLM提供商：

```env
# 选择提供商：claude, openai, deepseek, ollama
LLM_PROVIDER=claude

# Claude 配置
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

### 数据库配置

默认使用SQLite（无需额外配置），所有数据保存在 `data/mindflow.db`

```env
DATABASE_URL=sqlite:///./data/mindflow.db
```

### Gradio 配置

```env
GRADIO_HOST=0.0.0.0
GRADIO_PORT=7860
GRADIO_SHARE=false  # 是否生成公开链接
```

## 📱 使用指南

### 1. 生活记录

- 在"生活记录"标签页输入今天发生的事件
- 系统会自动识别和分类事件
- 支持编辑、删除事件

### 2. 计划管理

- 创建新计划：设定目标、截止日期、优先级
- 跟踪进度：定期更新计划进度
- 查看关联：查看与事件的关联分析

### 3. 每日复盘

- 点击"开始复盘"按钮
- 逐层回答4层递进式问题
- 系统保存复盘内容并学习你的特征

### 4. 用户画像

- 查看系统学习到的你的特征
- 包括行动力、思维方式、学习风格等
- 系统会随着使用逐步完善理解

## 🧪 开发和测试

### 运行测试

```bash
pytest tests/
```

### 代码格式检查

```bash
black src/
flake8 src/
mypy src/
```

## 🔐 隐私和安全

- ✅ 所有数据存储在本地，不经过第三方服务
- ✅ 支持本地LLM（Ollama）以实现完全隐私
- ✅ 清晰的隐私政策和数据管理
- ✅ 数据导出和删除功能

## 📚 项目文档

详细文档请查看：

- **架构设计** → `docs/ARCHITECTURE.md`
- **开发指南** → `docs/DEVELOPMENT.md`
- **数据库设计** → `docs/DATABASE.md`
- **LLM配置** → `docs/LLM_CONFIG.md`
- **部署指南** → `docs/DEPLOYMENT.md`
- **项目规划** → `PLAN.md`（本地参考）

## 🚦 开发阶段

### Phase 1：基础框架搭建 ✅ 进行中

- [x] 项目结构初始化
- [x] Gradio应用框架
- [x] LLM配置层
- [x] 数据库模型定义
- [x] Docker配置
- [ ] 功能测试和验证

### Phase 2：生活记录系统 ⏳

- [ ] 对话界面开发
- [ ] 事件提取Agent
- [ ] 用户画像初始化
- [ ] 事件管理功能

### Phase 3-6：待实现

详见 `PLAN.md` 第 "6个开发Phase" 部分

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📞 支持

如有问题，请：

1. 查看 `docs/` 目录中的相关文档
2. 检查 `.env` 配置是否正确
3. 查看应用日志：`logs/mindflow.log`
4. 提交 Issue 或讨论

---

**构建日期**: 2024-12-03
**版本**: Phase 1 (v1.0-dev)
**维护者**: Mindflow Team

祝你使用愉快！🎉
