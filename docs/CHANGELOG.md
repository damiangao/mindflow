# 📝 更新日志 (CHANGELOG)

> 记录 Mindflow 项目的所有重要变更

---

## [Unreleased] - 2026-01-16

### 🎉 项目重大升级

#### 定位变更
- **从**: 个人 AI 助理
- **到**: 智能体操作系统（Agent OS）

#### 架构升级
- 采用三层架构（应用层/服务层/底层能力）
- 借鉴 Goose 的 Extension 系统设计
- 支持插件化扩展和应用生态

---

## [2026-01-16] - 文档整合

### Added
- ✅ 创建 `README.md` - 项目整体介绍
  - 项目简介和核心特点
  - 竞品分析表格
  - 文档索引
  - 开发进度
  - 贡献指南

- ✅ 整合 `docs/LEARNING.md` - 技术栈学习计划
  - 从 `TECH_STACK_LEARNING.md` 移动
  - 3个学习阶段
  - 详细学习路线

- ✅ 创建 `docs/CHANGELOG.md` - 本文档
  - 记录所有重要变更
  - 版本历史

### Changed
- 📝 简化文档结构，只保留4个核心文档
  - README.md（项目介绍）
  - docs/DEVELOPMENT.md（开发计划）
  - docs/LEARNING.md（学习计划）
  - docs/CHANGELOG.md（更新日志）

### Removed
- ❌ 删除冗余文档
  - COMPETITOR_ANALYSIS.md（整合到 README）
  - CROSS_PLATFORM.md（整合到 DEVELOPMENT）
  - DATA_MIGRATION.md（整合到 DEVELOPMENT）
  - DIFFERENTIATION_STRATEGY.md（整合到 README）
  - KNOWLEDGE_BASE_DESIGN.md（整合到 DEVELOPMENT）
  - UPDATE_SUMMARY.md（替换为 CHANGELOG）

---

## [2026-01-15] - 架构设计和竞品分析

### Added
- ✅ 完成竞品分析（DeepSeek）
  - 分析 6 个直接/间接竞品
  - 市场空白分析
  - 差异化策略制定

- ✅ 创建开发计划 v2.0
  - 6 个 Phase 开发路线图
  - 预计 12-16 周完成
  - 详细任务清单

- ✅ 跨平台支持设计
  - Windows、macOS、Linux
  - 未来支持 Android、iOS
  - 平台特定数据目录

- ✅ 数据迁移方案
  - 本地导出/导入（Phase 1）
  - 云端同步（Phase 5，可选）
  - 跨平台兼容

- ✅ 知识库设计
  - 向量数据库（Phase 3）
  - 知识图谱（Phase 5，可选）
  - 混合方案

### Changed
- 📝 项目定位从"个人助理"升级为"智能体操作系统"
- 🏗️ 架构从单体应用升级为三层架构
- 🔌 引入 Extension 插件系统

---

## [2026-01-15] - 初始规划

### Added
- ✅ 创建项目仓库
- ✅ 初始文档结构
  - ARCHITECTURE.md
  - DATABASE.md
  - DEPLOYMENT.md
  - DEVELOPMENT.md
  - LLM_CONFIG.md

- ✅ 技术栈选型
  - Python + Gradio
  - LangGraph + Claude API
  - SQLite + SQLAlchemy

---

## 版本说明

### 版本号规则
- **Major.Minor.Patch** (例如: 1.0.0)
- **Major**: 重大架构变更
- **Minor**: 新功能添加
- **Patch**: Bug 修复和小改进

### 当前版本
- **v0.1.0-alpha** - 规划阶段

### 计划版本
- **v0.2.0-alpha** - Phase 0 完成（架构设计）
- **v0.3.0-alpha** - Phase 1 完成（Extension 系统）
- **v0.5.0-beta** - Phase 3 完成（核心应用）
- **v1.0.0** - Phase 6 完成（生产就绪）

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

**最后更新**: 2026-01-16  
**格式**: [Keep a Changelog](https://keepachangelog.com/)  
**版本**: [Semantic Versioning](https://semver.org/)
