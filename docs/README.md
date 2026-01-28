# 📚 MindFlow 文档中心

> **最后更新**: 2026-01-28  
> **版本**: v0.3.1-alpha

---

## 🎯 快速导航

### 核心文档

| 文档 | 说明 | 更新时间 |
|------|------|----------|
| [CHANGELOG.md](CHANGELOG.md) | 📝 更新日志 | 2026-01-28 |
| [DEVELOPMENT_ENVIRONMENT.md](DEVELOPMENT_ENVIRONMENT.md) | 🔧 开发环境配置 | 2026-01-28 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 🏗️ 系统架构设计 | 2026-01-28 |
| [SKILL_FORMAT.md](SKILL_FORMAT.md) | 📋 Skill 格式规范 | 2026-01-27 |
| [VECTOR_STORE_OPTIMIZATION.md](VECTOR_STORE_OPTIMIZATION.md) | ⚡ VectorStore 优化说明 | 2026-01-28 |

### 开发计划

📅 [plans/](plans/) - 分阶段开发计划
- [Phase 1: 核心知识库](plans/phase1-knowledge-base.md) (Week 1-6)
- [Phase 2: 输入输出层](plans/phase2-io-layer.md) (Week 7-12)
- [Phase 3: 自我演化](plans/phase3-evolution.md) (Week 13-18)
- [Phase 4: 用户界面](plans/phase4-ui.md) (Week 19-22)
- [Phase 5: 生产部署](plans/phase5-production.md) (Week 23-24)

### 调研文档

🔬 [research/](research/) - 技术调研和分析
- [知识图谱工具调研](research/knowledge_graph_tools.md)
- [Obsidian Skills 分析](research/obsidian_skills_analysis.md)

### 归档文档

📦 [archive/](archive/) - 历史文档和记录
- [2026-01 归档](archive/2026-01/) - Week 1 完成文档
- [早期文档](archive/) - 项目初期的设计和学习记录

---

## 📖 文档说明

### 核心文档

#### CHANGELOG.md
记录项目的所有重要变更，包括：
- 新功能
- 优化改进
- Bug 修复
- 文档更新

#### DEVELOPMENT_ENVIRONMENT.md
开发环境配置指南，包括：
- Python 虚拟环境设置
- 依赖管理
- 测试命令
- 环境变量配置
- 常见问题解决

#### ARCHITECTURE.md
系统架构设计文档，包括：
- 整体架构
- 三层知识库结构
- 数据流设计
- 技术选型

#### SKILL_FORMAT.md
Skill 格式规范，遵循 [Agent Skills Specification](https://agentskills.io/)：
- Markdown 格式定义
- YAML frontmatter 规范
- 示例和最佳实践

#### VECTOR_STORE_OPTIMIZATION.md
VectorStore 优化说明（v0.3.1-alpha）：
- 使用 Chroma 内置 sentence-transformers
- 代码简化和性能提升
- 迁移指南

---

## 🗂️ 文档组织原则

### 活跃文档
- 保留在 `docs/` 根目录
- 持续更新和维护
- 反映当前最新状态

### 归档文档
- 移动到 `archive/` 目录
- 按时间组织（如 `2026-01/`）
- 作为历史记录保存
- 不再更新

### 计划文档
- 保存在 `plans/` 目录
- 按 Phase 组织
- 随项目进展更新

### 调研文档
- 保存在 `research/` 目录
- 技术选型和分析
- 参考资料

---

## 🔍 查找文档

### 按主题查找

**开发相关**:
- 环境配置 → [DEVELOPMENT_ENVIRONMENT.md](DEVELOPMENT_ENVIRONMENT.md)
- 系统架构 → [ARCHITECTURE.md](ARCHITECTURE.md)
- 更新日志 → [CHANGELOG.md](CHANGELOG.md)

**技术规范**:
- Skill 格式 → [SKILL_FORMAT.md](SKILL_FORMAT.md)
- VectorStore → [VECTOR_STORE_OPTIMIZATION.md](VECTOR_STORE_OPTIMIZATION.md)

**项目计划**:
- 开发计划 → [plans/](plans/)
- 当前进度 → [plans/phase1-knowledge-base.md](plans/phase1-knowledge-base.md)

**历史记录**:
- Week 1 总结 → [archive/2026-01/WEEK1_SUMMARY.md](archive/2026-01/WEEK1_SUMMARY.md)
- 技术设计 v1.1 → [archive/2026-01/TECHNICAL_DESIGN.md](archive/2026-01/TECHNICAL_DESIGN.md)

### 按时间查找

**最新文档** (2026-01-28):
- [CHANGELOG.md](CHANGELOG.md) - v0.3.1-alpha 更新
- [VECTOR_STORE_OPTIMIZATION.md](VECTOR_STORE_OPTIMIZATION.md) - VectorStore 优化
- [DEVELOPMENT_ENVIRONMENT.md](DEVELOPMENT_ENVIRONMENT.md) - 环境配置

**历史文档**:
- [archive/2026-01/](archive/2026-01/) - 2026年1月归档

---

## 📝 文档贡献

### 创建新文档

1. **确定文档类型**
   - 核心文档 → `docs/`
   - 计划文档 → `docs/plans/`
   - 调研文档 → `docs/research/`

2. **使用 Markdown 格式**
   - 清晰的标题结构
   - 代码块使用语法高亮
   - 添加目录（如果文档较长）

3. **更新 README.md**
   - 添加到相应的导航表格
   - 更新最后更新时间

### 归档文档

当文档不再活跃更新时：

1. **移动到 archive/**
   ```bash
   mv docs/OLD_DOC.md docs/archive/YYYY-MM/
   ```

2. **添加归档说明**
   - 在文档开头添加归档标记
   - 说明归档原因和时间

3. **更新链接**
   - 更新其他文档中的链接
   - 在 README.md 中移除或标记

---

## 🔗 相关资源

### 项目文档
- [项目 README](../README.md) - 项目概述和快速开始
- [AGENTS.md](../AGENTS.md) - Goose Agent 配置

### 学习资料
- [learning/](../learning/) - 技术学习资料
  - [NetworkX](../learning/networkx/)
  - [Chroma](../learning/chroma/)
  - [Pydantic](../learning/pydantic/)

### 外部资源
- [Agent Skills Specification](https://agentskills.io/)
- [Chroma Documentation](https://docs.trychroma.com/)
- [NetworkX Documentation](https://networkx.org/)

---

## 📊 文档统计

**核心文档**: 6 个  
**计划文档**: 6 个  
**调研文档**: 2 个  
**归档文档**: 9 个  

**总计**: 23 个文档

---

**维护者**: MindFlow Team  
**联系方式**: [GitHub Issues](https://github.com/damiangao/mindflow/issues)
