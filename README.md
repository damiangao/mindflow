# Mindflow

> **Mindflow 是一个跨平台智能体操作系统,与你共同成长的数字伙伴**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()
[![Version](https://img.shields.io/badge/version-0.3.0--alpha-blue.svg)]()

---

## 🎯 项目愿景

Mindflow 是一个运行在 Windows/macOS/Linux 之上的智能体操作系统,专注于个人生活场景的深度优化。它不仅是一个工具,更是一个能够理解你、学习你、与你共同成长的数字伙伴。

## ✨ 核心特点

- 🧠 **知识库驱动** - 以知识图谱为认知基础,构建对世界的理解模型
- 🔄 **自我演化** - Skills 自动学习和优化,持续提升能力
- 🏠 **生活场景** - 深度优化个人日常使用,贴近真实需求
- 🔐 **隐私优先** - 本地存储,离线可用,数据完全掌控

## 🏗️ 架构设计

Mindflow 采用操作系统的抽象思维:

```
输入层 (Input)  →  知识库 (Knowledge Base)  →  输出层 (Output)
   ↓                      ↓                          ↓
多模态感知            认知与决策                  行动与学习
```

### 三层知识库结构

```
┌─────────────────────────────────┐
│  L1: 方法论层 (Methodologies)   │  ← 抽象原则,指导思维
│  数量: 10-50 个                  │
└─────────────────────────────────┘
           ↓ 指导
┌─────────────────────────────────┐
│  L2: Skills 层                  │  ← 可执行步骤,持续演化
│  数量: 100-500 个                │
└─────────────────────────────────┘
           ↓ 应用
┌─────────────────────────────────┐
│  L3: 产物层 (Artifacts)         │  ← 可复用资源,无限增长
│  数量: 无限                      │
└─────────────────────────────────┘
```

### Artifact 轻量化设计 (v0.3.0 新特性)

```python
class Artifact:
    summary: str    # 文档总结（用于向量索引）
    filepath: str   # 文件路径（指向实际文件）
```

**优势**:
- 图数据库轻量（减少 67% 存储空间）
- 文件可复用（可直接导入执行）
- 支持语义搜索（summary 用于索引）

## 🚀 快速开始

### 环境要求
- Python 3.10+
- 推荐使用 [uv](https://github.com/astral-sh/uv) 进行环境管理

### 安装步骤

**1. 安装 uv（推荐）**
```powershell
# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. 克隆项目**
```bash
git clone https://github.com/yourusername/mindflow.git
cd mindflow
```

**3. 创建虚拟环境**
```bash
uv venv --python 3.11
```

**4. 激活虚拟环境**
```powershell
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

**5. 安装依赖**
```bash
uv pip install -r requirements.txt
```

**6. 运行测试**
```bash
python tests/test_kb_en.py
python tests/test_e2e.py
python tests/test_artifact.py
```

### 常见问题

**Q: PowerShell 提示无法运行脚本？**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Q: 不想用 uv？**
```bash
# 使用标准 pip
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 🚀 核心能力

- **智能理解**: 基于知识库的深度意图识别
- **自动学习**: 从每次交互中提取经验,生成新的 Skills
- **知识演化**: 向上聚合提炼方法论,向下应用到具体场景
- **个性化**: 根据用户习惯和偏好持续优化

## 🛠️ 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **知识库** | NetworkX / Neo4j | 图数据库 |
| **向量索引** | Chroma + sentence-transformers | 语义搜索 |
| **LLM** | Claude / GPT / DeepSeek | 意图理解/生成 |
| **后端** | Python 3.10+ | 核心逻辑 |
| **前端** | Gradio / Tauri | 用户界面 |

## 📂 项目结构

```
mindflow/
├── src/                     # 源代码
│   └── knowledge_base/      # 知识库核心模块
│       ├── models.py        # 数据模型
│       ├── graph_store.py   # 图存储层
│       ├── vector_store.py  # 向量索引层
│       └── knowledge_base.py # 统一接口
├── tests/                   # 测试文件
│   ├── test_kb_en.py       # 功能测试
│   ├── test_e2e.py         # 端到端测试
│   └── test_artifact.py    # Artifact 测试
├── artifacts/               # 产物文件（代码/文档）
├── data/                    # 数据存储
│   ├── graph.json          # 图数据
│   └── vectors/            # 向量索引
├── docs/                    # 文档
│   ├── ARCHITECTURE.md      # 架构设计
│   ├── TECHNICAL_DESIGN.md  # 技术设计
│   ├── DEVELOPMENT_PLAN.md  # 开发计划
│   ├── PROGRESS.md          # 开发进度
│   └── CHANGELOG.md         # 更新日志
├── seeds/                   # 种子库
│   ├── methodologies/       # 方法论
│   └── skills/              # Skills
├── requirements.txt         # 依赖列表
├── pyproject.toml          # 项目配置
└── 
```

## 🎯 开发路线

### Phase 1: 核心知识库 ✅ 完成 (v0.3.0-alpha)
- ✅ 三层知识库结构实现
- ✅ 图数据库和向量索引
- ✅ 基础 CRUD 操作
- ✅ Artifact 轻量化优化
- ✅ 测试验证通过

### Phase 2: 输入输出 (Week 7-12)
- 文本输入和意图识别
- 对话生成和代码生成
- 复盘分析机制

### Phase 3: 自我演化 (Week 13-18)
- 产物自动提取
- Skills 自动生成
- 方法论演化机制

## 📖 文档

- [架构设计](docs/ARCHITECTURE.md) - 详细的系统架构说明
- [技术设计](docs/TECHNICAL_DESIGN.md) - 核心机制的技术实现
- [开发计划](docs/DEVELOPMENT_PLAN.md) - 详细的开发计划和时间线
- [开发进度](docs/PROGRESS.md) - 当前开发进度和完成情况
- [更新日志](docs/CHANGELOG.md) - 版本更新记录

## 🤝 参与贡献

Mindflow 目前处于早期开发阶段,欢迎各种形式的贡献:

- 💡 提出想法和建议
- 🐛 报告 Bug
- 📝 完善文档
- 💻 提交代码

## 📄 开源协议

本项目采用 [Apache License 2.0](LICENSE) 开源协议。

## 🌟 致谢

### 开发工具

本项目完全由 **[Goose](https://github.com/block/goose)** 辅助开发完成。

Goose 是由 Block 公司开发的开源 AI 编程助手，它不仅帮助编写代码，更重要的是：
- 🧠 **架构设计**：从零开始设计三层知识库架构
- 📝 **文档编写**：完整的技术文档和学习计划
- 🔍 **技术调研**：Obsidian Skills、Agent Skills 规范等
- 🐛 **问题解决**：调试、优化、重构
- 🎓 **知识传递**：定制化学习路线（NetworkX、Chroma 等）

**感谢 Goose 团队**，让 AI 辅助开发变得如此高效和愉快！

---

### 参考项目

Mindflow 的设计和实现受到以下优秀项目的启发：

#### 知识库与 Agent 框架
- **[Obsidian Skills](https://github.com/your-obsidian-skills-link)** - Agent Skills 规范的先驱，启发了我们的 Skill 格式设计
- **[Agent Skills Specification](https://agentskills.io/)** - 业界标准的 Agent 技能描述规范
- **[LangChain](https://github.com/langchain-ai/langchain)** - Agent 框架设计思路
- **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** - 自主 Agent 的实践参考

#### 知识图谱与向量搜索
- **[NetworkX](https://github.com/networkx/networkx)** - 图数据库的 Python 实现
- **[Chroma](https://github.com/chroma-core/chroma)** - 轻量级向量数据库
- **[sentence-transformers](https://github.com/UKPLab/sentence-transformers)** - 高质量的文本向量化模型

#### 自我演化与学习
- **[Voyager](https://github.com/MineDojo/Voyager)** - 自我演化 Agent 的开创性工作
- **[MetaGPT](https://github.com/geekan/MetaGPT)** - 多 Agent 协作框架

#### 工具与基础设施
- **[uv](https://github.com/astral-sh/uv)** - 快速的 Python 包管理器
- **[Pydantic](https://github.com/pydantic/pydantic)** - 数据验证和模型定义

---

### 特别感谢

- 感谢所有开源项目的贡献者，你们的工作让这个项目成为可能
- 感谢 Goose 社区的支持和反馈
- 感谢每一位关注和使用 Mindflow 的用户

---

**当前状态**: Alpha 开发中 | **版本**: v0.3.0-alpha | **最后更新**: 2026-01-27


