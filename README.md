# Mindflow - 智能体操作系统

> 你的个人智能体操作系统 | 知识库驱动 | 自我演化

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-architecture--complete-green.svg)](docs/DEVELOPMENT.md)
[![Version](https://img.shields.io/badge/version-v0.2.0--alpha-yellow.svg)](docs/CHANGELOG.md)

---

## 🎯 项目简介

**Mindflow** 是一个智能体操作系统 (Agent OS),运行在 Windows/macOS/Linux 之上,专注于个人生活场景的深度优化。

### 核心特点

- 🧠 **知识库驱动** - 以知识图谱为认知基础
- 🔄 **自我演化** - Skills 自动学习和优化
- 🏠 **生活场景** - 深度优化个人日常使用
- 🔐 **隐私优先** - 本地存储,离线可用

### 核心架构

```
输入层 (Input Layer)
  ↓
知识库 (Knowledge Base) - 三层结构
  ├─ L1: 方法论层 (Methodologies)
  ├─ L2: Skills 层
  └─ L3: 副产品层 (Artifacts)
  ↓
输出层 (Output Layer)
```

**详细设计**: 见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🚀 快速开始

### 当前状态

- **版本**: v0.2.0-alpha
- **阶段**: 架构设计完成
- **下一步**: Phase 1 - 核心知识库实现

### 安装（开发中）

```bash
# 克隆仓库
git clone https://github.com/damiangao/mindflow.git
cd mindflow

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖 (待创建)
pip install -r requirements.txt

# 配置 LLM API Key
cp .env.example .env
# 编辑 .env 填入 API Key
```

---

## 📚 文档索引

### 核心文档

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - 核心架构设计
  - 操作系统抽象
  - 知识库三层结构
  - 核心机制设计

- **[TECHNICAL_DESIGN.md](docs/TECHNICAL_DESIGN.md)** - 技术实现方案
  - 数据结构设计
  - 核心算法
  - 技术栈选型

- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - 开发指南
  - Phase 1-5 路线图
  - 任务清单
  - 快速开始

- **[LEARNING.md](docs/LEARNING.md)** - 技术栈学习计划
  - 分阶段学习路线
  - 学习资源
  - 检查清单

- **[CHANGELOG.md](docs/CHANGELOG.md)** - 更新日志
  - 版本历史
  - 重要变更

---

## 📋 开发进度

### Phase 1: 核心知识库 (4-6周)
- [ ] 数据结构设计
- [ ] 图数据库 (NetworkX / Neo4j)
- [ ] 向量索引 (Chroma)
- [ ] 冷启动种子库 (5个方法论 + 15-20个 Skills)

### Phase 2: 输入输出层 (4-6周)
- [ ] 意图识别
- [ ] Skills 匹配和执行
- [ ] 对话生成

### Phase 3: 自我演化 (4-6周)
- [ ] 副产品提取
- [ ] Skills 自动生成
- [ ] 用户交互策略

### Phase 4-5: UI 和生产 (4-6周)
- [ ] 前端界面
- [ ] 错误处理
- [ ] 部署方案

**详细计划**: 见 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

---

## 🔧 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **知识库** | Neo4j / NetworkX | 图数据库 |
| **向量索引** | Chroma | 语义搜索 |
| **LLM** | Claude / GPT / DeepSeek | 意图理解/生成 |
| **后端** | Python 3.10+ | 核心逻辑 |
| **前端** | Gradio / Tauri | UI |

---

## 📊 竞品分析

| 产品 | 定位 | 相似度 | 主要差异 | Mindflow 优势 |
|------|------|--------|----------|--------------|
| **LangChain** | AI开发框架 | 7/10 | 开发者工具 | 生活场景深度优化 |
| **AutoGPT** | 自主智能体 | 6/10 | 技术实验 | 稳定可靠的日常使用 |
| **Notion AI** | 知识管理 | 4/10 | 云端服务 | 本地存储+自我演化 |
| **Obsidian** | 知识管理 | 3/10 | 被动工具 | AI主动协助 |

**市场空白**: 本地运行 + 自我演化 + 生活场景深度优化

---

## 🤝 贡献指南

欢迎贡献! 请遵循以下流程:

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交代码 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交规范

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👥 贡献者

- [@damiangao](https://github.com/damiangao) - 项目创建者

---

## 🔗 相关链接

- **GitHub**: https://github.com/damiangao/mindflow
- **文档**: [docs/](docs/)
- **问题反馈**: [GitHub Issues](https://github.com/damiangao/mindflow/issues)

---

**最后更新**: 2026-01-18  
**当前版本**: v0.2.0-alpha  
**状态**: 架构设计完成,准备开始实现
