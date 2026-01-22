# 📚 Mindflow 技术栈学习计划

> **更新日期**: 2026-01-18  
> **当前阶段**: Phase 1 准备

---

## 🎯 学习目标

掌握 Mindflow 开发所需的核心技术,按 Phase 分阶段学习。

---

## 📋 Phase 1: 核心知识库 (Week 1-6)

### 必学技术

#### 1. 图数据库

**NetworkX** (开发环境)
- 基础概念: 节点、边、属性
- 图的创建和操作
- 图遍历算法
- 图的序列化和持久化

**学习资源**:
- 官方文档: https://networkx.org/documentation/stable/
- 教程: NetworkX Tutorial (1-2天)

**Neo4j** (生产环境,可选)
- Cypher 查询语言
- 图模式设计
- 索引和性能优化

**学习资源**:
- 官方文档: https://neo4j.com/docs/
- 在线课程: Neo4j Graph Academy (3-5天)

---

#### 2. 向量搜索

**Chroma**
- 向量数据库基础
- Embedding 和索引
- 相似度搜索
- 元数据过滤

**学习资源**:
- 官方文档: https://docs.trychroma.com/
- 快速开始: Chroma Quickstart (1天)

**sentence-transformers**
- 文本向量化
- 预训练模型选择
- 相似度计算

**学习资源**:
- 官方文档: https://www.sbert.net/
- 教程: Sentence Transformers Tutorial (1-2天)

---

#### 3. LLM 集成

**Anthropic Claude API**
- API 基础使用
- Prompt 工程
- Tool Calling
- 错误处理

**学习资源**:
- 官方文档: https://docs.anthropic.com/
- API 参考: Claude API Reference (2-3天)

**OpenAI API** (备选)
- GPT-4 API 使用
- Function Calling
- 流式响应

---

#### 4. Python 核心库

**Pydantic**
- 数据验证
- 模型定义
- 序列化/反序列化

**学习资源**:
- 官方文档: https://docs.pydantic.dev/
- 教程: Pydantic Tutorial (1天)

---

### 学习计划 (Week 1-2)

**Week 1**:
- Day 1-2: NetworkX 基础
- Day 3-4: Chroma + sentence-transformers
- Day 5: Pydantic

**Week 2**:
- Day 1-3: Claude API
- Day 4-5: 综合练习 (小型 demo)

---

## 📋 Phase 2: 输入输出层 (Week 7-12)

### 必学技术

#### 1. LLM 应用开发

**LangChain** (可选)
- Agent 框架
- Memory 管理
- Chain 组合

**学习资源**:
- 官方文档: https://python.langchain.com/
- 教程: LangChain Tutorials (3-5天)

---

#### 2. 异步编程

**asyncio**
- 异步基础
- 并发执行
- 错误处理

**学习资源**:
- Python 官方文档: asyncio
- 教程: Async Python (2-3天)

---

### 学习计划 (Week 7-8)

**Week 7**:
- Day 1-3: LangChain 基础
- Day 4-5: asyncio

**Week 8**:
- Day 1-5: 综合练习

---

## 📋 Phase 3: 自我演化 (Week 13-18)

### 必学技术

#### 1. 代码分析

**AST (Abstract Syntax Tree)**
- Python AST 模块
- 代码解析
- 模式识别

**学习资源**:
- Python 官方文档: ast module
- 教程: Python AST Tutorial (2-3天)

---

#### 2. 机器学习基础 (可选)

**模式识别**
- 聚类算法
- 相似度计算
- 特征提取

**学习资源**:
- scikit-learn 文档
- 教程: ML Basics (3-5天)

---

## 📋 Phase 4-5: UI 和生产 (Week 19-24)

### 必学技术

#### 1. 前端框架

**Gradio**
- 快速 UI 构建
- 组件使用
- 事件处理

**学习资源**:
- 官方文档: https://www.gradio.app/docs/
- 教程: Gradio Quickstart (1-2天)

**Tauri** (可选,桌面应用)
- Rust + Web 技术
- 跨平台打包

---

#### 2. 测试和部署

**pytest**
- 单元测试
- 集成测试
- Mock 和 Fixture

**学习资源**:
- 官方文档: https://docs.pytest.org/
- 教程: pytest Tutorial (2-3天)

**Docker** (可选)
- 容器化
- 部署

---

## 🎓 推荐学习顺序

### 立即开始 (Phase 1 准备)
1. NetworkX (2天)
2. Chroma + sentence-transformers (2天)
3. Claude API (3天)
4. Pydantic (1天)

### 按需学习
- Neo4j: 当 NetworkX 性能不足时
- LangChain: 当需要更复杂的 Agent 逻辑时
- AST: Phase 3 开始前学习

---

## 📚 额外资源

### 书籍
- 《Designing Data-Intensive Applications》- 数据系统设计
- 《Building LLM Apps》- LLM 应用开发

### 课程
- DeepLearning.AI: LangChain for LLM Application Development
- Fast.ai: Practical Deep Learning

### 社区
- LangChain Discord
- Chroma Discord
- r/LocalLLaMA

---

## ✅ 学习检查清单

### Phase 1 必备技能
- [ ] 能用 NetworkX 创建和查询图
- [ ] 能用 Chroma 进行向量搜索
- [ ] 能调用 Claude API 并处理响应
- [ ] 能用 Pydantic 定义数据模型

### Phase 2 必备技能
- [ ] 能实现基础的 LLM Agent
- [ ] 能处理异步任务
- [ ] 能实现 Tool Calling

### Phase 3 必备技能
- [ ] 能解析 Python 代码
- [ ] 能识别代码模式
- [ ] 能实现自动化工作流

---

**最后更新**: 2026-01-18  
**维护者**: [@damiangao](https://github.com/damiangao)
