# Obsidian Skills 项目分析与启发

> **分析日期**: 2026-01-27  
> **项目来源**: https://github.com/kepano/obsidian-skills  
> **作者**: Steph Ango (Obsidian CEO)  
> **对标**: MindFlow v0.3.0-alpha

---

## 📋 项目概览

### 基本信息

| 维度 | Obsidian Skills | MindFlow |
|------|----------------|----------|
| **定位** | Agent Skills 规范实现 | 自我演化知识库 |
| **技术栈** | Markdown + YAML | NetworkX + Chroma + Python |
| **数据格式** | `.md`, `.base`, `.canvas` | JSON + 文件系统 |
| **核心价值** | 标准化 Agent 能力描述 | 动态学习和演化 |
| **开源协议** | MIT | (待定) |

### 项目结构

```
obsidian-skills/
├── .claude-plugin/
│   ├── plugin.json          # 插件元数据
│   └── marketplace.json     # 市场信息
└── skills/
    ├── obsidian-markdown/
    │   └── SKILL.md         # Markdown 语法规范
    ├── json-canvas/
    │   └── SKILL.md         # Canvas 格式规范
    └── obsidian-bases/
        └── SKILL.md         # Bases 数据库规范
```

---

## 🎯 核心设计理念

### 1. **Agent Skills 规范** (agentskills.io)

**关键发现**：
- 遵循统一的 Skills 描述标准
- 可被任何兼容 Agent 使用（Claude Code, Codex CLI）
- 使用 Markdown 作为 Skill 定义格式

**Skill 文件结构**：
```markdown
---
name: skill-name
description: When to use this skill
---

# Skill Title

## Overview
...

## Syntax Reference
...

## Examples
...
```

**对 MindFlow 的启发**：
- ✅ **标准化 Skill 格式**：我们的 `Skill` 数据模型可以导出为 Agent Skills 规范
- ✅ **互操作性**：MindFlow 生成的 Skills 可以被其他 Agent 使用
- ✅ **文档即代码**：Skill 的 `instructions` 字段可以直接是 Markdown

---

### 2. **声明式 Skill 定义**

**Obsidian Skills 的做法**：
- 纯文档形式描述能力
- 不包含可执行代码
- 依赖 LLM 理解和执行

**示例**：
```markdown
---
name: obsidian-markdown
description: Create and edit Obsidian Flavored Markdown with wikilinks, 
             embeds, callouts, properties, and other Obsidian-specific syntax.
---

# Obsidian Flavored Markdown Skill

## Wikilinks
\`\`\`markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
\`\`\`
```

**对 MindFlow 的启发**：

#### ✅ **混合模式优化**

当前 MindFlow 设计（TECHNICAL_DESIGN.md）：
```python
Skill {
    instructions: str       # 文本描述
    called_skills: List[str]  # 声明依赖
}
```

**改进方案**：
```python
class Skill:
    # 核心字段
    name: str
    description: str  # 触发条件（类似 Obsidian 的 description）
    
    # 执行方式（二选一或混合）
    instructions: Optional[str]      # 声明式（LLM 理解）
    executable: Optional[Callable]   # 命令式（直接执行）
    
    # 依赖和产物
    called_skills: List[str]
    artifacts: List[str]
    
    # 方法论评分
    methodology_scores: Dict[str, float]
```

**使用场景**：
- **纯声明式**：文档处理、格式转换（如 Obsidian Markdown）
- **纯命令式**：系统调用、API 请求
- **混合式**：复杂任务（LLM 规划 + 工具执行）

---

### 3. **领域特定语言 (DSL)**

**Obsidian Bases 的启发**：

Bases 使用 YAML + 表达式语言定义数据视图：
```yaml
formulas:
  days_until_due: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'

filters:
  and:
    - 'status != "done"'
    - file.hasTag("task")
```

**对 MindFlow 的启发**：

#### ✅ **Skill DSL 设计**

为 MindFlow 设计轻量级 DSL：

```yaml
# skills/data_cleaning.yaml
name: 数据清洗
description: 清洗 CSV 数据，处理缺失值和异常值

# 声明式规则
rules:
  preconditions:
    - has_dataframe
    - column_count > 0
  
  effects:
    - has_clean_data
    - has_validation_report

# 执行步骤（可被 LLM 理解）
steps:
  - action: check_missing
    formula: 'df.isnull().sum()'
  
  - action: fill_missing
    condition: 'missing_count > 0'
    method: 'df.fillna(df.mean())'
  
  - action: remove_outliers
    formula: 'df[(df.z_score < 3)]'

# 方法论评分
methodology_scores:
  meth_simple: 0.8
  meth_stdlib: 0.9
```

**优势**：
- LLM 可以直接理解和执行
- 人类可读性强
- 易于版本控制

---

### 4. **完整的语法参考文档**

**Obsidian Skills 的特点**：
- 每个 Skill 都是完整的语法手册
- 包含大量示例
- 覆盖边界情况

**示例**：`obsidian-markdown/SKILL.md` 包含：
- 基础格式（620 行）
- Wikilinks 语法
- Callouts 类型表
- Mermaid 图表
- LaTeX 数学公式
- 完整示例

**对 MindFlow 的启发**：

#### ✅ **Artifact 文档化标准**

```python
class Artifact:
    id: str
    name: str
    type: ArtifactType
    
    # 新增：完整文档
    documentation: str  # Markdown 格式
    examples: List[Example]
    
    # 文件路径
    filepath: str
    
    # 元数据
    usage_count: int
    tags: List[str]

class Example:
    title: str
    description: str
    code: str
    output: Optional[str]
```

**生成策略**：
- 自动从代码提取文档字符串
- LLM 生成使用示例
- 用户反馈补充边界情况

---

## 🔧 技术实现对比

### 1. **Skill 存储格式**

| 维度 | Obsidian Skills | MindFlow (当前) | MindFlow (改进) |
|------|----------------|----------------|----------------|
| **格式** | Markdown | JSON | YAML + Markdown |
| **可读性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **可编辑** | 文本编辑器 | 代码 | 文本编辑器 |
| **版本控制** | Git 友好 | Git 友好 | Git 友好 |
| **LLM 理解** | 优秀 | 一般 | 优秀 |

**改进方案**：

```
mindflow/
├── skills/
│   ├── data_processing/
│   │   ├── csv_processing.yaml      # Skill 定义
│   │   └── csv_processing.md        # 完整文档
│   └── life_management/
│       ├── task_breakdown.yaml
│       └── task_breakdown.md
└── artifacts/
    ├── csv_processor.py
    └── task_template.md
```

---

### 2. **插件系统设计**

**Obsidian Skills 的插件元数据**：

```json
{
  "name": "obsidian",
  "version": "1.0.0",
  "description": "Create and edit Obsidian vault files...",
  "author": {
    "name": "Steph Ango",
    "url": "https://stephango.com/"
  },
  "repository": "https://github.com/kepano/obsidian-skills",
  "keywords": ["obsidian", "markdown", "bases"]
}
```

**对 MindFlow 的启发**：

#### ✅ **Skill Package 系统**

```python
# src/knowledge_base/skill_package.py
class SkillPackage:
    """Skill 包管理器"""
    
    metadata: PackageMetadata
    skills: List[Skill]
    artifacts: List[Artifact]
    
    def install(self, kb: KnowledgeBase) -> None:
        """安装到知识库"""
        pass
    
    def export(self, output_dir: Path) -> None:
        """导出为标准格式"""
        pass

class PackageMetadata:
    name: str
    version: str
    description: str
    author: str
    repository: str
    keywords: List[str]
    dependencies: List[str]  # 依赖的其他包
```

**使用场景**：
```bash
# 安装社区 Skill 包
mindflow install data-science-skills

# 导出自己的 Skills
mindflow export my-skills --format agentskills
```

---

### 3. **JSON Canvas 的启发**

**JSON Canvas 规范**：
- 开放标准（jsoncanvas.org）
- 简单的节点-边模型
- 支持多种节点类型（text, file, link, group）

**数据结构**：
```json
{
  "nodes": [
    {
      "id": "6f0ad84f44ce9c17",
      "type": "text",
      "x": 0, "y": 0,
      "width": 400, "height": 200,
      "text": "# Hello World"
    }
  ],
  "edges": [
    {
      "id": "f67890123456789a",
      "fromNode": "6f0ad84f44ce9c17",
      "toNode": "a1b2c3d4e5f67890"
    }
  ]
}
```

**对 MindFlow 的启发**：

#### ✅ **知识图谱可视化导出**

```python
# src/export/canvas_exporter.py
class CanvasExporter:
    """导出为 JSON Canvas 格式"""
    
    def export_knowledge_graph(self, kb: KnowledgeBase) -> dict:
        """
        将 MindFlow 知识图谱导出为 Canvas
        - Methodology 节点 → 紫色 group
        - Skill 节点 → 蓝色 text
        - Artifact 节点 → 绿色 file
        - 关系 → edges
        """
        nodes = []
        edges = []
        
        # 布局算法（力导向图）
        layout = self._calculate_layout(kb)
        
        for skill in kb.get_all_skills():
            nodes.append({
                "id": skill.id,
                "type": "text",
                "x": layout[skill.id].x,
                "y": layout[skill.id].y,
                "width": 300,
                "height": 150,
                "text": f"# {skill.name}\n\n{skill.description}",
                "color": "5"  # 蓝色
            })
        
        return {"nodes": nodes, "edges": edges}
```

**使用场景**：
- 在 Obsidian 中可视化 MindFlow 知识库
- 手动编辑后重新导入
- 与团队分享知识图谱

---

## 💡 关键启发总结

### 1. **标准化优先** ⭐⭐⭐⭐⭐

**行动项**：
- [ ] 实现 Agent Skills 规范导出
- [ ] 设计 MindFlow Skill YAML 格式
- [ ] 支持导入标准 Skills

**优先级**: 高（Week 2-3）

---

### 2. **文档即代码** ⭐⭐⭐⭐⭐

**行动项**：
- [ ] 为每个 Skill 生成完整文档
- [ ] 使用 Markdown 作为主要格式
- [ ] 自动生成示例代码

**优先级**: 中（Week 4-5）

---

### 3. **插件生态系统** ⭐⭐⭐⭐

**行动项**：
- [ ] 设计 Skill Package 格式
- [ ] 实现安装/导出功能
- [ ] 创建社区 Skill 仓库

**优先级**: 低（Phase 2）

---

### 4. **可视化导出** ⭐⭐⭐⭐

**行动项**：
- [ ] 实现 JSON Canvas 导出
- [ ] 支持 Obsidian Graph View
- [ ] 双向同步（导入/导出）

**优先级**: 中（Week 6）

---

### 5. **DSL 设计** ⭐⭐⭐

**行动项**：
- [ ] 设计 Skill DSL 语法
- [ ] 实现解释器
- [ ] 编写语法文档

**优先级**: 低（Phase 3）

---

## 🚀 立即行动计划

### Week 2 (本周) 优先级调整

**原计划**：
- 数据模型设计
- Claude API 学习

**新增任务**（基于 Obsidian Skills 启发）：

#### 1. **Skill 格式标准化** (2天)

```python
# src/knowledge_base/models.py
class Skill:
    # 基础字段
    id: str
    name: str
    description: str  # 触发条件（Agent Skills 规范）
    
    # 执行方式
    instructions: str  # Markdown 格式
    executable: Optional[str]  # Python 代码路径
    
    # 依赖
    preconditions: List[str]
    effects: List[str]
    called_skills: List[str]
    
    # 方法论
    methodology_scores: Dict[str, float]
    
    # 元数据
    version: str
    author: str
    tags: List[str]
    
    def to_agentskills_format(self) -> str:
        """导出为 Agent Skills 规范"""
        return f"""---
name: {self.name}
description: {self.description}
---

# {self.name}

{self.instructions}
"""
```

#### 2. **YAML 配置支持** (1天)

```yaml
# skills/csv_processing.yaml
name: CSV 文件处理
description: 读取、解析、处理 CSV 格式数据。当用户提到 CSV、表格数据、数据清洗时使用。

instructions: |
  1. 使用 pandas 读取 CSV 文件
  2. 检查数据完整性
  3. 处理缺失值
  4. 返回 DataFrame

preconditions:
  - has_csv_file

effects:
  - has_dataframe

methodology_scores:
  meth_simple: 0.8
  meth_stdlib: 0.9

called_skills:
  - file_read

version: "1.0.0"
author: "MindFlow"
tags:
  - data-processing
  - csv
```

#### 3. **Canvas 导出原型** (1天)

```python
# src/export/canvas_exporter.py
def export_to_canvas(kb: KnowledgeBase, output_path: Path):
    """导出知识图谱为 JSON Canvas"""
    canvas = {
        "nodes": [],
        "edges": []
    }
    
    # 简单布局：按层级排列
    y_offset = 0
    for methodology in kb.get_all_methodologies():
        canvas["nodes"].append({
            "id": methodology.id,
            "type": "group",
            "x": 0,
            "y": y_offset,
            "width": 1000,
            "height": 400,
            "label": methodology.name,
            "color": "6"
        })
        y_offset += 500
    
    output_path.write_text(json.dumps(canvas, indent=2))
```

---

## 📊 对比矩阵

| 特性 | Obsidian Skills | MindFlow (当前) | MindFlow (目标) |
|------|----------------|----------------|----------------|
| **标准化格式** | ✅ Agent Skills | ❌ 自定义 JSON | ✅ 兼容 Agent Skills |
| **文档质量** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **可视化** | ✅ Canvas | ❌ 无 | ✅ Canvas + Graph |
| **插件系统** | ✅ Marketplace | ❌ 无 | ✅ Package Manager |
| **自我演化** | ❌ 静态 | ✅ 动态学习 | ✅ 动态学习 |
| **方法论评分** | ❌ 无 | ✅ 有 | ✅ 增强 |
| **Skills 组合** | ❌ 无 | ✅ HTN Planning | ✅ HTN Planning |

---

## 🎯 核心差异化优势

**MindFlow 保持的独特价值**：

1. ✅ **自我演化**：从使用中学习新 Skills
2. ✅ **方法论驱动**：量化评分和优化
3. ✅ **动态组合**：HTN Planning 规划 Skills 序列
4. ✅ **副产品提取**：自动积累可复用代码
5. ✅ **用户交互策略**：三级风险评估

**借鉴 Obsidian Skills 的优势**：

1. ✅ **标准化**：兼容 Agent Skills 规范
2. ✅ **文档化**：完整的语法参考
3. ✅ **可视化**：JSON Canvas 导出
4. ✅ **生态系统**：插件市场

---

## 📝 结论

Obsidian Skills 项目为 MindFlow 提供了以下关键启发：

### 立即采纳（Week 2-3）
1. **Agent Skills 规范兼容**
2. **YAML + Markdown 格式**
3. **完整文档生成**

### 中期规划（Week 4-6）
4. **JSON Canvas 导出**
5. **Skill Package 系统**

### 长期愿景（Phase 2-3）
6. **社区 Skill 市场**
7. **DSL 设计**

**核心策略**：
- 保持 MindFlow 的自我演化核心优势
- 借鉴 Obsidian 的标准化和文档化
- 实现互操作性，融入 Agent 生态

---

**创建日期**: 2026-01-27  
**分析者**: MindFlow Team  
**下一步**: 更新 Week 2 开发计划
