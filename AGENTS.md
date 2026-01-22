# Goose Agent 配置

本项目使用 Goose Desktop 进行开发。

## 开发规范

### 代码风格
- **最小化实现**：只写必要的代码，避免冗余
- **Simplicity First**：优先选择简单方案
- **中文响应**：与用户交互使用中文

### 知识库设计原则

#### 三层架构
- **L1 Methodologies**: 指导原则（如 "Simplicity First"）
- **L2 Skills**: 可执行能力（如 "CSV Processing"）
- **L3 Artifacts**: 执行产物（代码、文档等）

#### Artifact 设计 (v0.3.0)
```python
class Artifact:
    summary: str    # 文档总结（用于向量索引）
    filepath: str   # 文件路径（指向实际文件）
```

**设计理念**：
- 图数据库只存轻量级元数据
- 实际文件存储在 `artifacts/` 目录
- 支持语义搜索和文件复用

#### 关系类型
- `guides`: Methodology → Skill
- `produces`: Skill → Artifact
- `depends_on`: Skill → Skill

### 数据持久化

#### 文件结构
```
data/
├── graph.json          # 图数据（NetworkX）
└── vectors/            # 向量索引（Chroma）

artifacts/
├── *.py               # Python 代码
├── *.md               # 文档
└── *.yaml             # 配置
```

#### 重要提示
- `json.dumps()` 必须使用 `default=str` 处理 datetime
- 文件编码统一使用 UTF-8
- Windows 路径使用正斜杠 `/` 避免转义问题

## 当前进度 (v0.3.0-alpha)

### ✅ 已完成
- 三层数据模型 (Pydantic)
- 图存储 (NetworkX + JSON)
- 向量索引 (Chroma + sentence-transformers)
- 统一接口 (KnowledgeBase)
- Artifact 轻量化优化
- 测试验证通过

### 🎯 下一步 (Week 2)
- 种子库扩展 (15-20 Skills)
- 方法论评分机制
- Skills 组合规划器

## 技术栈

| 组件 | 技术 | 状态 |
|------|------|------|
| 数据模型 | Pydantic | ✅ |
| 图数据库 | NetworkX | ✅ |
| 向量索引 | Chroma | ✅ |
| 嵌入模型 | sentence-transformers | ✅ |
| 测试框架 | pytest | ⏳ |

## 常见问题

### datetime 序列化错误
```python
# ❌ 错误
json.dumps(data, ensure_ascii=False, indent=2)

# ✅ 正确
json.dumps(data, ensure_ascii=False, indent=2, default=str)
```

### HuggingFace 连接超时
- 使用本地缓存模型
- 或配置镜像源
- 测试时可跳过向量索引初始化

## 参考文档

- [开发计划](docs/DEVELOPMENT_PLAN.md)
- [技术设计](docs/TECHNICAL_DESIGN.md)
- [开发进度](docs/PROGRESS.md)
- [更新日志](docs/CHANGELOG.md)

---

**最后更新**: 2026-01-22  
**版本**: v0.3.0-alpha
