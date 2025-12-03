# Mindflow 系统架构设计

## 项目概述

**Mindflow** 是一个个人AI助理系统，帮助用户记录生活、管理计划、进行定期复盘。核心特点是能够逐步学习用户特征，提供个性化的帮助。

## 核心设计原则

- **隐私优先**：所有数据本地存储，支持自建服务器部署
- **个性化**：系统逐步了解用户，提供定制化帮助
- **模块化**：各功能相对独立，便于维护和扩展
- **简洁高效**：技术栈精简，易于理解和部署

## 系统架构概览

```
┌─────────────────────────────────────┐
│  Gradio 前端 (Web UI)                │
│  - PC/移动端响应式界面               │
│  - 对话、计划、复盘等UI组件          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  后端服务层 (Services)               │
│  - 事件管理                          │
│  - 计划管理                          │
│  - 复盘管理                          │
│  - 用户画像管理                      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  LangGraph Agent 工作流              │
│  - 事件提取Agent                     │
│  - 用户画像Agent                     │
│  - 计划推动Agent                     │
│  - 复盘生成Agent                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  数据层                              │
│  - SQLite数据库                      │
│  - 文件存储                          │
│  - 外部API集成(LLM)                 │
└─────────────────────────────────────┘
```

## 核心功能模块

### 1. 生活记录系统

**功能**：通过对话记录用户的日常生活事件

- 对话式输入：自然流畅的交互方式
- 自动提取：LLM自动从对话中识别和提取事件
- 自动分类：事件分类（工作、学习、生活、健康、个人等）
- 事件管理：查看、编辑、删除事件

### 2. 计划管理系统

**功能**：帮助用户设定目标并持续推动进度

- 计划创建：用户定义目标和截止日期
- 进度跟踪：百分比表示、状态管理（活跃、完成、存档）
- 智能推动：基于用户画像的个性化督促建议
- 关联分析：连接生活事件和计划进度

### 3. 每日复盘系统

**功能**：帮助用户总结反思，持续改进

- 个性化提示：4层递进式的复盘引导
  - 基础框架提示（固定）
  - 事件相关提示（动态）
  - 计划相关提示（动态）
  - 用户画像驱动提示（个性化）
- 记录保存：复盘内容持久化存储
- 历史查看：按时间查看过去的复盘

### 4. 用户画像系统

**功能**：系统逐步了解用户，提供个性化帮助

- 初始档案：首次使用时的用户问卷
- 行为特征：从交互中学习用户的习惯和偏好
- 特征库：带置信度的用户特征数据
- 个性化应用：根据画像调整提示风格和强度

## 技术栈

### 前端
- **Gradio**: 快速构建Web UI，自动生成响应式界面

### 后端
- **LangGraph**: AI Agent工作流定义和执行
- **SQLAlchemy**: ORM数据库操作
- **Pydantic**: 数据验证

### LLM与AI
- **主要方案**：Claude API (Haiku 4.5 - 成本优化)
- **备选方案**：GPT-4o mini, DeepSeek (可快速切换)
- **本地选项**：Ollama (隐私优先)
- **特点**：通过环境变量支持LLM快速切换，业务逻辑不受影响

### 数据存储
- **SQLite**: MVP阶段足够，简单快速
- 支持后续升级到PostgreSQL

### 任务调度
- **APScheduler**: 定时任务（每日复盘提醒、计划推动提醒等）

### 部署
- **Docker**: 容器化部署
- **Linux服务管理**: Systemd或类似工具

## 数据库设计

### 核心表结构

#### 用户档案表
```sql
CREATE TABLE user_profile (
    id TEXT PRIMARY KEY,
    user_id TEXT,  -- 预留多用户隔离
    name TEXT,
    goals TEXT,  -- JSON
    values TEXT,  -- JSON
    work_direction TEXT,
    personality_traits TEXT,  -- JSON
    weak_points TEXT,  -- JSON
    preferred_reminder_style TEXT,
    timezone TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### 用户行为特征库
```sql
CREATE TABLE user_behavior_features (
    id TEXT PRIMARY KEY,
    feature_key TEXT,
    feature_value TEXT,  -- JSON
    confidence FLOAT,  -- 置信度 0-1
    last_updated TIMESTAMP
);
```

#### 生活事件表
```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    title TEXT,
    description TEXT,
    category TEXT,  -- work/learning/life/health/personal
    date TIMESTAMP,
    importance INTEGER,
    related_plan_ids TEXT,  -- JSON
    created_at TIMESTAMP
);
```

#### 计划表
```sql
CREATE TABLE plans (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    title TEXT,
    description TEXT,
    status TEXT,  -- active/completed/archived
    priority INTEGER,
    start_date TIMESTAMP,
    due_date TIMESTAMP,
    progress_percentage INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### 复盘记录表
```sql
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    review_date DATE,
    content TEXT,
    ai_suggestions TEXT,
    related_event_ids TEXT,  -- JSON
    related_plan_ids TEXT,  -- JSON
    mood_rating INTEGER,  -- 1-5
    created_at TIMESTAMP
);
```

#### 对话历史表（用于学习）
```sql
CREATE TABLE conversation_history (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    user_message TEXT,
    ai_response TEXT,
    extracted_event_id TEXT,
    conversation_type TEXT,
    timestamp TIMESTAMP
);
```

### 数据关系图

```
user_profile ── (1:N) ──→ events
    ├── (1:N) ──→ plans
    ├── (1:N) ──→ reviews
    ├── (1:N) ──→ conversation_history
    └── (1:N) ──→ user_behavior_features

events ────── (M:1) ─→ plans
plans ─────── (1:N) ─→ plan_updates
reviews ───── (M:1) ─→ events
reviews ───── (M:1) ─→ plans
```

## 架构特点

### 1. LLM灵活配置

所有LLM调用通过统一的配置层，支持快速切换：

```python
# 通过环境变量切换
LLM_PROVIDER=claude  # 或 openai, deepseek, ollama
CLAUDE_API_KEY=...
```

**优势**：
- 业务逻辑与LLM提供商完全解耦
- 支持多个LLM并行配置
- 可在运行时动态切换
- 便于成本优化和隐私权衡

### 2. 用户隔离架构

虽然MVP是单用户系统，但设计中预留了多用户扩展：

- 所有表都包含 `user_id` 字段
- 所有查询都显式过滤 `user_id`
- 无需重构核心逻辑即可支持多用户

**迁移到多用户的步骤**：
1. 添加认证层和用户管理表
2. 实现会话管理和用户上下文
3. 更新配置以读取当前用户ID
4. 无需修改业务逻辑即可支持多用户

### 3. Agent驱动架构

使用LangGraph实现四个核心Agent：

1. **事件提取Agent**：从对话中识别事件
2. **用户画像Agent**：学习用户特征
3. **计划推动Agent**：生成督促建议
4. **复盘生成Agent**：生成个性化复盘提示

**优势**：
- 清晰的职责划分
- 易于独立测试
- 支持未来的扩展和改进

## 核心工作流

### 生活记录工作流
```
用户输入消息
    ↓
事件提取Agent分析
    ↓
提取事件并分类
    ↓
用户画像Agent学习特征
    ↓
保存事件和更新用户特征
```

### 每日复盘工作流
```
用户选择复盘
    ↓
系统检索该日事件和计划
    ↓
生成4层复盘提示
    ↓
用户填写复盘内容
    ↓
保存复盘并优化用户画像
```

### 计划推动工作流
```
定时触发（每日）
    ↓
计划推动Agent检查计划进度
    ↓
基于用户画像生成督促建议
    ↓
推送提醒给用户
```

## 开发优先级

### MVP核心（必须做）
1. 生活记录系统
2. 计划管理系统
3. 每日复盘系统
4. 用户画像初始化和学习

### 后续扩展（可选）
- 多模态输入（语音、图片）
- 知识库管理（多模态、向量检索）
- 多用户支持和认证
- 高级分析和推荐
- 外部应用集成

## 部署架构

```
用户的Linux服务器
    ├── Docker容器
    │   ├── Gradio应用
    │   └── Python后端
    ├── SQLite数据库
    └── 环境配置 (.env)
```

**部署方式**：
- 通过Docker Compose快速部署
- 支持固定IP访问
- 所有数据本地存储
- 支持本地备份

## 设计决策

### 为什么选择Gradio？
- 快速搭建Web UI
- 自动生成响应式界面（PC和移动端）
- 简化前后端集成
- 学习曲线平缓

### 为什么选择LangGraph？
- 强大的Agent工作流能力
- 清晰的状态管理
- 支持复杂的多步骤流程
- 与LLM API无缝集成

### 为什么选择SQLite？
- MVP阶段足够
- 零配置，易于部署
- 无需服务器
- 支持后续升级到PostgreSQL

### 为什么采用Agent架构？
- 清晰的职责划分
- 易于测试和维护
- 支持独立演进
- 便于添加新功能

## 安全和隐私

- **数据本地存储**：所有用户数据存储在自建服务器
- **无云同步**：数据不上传到任何云服务
- **API隐私**：支持本地LLM（Ollama）以保护隐私
- **配置灵活性**：可根据需求选择不同的LLM提供商

## 扩展性考虑

该架构设计考虑了以下扩展方向：

1. **多用户支持**：通过user_id隔离，无需重构核心代码
2. **多模态输入**：Agent架构支持添加新的输入处理
3. **知识库集成**：预留接口支持向量检索集成
4. **通知系统**：模块化的提醒机制支持多种通知方式
5. **高级分析**：用户行为特征库支持统计分析和推荐

---

更多详情请查看：
- [开发计划](DEVELOPMENT.md)
- [数据库schema](DATABASE.md)
- [LLM配置](LLM_CONFIG.md)
