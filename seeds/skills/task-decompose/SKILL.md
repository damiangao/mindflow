---
name: task-decompose
description: 将复杂任务分解为可执行的小步骤。当用户提到任务分解、拆分任务、规划步骤、项目规划时使用。
metadata:
  id: skill_task_decompose
  display_name: 任务分解
  preconditions:
    - has_task_description
  effects:
    - has_task_list
  methodology_scores:
    meth_simple: 0.9
    meth_iterate: 0.9
  parent_methodologies:
    - meth_simple
    - meth_iterate
  called_skills: []
  tags:
    - life-management
    - planning
    - productivity
  version: "1.0.0"
  author: MindFlow
---

# 任务分解

## 概述

将复杂任务分解为可执行的小步骤。通过结构化的分解方法，让大任务变得可管理、可追踪。

## 执行步骤

1. 理解任务的最终目标
2. 识别关键里程碑
3. 将每个里程碑分解为具体步骤
4. 确定步骤之间的依赖关系
5. 输出结构化的任务列表

## 分解原则

### SMART 原则

每个子任务应该是：
- **S**pecific（具体的）：明确要做什么
- **M**easurable（可衡量的）：知道何时完成
- **A**chievable（可实现的）：在能力范围内
- **R**elevant（相关的）：与目标相关
- **T**ime-bound（有时限的）：有明确的截止时间

### 分解粒度

- 每个子任务应该在 **2-4 小时** 内可完成
- 如果超过 4 小时，继续分解
- 如果少于 30 分钟，考虑合并

## 分解模板

```markdown
# 任务：{{task_name}}

## 目标
{{final_goal}}

## 里程碑
1. [ ] 里程碑1 - 截止日期
2. [ ] 里程碑2 - 截止日期
3. [ ] 里程碑3 - 截止日期

## 详细步骤

### 里程碑1：{{milestone_name}}
- [ ] 步骤1.1：具体任务描述 (预计时间)
- [ ] 步骤1.2：具体任务描述 (预计时间)
  - 依赖：步骤1.1

### 里程碑2：{{milestone_name}}
- [ ] 步骤2.1：具体任务描述 (预计时间)

## 依赖关系
- 步骤1.2 依赖 步骤1.1
- 里程碑2 依赖 里程碑1

## 风险和注意事项
- 风险1：描述及应对措施
```

## 示例

### 输入
> 我想学习 Python 数据分析

### 输出

```markdown
# 任务：学习 Python 数据分析

## 目标
能够使用 Python 进行基础数据分析，包括数据清洗、可视化和简单统计

## 里程碑
1. [ ] 环境搭建 - 第1天
2. [ ] 基础语法 - 第1周
3. [ ] Pandas 入门 - 第2周
4. [ ] 数据可视化 - 第3周
5. [ ] 实战项目 - 第4周

## 详细步骤

### 里程碑1：环境搭建
- [ ] 安装 Python 3.x (30分钟)
- [ ] 安装 VS Code 和 Python 插件 (30分钟)
- [ ] 安装 Jupyter Notebook (30分钟)
- [ ] 验证环境：运行 Hello World (15分钟)

### 里程碑2：基础语法
- [ ] 学习变量和数据类型 (2小时)
- [ ] 学习控制流程 (2小时)
- [ ] 学习函数定义 (2小时)
- [ ] 完成10道练习题 (3小时)
```

## 常见问题

### 任务太大不知道从哪开始
- 先写出最终目标
- 倒推需要哪些中间成果
- 每个中间成果就是一个里程碑

### 分解后任务太多
- 按优先级排序
- 先完成最重要的 3-5 个
- 其他任务可以后续调整
