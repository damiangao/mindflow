# Mindflow 文档

欢迎查看Mindflow的完整文档。本文件夹包含关于系统架构、开发、配置和部署的详细信息。

## 文档导航

### 🏗️ 核心文档

#### [ARCHITECTURE.md](ARCHITECTURE.md)
**系统设计和技术架构**
- 系统架构概览和核心设计原则
- 四个核心功能模块（生活记录、计划管理、复盘、用户画像）
- 完整的数据库模式和SQL示例
- 四个LangGraph Agent的设计
- 工作流程和交互流程图
- 安全和隐私考虑

**适合阅读**：架构师、技术负责人、想要理解系统整体设计的开发者

#### [DEVELOPMENT.md](DEVELOPMENT.md)
**开发指南和阶段规划**
- 6个开发阶段的详细规划（Phase 1-6）
- 每个阶段的具体任务和检查清单
- MVP范围定义（包含和不包含的功能）
- 开发最佳实践和代码组织
- 技术决策说明
- 常见问题解答

**适合阅读**：开发团队、项目经理、参与开发的人员

#### [DATABASE.md](DATABASE.md)
**数据库设计详解**
- 7个核心表的完整定义和字段说明
- 数据关系图和关系模式
- 数据示例（JSON格式）
- 性能优化策略和索引设计
- SQLite到PostgreSQL的升级路径
- 多用户支持的架构预留
- 备份和恢复方案

**适合阅读**：后端开发者、DBA、需要理解数据结构的人员

#### [LLM_CONFIG.md](LLM_CONFIG.md)
**LLM灵活配置指南**
- 支持的LLM提供商（Claude、OpenAI、DeepSeek、Ollama）
- 每个提供商的优势和使用场景
- 完整的环境变量配置示例
- LLM提供商实现架构
- 成本估算和性能对比
- API密钥管理安全建议
- 快速切换和故障排除指南

**适合阅读**：所有开发者、需要配置LLM的用户、想要降低成本的运维人员

#### [DEPLOYMENT.md](DEPLOYMENT.md)
**生产部署指南**
- 详细的系统要求和前置条件
- 完整的部署步骤（Step 1-6）
- Docker和Docker Compose配置
- 远程访问和反向代理配置
- HTTPS和安全证书配置
- 自动备份和恢复方案
- 定期维护和监控
- 故障排除指南
- 安全最佳实践

**适合阅读**：运维人员、系统管理员、需要部署系统的用户

---

## 快速导航

### 我是...

#### 🎯 想快速了解系统的人
1. 首先阅读 [ARCHITECTURE.md](ARCHITECTURE.md) 的概览部分
2. 查看系统架构图和核心功能模块
3. 浏览工作流程图

#### 👨‍💻 参与开发的工程师
1. 查看 [DEVELOPMENT.md](DEVELOPMENT.md) 的项目开发概览
2. 了解你要负责的开发阶段
3. 查看数据库设计：[DATABASE.md](DATABASE.md)
4. 理解LLM配置：[LLM_CONFIG.md](LLM_CONFIG.md)

#### 🏗️ 系统架构师
1. 深入阅读 [ARCHITECTURE.md](ARCHITECTURE.md) 的完整内容
2. 关注用户隔离架构和可扩展性考虑
3. 查看数据库关系图：[DATABASE.md](DATABASE.md)

#### 📊 DBA或数据库管理员
1. 查看 [DATABASE.md](DATABASE.md) 的完整内容
2. 重点关注索引策略和性能优化部分
3. 了解备份和恢复方案

#### 🤖 LLM配置和成本管理
1. 阅读 [LLM_CONFIG.md](LLM_CONFIG.md) 的完整内容
2. 对比不同提供商的成本
3. 学习如何快速切换LLM

#### 🚀 部署和运维人员
1. 阅读 [DEPLOYMENT.md](DEPLOYMENT.md) 的完整内容
2. 按步骤进行部署
3. 设置监控和备份
4. 阅读安全建议部分

#### 💰 想了解系统成本的人
1. [LLM_CONFIG.md](LLM_CONFIG.md) 中的成本估算部分
2. [DEPLOYMENT.md](DEPLOYMENT.md) 中的系统要求
3. [DATABASE.md](DATABASE.md) 中的存储需求

---

## 主要概念解释

### 四个核心Agent

1. **事件提取Agent**
   - 从用户对话中识别和提取生活事件
   - 自动分类事件（工作、学习、生活、健康、个人）
   - 参考：[ARCHITECTURE.md](ARCHITECTURE.md) - 生活记录系统

2. **用户画像Agent**
   - 从交互中学习用户的特征、习惯和偏好
   - 维护用户特征库，带有置信度评分
   - 参考：[ARCHITECTURE.md](ARCHITECTURE.md) - 用户画像系统

3. **计划推动Agent**
   - 基于用户画像生成个性化的计划督促建议
   - 定时提醒用户更新计划进度
   - 参考：[ARCHITECTURE.md](ARCHITECTURE.md) - 计划管理系统

4. **复盘生成Agent**
   - 生成4层递进式的复盘提示
   - 根据用户特征提供个性化反思建议
   - 参考：[ARCHITECTURE.md](ARCHITECTURE.md) - 每日复盘系统

### 三个主要功能模块

1. **生活记录** - 通过对话自动记录日常事件
2. **计划管理** - 创建、跟踪和推动目标达成
3. **每日复盘** - 个性化的反思和总结

更多详情参考 [ARCHITECTURE.md](ARCHITECTURE.md)

### LLM灵活性

系统支持在多个LLM提供商之间快速切换，通过修改环境变量即可，无需修改代码。支持的提供商包括：
- Claude（推荐，成本优化）
- OpenAI（GPT系列）
- DeepSeek（国内友好）
- Ollama（本地隐私）

参考：[LLM_CONFIG.md](LLM_CONFIG.md)

---

## 开发阶段概览

| 阶段 | 名称 | 时间 | 主要内容 |
|------|------|------|--------|
| Phase 1 | 基础框架搭建 | 1-2周 | Gradio框架、数据库、LLM配置 |
| Phase 2 | 生活记录系统 | 2周 | 对话界面、事件提取、用户画像初始化 |
| Phase 3 | 计划管理系统 | 1.5周 | 计划CRUD、进度跟踪、计划推动Agent |
| Phase 4 | 每日复盘系统 | 1.5周 | 复盘提示生成、用户填写、历史查看 |
| Phase 5 | 用户画像深化 | 1周 | 特征优化、个性化提升、性能优化 |
| Phase 6 | 部署和扩展准备 | 1周 | Docker配置、文档、测试、扩展预留 |

详细信息参考：[DEVELOPMENT.md](DEVELOPMENT.md)

---

## 关键技术栈

- **前端UI**: Gradio（自动响应式、易部署）
- **工作流**: LangGraph（AI Agent框架）
- **数据库**: SQLite（MVP）/ PostgreSQL（生产）
- **ORM**: SQLAlchemy
- **验证**: Pydantic
- **LLM**: Claude Haiku 4.5（可切换）
- **调度**: APScheduler
- **部署**: Docker & Docker Compose
- **服务**: Systemd（Linux）

---

## 数据库架构快览

7个核心表：
1. **user_profile** - 用户基本档案
2. **user_behavior_features** - 学到的用户特征
3. **events** - 生活事件记录
4. **plans** - 用户计划/目标
5. **plan_updates** - 计划进度历史
6. **reviews** - 每日复盘记录
7. **conversation_history** - 对话历史（用于学习）

参考：[DATABASE.md](DATABASE.md)

---

## 常见问题（快速答案）

**Q: 系统如何保护隐私？**
A: 所有数据存储在用户自建的Linux服务器上，不连接任何云服务。支持本地LLM（Ollama）以完全避免数据发送到第三方。

**Q: 可以切换LLM吗？**
A: 完全可以。只需修改.env文件中的LLM_PROVIDER和相应的API密钥，重启应用即可。

**Q: 数据库可以升级吗？**
A: 当然可以。MVP使用SQLite，生产环境可以升级到PostgreSQL。数据库设计充分考虑了这一点。

**Q: 如何添加新功能？**
A: 查看 [DEVELOPMENT.md](DEVELOPMENT.md) 的"常见问题"部分了解扩展机制。

**Q: 部署需要多久？**
A: 按照 [DEPLOYMENT.md](DEPLOYMENT.md) 的步骤，通常需要30-60分钟。

**Q: 成本是多少？**
A: 主要成本来自LLM API调用。参考 [LLM_CONFIG.md](LLM_CONFIG.md) 的成本估算部分。

---

## 文件大小和更新日期

| 文件 | 大小 | 用途 |
|------|------|------|
| ARCHITECTURE.md | ~8KB | 系统设计 |
| DEVELOPMENT.md | ~12KB | 开发规划 |
| DATABASE.md | ~15KB | 数据库设计 |
| LLM_CONFIG.md | ~14KB | LLM配置 |
| DEPLOYMENT.md | ~16KB | 部署指南 |
| README.md | 本文件 | 文档导航 |

---

## 贡献和反馈

- 如发现文档错误或不清楚之处，请提交Issue
- 欢迎改进建议和补充内容
- 遵循项目的贡献指南

---

## 更多资源

### 官方文档
- [Gradio官方文档](https://gradio.app/)
- [LangGraph官方文档](https://langchain-ai.github.io/langgraph/)
- [SQLAlchemy官方文档](https://docs.sqlalchemy.org/)
- [Claude API文档](https://docs.anthropic.com/)

### 学习资源
- [AI Agent开发指南](https://www.anthropic.com/)
- [数据库设计最佳实践](https://en.wikipedia.org/wiki/Database_design)
- [Docker完全指南](https://docs.docker.com/)

### 相关项目
- LangChain - LLM应用框架
- FastAPI - Web框架（可替代Gradio）
- Pydantic - 数据验证

---

## 许可证

该项目遵循开源许可证。详见项目根目录的LICENSE文件。

---

## 最后更新

文档最后更新时间：2024年

持续维护和改进中...
