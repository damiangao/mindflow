# Phase 1: 核心知识库 (Week 1-6)

> **时间**: 2026-01-20 ~ 2026-03-02  
> **状态**: 🔄 进行中

---

## Week 1 (1/20 - 1/26): 环境搭建 + 基础实现 ✅

**已完成**:
- ✅ 三层数据模型 (Pydantic): Methodology, Skill, Artifact
- ✅ 图存储层 (NetworkX + JSON 持久化)
- ✅ 向量索引层 (Chroma + sentence-transformers)
- ✅ 统一接口 (KnowledgeBase)
- ✅ Artifact 轻量化优化 (summary + filepath)

**✅ Milestone 1.1**: 核心知识库架构完成

---

## Week 2 (1/27 - 2/2): Agent Skills 规范 + 种子库扩展

> **更新日期**: 2026-01-27  
> **调整原因**: 基于 Obsidian Skills 调研，优先实现业界标准兼容

### ✅ 已完成 (1/27)

**Agent Skills 规范迁移**:
- ✅ Skill 格式从 YAML 迁移到 Markdown (SKILL.md)
- ✅ 遵循 [Agent Skills Specification](https://agentskills.io/specification)
- ✅ 数据模型增加 `to_markdown()` / `from_markdown()` 方法
- ✅ 种子库加载器支持新格式 + 向后兼容
- ✅ 创建格式规范文档 `docs/SKILL_FORMAT.md`
- ✅ Obsidian Skills 调研报告 `docs/research/obsidian_skills_analysis.md`

**新目录结构**:
```
seeds/skills/
├── csv-processing/
│   └── SKILL.md          # Agent Skills 规范格式
├── daily-review/
│   └── SKILL.md
├── file-io/
│   └── SKILL.md
├── python-script/
│   └── SKILL.md
└── task-decompose/
    └── SKILL.md
```

### 📋 本周剩余任务 (1/28 - 2/2)

**1. 种子库扩展** (2天)
- [ ] 扩展到 15-20 个 Skills (SKILL.md 格式)
- [ ] 补充 Methodology 关联关系
- [ ] 每个 Skill 包含完整文档（示例、常见问题）

**新增 Skills 计划**:

| 类别 | Skills |
|------|--------|
| 数据处理 | json-processing, data-validation, data-transform |
| 生活管理 | weekly-review, task-tracking, note-organize |
| 代码辅助 | code-refactor, error-handling |
| 通用工具 | command-line, api-request |

**2. 方法论评分机制** (2天)
- [ ] 实现加权归一化算法
- [ ] Skill 查询时自动评分排序
- [ ] 测试评分准确性

```python
def calculate_skill_score(skill, methodologies):
    weighted_sum = 0
    total_weight = 0
    
    for meth in methodologies:
        score = skill.methodology_scores.get(meth.id, 0.5)
        weighted_sum += meth.weight * score
        total_weight += meth.weight
    
    return weighted_sum / total_weight
```

**3. JSON Canvas 导出** (1天，可选)
- [ ] 实现知识图谱导出为 Obsidian Canvas 格式
- [ ] 支持在 Obsidian 中可视化

**✅ Milestone 1.2**: 
- ✅ Agent Skills 规范兼容
- 15-20 个 Skills 种子库
- 方法论评分机制可用

---

## Week 3 (2/3 - 2/9): Skills 组合规划器

**开发任务**: `src/planner/skill_planner.py`

```python
class SkillPlanner:
    """Skills 组合规划器 (简化版 HTN)"""
    
    def plan(goal_effects: List[str], current_state: Set[str]) -> List[Skill]:
        """贪心搜索，返回执行序列"""
        pass
    
    def check_preconditions(skill: Skill, state: Set[str]) -> bool:
        """检查前置条件是否满足"""
        pass
    
    def apply_effects(skill: Skill, state: Set[str]) -> Set[str]:
        """应用 Skill 效果到状态"""
        pass
```

**规划流程**:
```
用户: "处理CSV并生成图表"
    ↓
LLM 解析目标 → ["has_dataframe", "has_chart"]
    ↓
当前状态: {"has_csv_file"}
    ↓
规划器搜索 → [Skill("CSV处理"), Skill("数据可视化")]
    ↓
返回执行计划
```

**✅ Milestone 1.3**: Skills 组合规划可用，能自动规划多步骤任务

---

## Week 4 (2/10 - 2/16): 可视化 + 导出 + Methodology 迁移

**开发任务**: `src/export/`

### 1. 可视化导出

```python
# 1. JSON Canvas 导出 (Obsidian 兼容)
class CanvasExporter:
    def export_knowledge_graph(kb: KnowledgeBase) -> dict
    def export_skill_chain(skill_id: str) -> dict

# 2. Markdown 导出 (Agent Skills 规范)
class MarkdownExporter:
    def export_skill(skill: Skill) -> str
    def export_all_skills(kb: KnowledgeBase, output_dir: Path)
```

**可视化功能**:
- [ ] 知识图谱导出为 JSON Canvas
- [ ] 在 Obsidian 中可视化三层架构
- [ ] Skill 调用链可视化

### 2. Methodology 迁移到 Markdown 格式 🆕

> **迁移成本分析**: 现在迁移成本最低（~2小时），在 Phase 3 自我演化之前完成

**涉及文件**:

| 文件 | 涉及内容 | 迁移影响 |
|------|----------|----------|
| `models.py` | Methodology 类定义 | 需增加 `to_markdown()` / `from_markdown()` |
| `load_seeds.py` | 加载 YAML 文件 | 需改为加载 METHODOLOGY.md |
| `graph_store.py` | `add_node()`, `get_skills_by_methodology()` | 无需修改 |
| `knowledge_base.py` | `add_methodology()`, `get_methodology()` | 无需修改 |

**迁移任务**:
- [ ] 设计 METHODOLOGY.md 格式规范
- [ ] 实现 `Methodology.to_markdown()` / `from_markdown()`
- [ ] 更新 `load_seeds.py` 支持新格式
- [ ] 迁移现有 5 个 YAML 文件到 Markdown
- [ ] 更新文档 `docs/METHODOLOGY_FORMAT.md`

**METHODOLOGY.md 格式草案**:
```markdown
---
name: simplicity-first
description: 优先选择简单方案
metadata:
  id: meth_simplicity
  display_name: Simplicity First
  weight: 0.8
  tags: [design, principle]
---

# Simplicity First

## 核心理念
...

## 应用场景
...

## 相关 Skills
- csv-processing (score: 0.9)
- task-decompose (score: 0.8)
```

**✅ Milestone 1.4**: 
- 知识库可视化，支持 Obsidian 集成
- Methodology 格式统一为 Markdown

---

## Week 5 (2/17 - 2/23): 向量搜索优化

**开发任务**: `src/knowledge_base/vector_store.py` 优化

- [ ] 上下文加权搜索
- [ ] 多集合联合查询
- [ ] 搜索结果缓存

```python
class VectorStore:
    def search_with_context(query: str, context: Context) -> List[Skill]:
        """带上下文的语义搜索"""
        # 1. 基础向量搜索
        # 2. 上下文加权调整
        # 3. 方法论评分排序
        pass
```

**✅ Milestone 1.5**: 向量搜索优化完成，首次命中率 > 80%

---

## Week 6 (2/24 - 3/2): 知识库整合 + Phase 1 验收

**开发任务**: 整合测试 + 文档完善

```python
def test_end_to_end():
    kb = KnowledgeBase()
    kb.load_seeds("seeds/")
    
    # 测试1: 语义搜索
    result = kb.query("帮我处理这个CSV文件")
    assert result.best_skill.name == "CSV文件处理"
    
    # 测试2: Skills 组合
    plan = kb.plan(["has_chart"], {"has_csv_file"})
    assert len(plan) >= 2
    
    # 测试3: 可视化导出
    canvas = kb.export_canvas()
    assert "nodes" in canvas
```

**🎯 Phase 1 验收标准**:
- ✅ 三层知识库结构完整
- ✅ Agent Skills 规范兼容
- ✅ Methodology Markdown 格式统一
- ✅ 15-20 个 Skills 种子库
- ✅ 方法论评分机制
- ✅ Skills 组合规划
- ✅ Obsidian 可视化导出
- ✅ 端到端测试通过

---

**返回**: [开发计划总览](./README.md)
