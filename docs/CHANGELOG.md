# 📝 更新日志 (CHANGELOG)

> 记录 Mindflow 项目的所有重要变更

---

## [0.3.1-alpha] - 2026-01-28

### 🎯 VectorStore 优化 - 简化技术栈

#### 核心改进
- ✅ **移除直接依赖**: 不再单独安装 sentence-transformers
- ✅ **使用 Chroma 内置**: 通过 `embedding_functions.SentenceTransformerEmbeddingFunction`
- ✅ **多语言支持**: 默认使用 `paraphrase-multilingual-MiniLM-L12-v2` (支持中文)
- ✅ **代码简化**: 减少 20% 代码量，自动管理嵌入向量

#### 文档更新
- ✅ 新增 `docs/VECTOR_STORE_OPTIMIZATION.md` - 优化说明文档
- ✅ 更新所有相关文档中的技术栈描述
- ✅ 新增学习资料 `learning/chroma/day4_sentence_transformers_integration.md`

## [0.3.0-alpha] - 2026-01-22

### 🎉 Week 1 完成 - 核心知识库实现

#### 核心功能
- ✅ **三层数据模型**: Methodology / Skill / Artifact (Pydantic)
- ✅ **图数据库**: NetworkX 实现，JSON 持久化
- ✅ **向量索引**: Chroma (内置 sentence-transformers)
- ✅ **统一接口**: KnowledgeBase 封装所有操作

#### Artifact 优化 (重要改进)
- ✅ **轻量化设计**: `summary` (语义索引) + `filepath` (文件路径)
- ✅ **文件持久化**: artifacts/ 目录存储实际代码
- ✅ **可复用性**: 代码文件可直接导入执行
- ✅ **向量搜索**: Artifact 独立索引，支持语义检索

#### 测试验证
- ✅ 功能测试通过 (test_kb_en.py)
- ✅ 端到端测试通过 (test_e2e.py)
- ✅ Artifact 持久化测试通过 (test_artifact.py)

#### 技术细节
```python
# Artifact 最终设计
class Artifact:
    summary: str    # 文档总结（用于向量索引）
    filepath: str   # 文件路径（指向实际文件）
```

---

## [Unreleased] - 2026-01-18

### 🎉 架构设计完成

#### 核心架构确定
- **操作系统抽象**: 输入 + 输出 + 资源调度
- **知识库三层结构**: 方法论 → Skills → 副产品
- **DAG 结构**: 允许多父节点,灵活关联

#### 核心机制设计
- ✅ **关联机制**: 静态(图数据库) + 动态(向量搜索)
- ✅ **方法论评分**: 加权归一化机制
- ✅ **Skills 组合**: 规划式 HTN Planning
- ✅ **用户交互**: 三级策略(静默/队列/立即)
- ✅ **查询流程**: 渐进式设计(Phase 1 MVP → Phase 2 按需)
- ✅ **Skills 调用**: 混合模式(instructions + called_skills)

#### 文档新增
- ✅ `docs/ARCHITECTURE.md` v1.0 - 核心架构设计
- ✅ `docs/ARCHITECTURE_DISCUSSION.md` v1.1 - 架构讨论纪要
- ✅ `docs/TECHNICAL_DESIGN.md` v1.1 - 技术实现方案

#### 冷启动设计
- ✅ 方法论层: 5个核心方法论
- ✅ Skills 层: 15-20个精简 Skills
  - 生活管理 (6个)
  - 数据处理 (6个)
  - 代码辅助 (3个)
  - 通用工具 (2个)

#### 技术栈确定
- **图数据库**: Neo4j(生产) / NetworkX(开发)
- **向量搜索**: Chroma (内置 sentence-transformers)
- **LLM**: Claude / GPT / DeepSeek

#### 关键决策
1. 不过度设计,先简单实现再优化
2. 向量搜索优先,图查询按需加入
3. Skills 调用用混合模式
4. 种子库精简,从使用中学习是核心

---

## [2026-01-16] - 文档整合

### Added
- ✅ 创建 `README.md` - 项目整体介绍
- ✅ 整合 `docs/LEARNING.md` - 技术栈学习计划
- ✅ 创建 `docs/CHANGELOG.md` - 本文档

### Changed
- 📝 简化文档结构,只保留核心文档
- 🏗️ 项目定位升级为"智能体操作系统"

### Removed
- ❌ 删除冗余文档,整合到核心文档

---

## [2026-01-15] - 架构设计和竞品分析

### Added
- ✅ 完成竞品分析
- ✅ 创建开发计划 v2.0
- ✅ 跨平台支持设计
- ✅ 数据迁移方案
- ✅ 知识库设计

### Changed
- 📝 项目定位从"个人助理"升级为"智能体操作系统"
- 🏗️ 架构从单体应用升级为三层架构

---

## [2026-01-15] - 初始规划

### Added
- ✅ 创建项目仓库
- ✅ 初始文档结构
- ✅ 技术栈选型

---

## 版本说明

### 版本号规则
- **Major.Minor.Patch** (例如: 1.0.0)
- **Major**: 重大架构变更
- **Minor**: 新功能添加
- **Patch**: Bug 修复和小改进

### 当前版本
- **v0.2.0-alpha** - 架构设计完成

### 计划版本
- **v0.3.0-alpha** - Phase 1 完成(核心知识库)
- **v0.5.0-beta** - Phase 3 完成(自我演化)
- **v1.0.0** - 生产就绪

---

## 变更类型说明

- **Added**: 新增功能
- **Changed**: 功能变更
- **Deprecated**: 即将废弃的功能
- **Removed**: 已删除的功能
- **Fixed**: Bug 修复
- **Security**: 安全相关更新

---

## 贡献者

- [@damiangao](https://github.com/damiangao) - 项目创建者

---

**最后更新**: 2026-01-18  
**格式**: [Keep a Changelog](https://keepachangelog.com/)  
**版本**: [Semantic Versioning](https://semver.org/)
