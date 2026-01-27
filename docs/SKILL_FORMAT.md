# MindFlow Skill 格式规范

> **版本**: 1.0.0  
> **日期**: 2026-01-27  
> **基于**: [Agent Skills Specification](https://agentskills.io/specification)

---

## 概述

MindFlow 的 Skill 格式遵循 **Agent Skills 规范**，使用 Markdown 文件 (`SKILL.md`) 定义 Skill。这确保了与其他 Agent 系统（如 Claude Code、Codex CLI）的互操作性。

## 目录结构

```
seeds/skills/
├── csv-processing/
│   └── SKILL.md          # 必需
├── daily-review/
│   ├── SKILL.md          # 必需
│   └── references/       # 可选：参考文档
│       └── TEMPLATE.md
└── python-script/
    ├── SKILL.md          # 必需
    └── scripts/          # 可选：可执行脚本
        └── generator.py
```

## SKILL.md 格式

### 基本结构

```markdown
---
name: skill-name
description: 描述 Skill 的功能和触发条件
metadata:
  # MindFlow 扩展字段
  id: skill_xxx
  display_name: 显示名称
  preconditions: [...]
  effects: [...]
  methodology_scores: {...}
---

# Skill 标题

## 概述
...

## 执行步骤
...

## 示例
...
```

### Frontmatter 字段

#### 必需字段 (Agent Skills 规范)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `name` | string | 1-64字符，小写字母、数字、连字符 | Skill 标识符 |
| `description` | string | 1-1024字符 | 描述功能和触发条件 |

#### MindFlow 扩展字段 (metadata)

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | `skill_{name}` | 内部唯一标识符 |
| `display_name` | string | 从 name 生成 | 显示名称（支持中文） |
| `preconditions` | list[str] | `[]` | 前置条件 |
| `effects` | list[str] | `[]` | 产生效果 |
| `methodology_scores` | dict[str, float] | `{}` | 方法论评分 (0-1) |
| `parent_methodologies` | list[str] | `[]` | 所属方法论 |
| `called_skills` | list[str] | `[]` | 依赖的其他 Skills |
| `tags` | list[str] | `[]` | 标签 |
| `version` | string | `"1.0.0"` | 版本号 |
| `author` | string | `"MindFlow"` | 作者 |

### Markdown 正文

正文部分没有格式限制，但建议包含以下章节：

1. **概述** - 简要说明 Skill 的用途
2. **执行步骤** - 详细的执行流程
3. **示例** - 输入输出示例
4. **常见问题** - FAQ 和边界情况

## 完整示例

```markdown
---
name: csv-processing
description: 读取、解析、处理CSV格式数据。当用户提到CSV文件、表格数据、数据清洗、数据导入时使用。
metadata:
  id: skill_csv
  display_name: CSV文件处理
  preconditions:
    - has_csv_file
  effects:
    - has_dataframe
  methodology_scores:
    meth_simple: 0.8
    meth_stdlib: 0.9
  parent_methodologies:
    - meth_simple
    - meth_stdlib
  called_skills: []
  tags:
    - data-processing
    - csv
    - pandas
  version: "1.0.0"
  author: MindFlow
---

# CSV文件处理

## 概述

读取、解析、处理CSV格式数据。支持数据清洗、缺失值处理、数据验证等常见操作。

## 执行步骤

1. 使用 pandas 读取 CSV 文件
2. 检查数据完整性和列名
3. 处理缺失值和异常数据
4. 返回处理后的 DataFrame

## 示例

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.fillna(df.mean(), inplace=True)
```

## 常见问题

### 编码问题
如果遇到编码错误，尝试指定编码：
```python
df = pd.read_csv("data.csv", encoding="utf-8")
```
```

## 命名规范

### name 字段

- 只能包含小写字母、数字和连字符 (`a-z`, `0-9`, `-`)
- 不能以连字符开头或结尾
- 不能包含连续连字符 (`--`)
- 长度 1-64 字符

**正确示例**:
```yaml
name: csv-processing
name: daily-review
name: python-script
```

**错误示例**:
```yaml
name: CSV-Processing  # 大写字母
name: -csv            # 以连字符开头
name: csv--process    # 连续连字符
```

### description 字段

- 长度 1-1024 字符
- 应描述 Skill 的功能和触发条件
- 包含关键词帮助 Agent 识别相关任务

**好的示例**:
```yaml
description: 读取、解析、处理CSV格式数据。当用户提到CSV文件、表格数据、数据清洗、数据导入时使用。
```

**差的示例**:
```yaml
description: 处理CSV
```

## 渐进式加载

为了高效使用上下文，Skill 应该分层组织：

1. **元数据** (~100 tokens): `name` 和 `description` 在启动时加载
2. **指令** (< 5000 tokens): 激活 Skill 时加载完整 `SKILL.md`
3. **资源** (按需): `scripts/`、`references/` 中的文件按需加载

**建议**:
- `SKILL.md` 保持在 500 行以内
- 详细参考资料放在 `references/` 目录

## 与旧格式的兼容性

MindFlow 仍支持旧版 YAML 格式 (`*.yaml`)，但建议迁移到新格式：

### 旧格式 (不推荐)
```yaml
# seeds/skills/csv_processing.yaml
id: skill_csv
name: CSV文件处理
description: 读取、解析、处理CSV格式数据
instructions: |
  1. 使用 pandas 读取 CSV 文件
  ...
```

### 新格式 (推荐)
```markdown
# seeds/skills/csv-processing/SKILL.md
---
name: csv-processing
description: 读取、解析、处理CSV格式数据...
metadata:
  id: skill_csv
  display_name: CSV文件处理
---

# CSV文件处理

## 执行步骤
1. 使用 pandas 读取 CSV 文件
...
```

## 验证

使用以下命令验证 Skill 格式：

```bash
# 安装依赖
pip install python-frontmatter

# 验证单个 Skill
python -c "
import frontmatter
from pathlib import Path

skill_file = Path('seeds/skills/csv-processing/SKILL.md')
post = frontmatter.loads(skill_file.read_text())

# 检查必需字段
assert 'name' in post.metadata, 'Missing name'
assert 'description' in post.metadata, 'Missing description'
assert len(post.metadata['name']) <= 64, 'name too long'
assert len(post.metadata['description']) <= 1024, 'description too long'

print('✓ Skill 格式验证通过')
"
```

## 参考

- [Agent Skills Specification](https://agentskills.io/specification)
- [Obsidian Skills](https://github.com/kepano/obsidian-skills)
- [MindFlow 技术设计](TECHNICAL_DESIGN.md)

---

**最后更新**: 2026-01-27  
**维护者**: MindFlow Team
