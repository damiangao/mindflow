# Mindflow 技术设计文档 (精简版)

> **基于**: ARCHITECTURE.md v1.0  
> **版本**: v1.1  
> **日期**: 2026-01-18  
> **状态**: 核心机制已确定

---

## 🎯 本文档目的

本文档补充 ARCHITECTURE.md,用流程图和伪代码说明核心机制。

---

## 📊 数据结构增强

### Skill 节点新增字段

```
Skill {
    ... (基础字段见 ARCHITECTURE.md)
    
    # 新增: 规划相关
    preconditions: ["has_csv_file"]      # 前置条件
    effects: ["has_dataframe"]           # 产生效果
    
    # 新增: 方法论评分
    methodology_scores: {
        "meth_simple": 0.9,              # 对各方法论的符合度 0-1
        "meth_stdlib": 0.7
    }
}
```

### Methodology 节点新增字段

```
Methodology {
    ... (基础字段见 ARCHITECTURE.md)
    
    # 新增: 评估规则
    evaluation_rule: "检查是否使用标准库"  # 文本描述或代码
    weight: 0.8                           # 全局权重 0-1
}
```

## 🔗 Skills 调用方式 (混合模式)

### 数据结构

```
Skill {
    name: "数据清洗流程"
    instructions: """
    1. 读取CSV文件
    2. 验证数据完整性
    3. 处理缺失值
    4. 输出清洗后的数据
    """
    called_skills: ["CSV处理", "数据验证"]  # 声明依赖
}
```

### 执行流程

```
激活 Skill
    ↓
LLM 读取 instructions
    ↓
逐步执行:
  ├─ 识别需要调用的子 Skill
  ├─ 从 called_skills 中查找
  ├─ 调用并传递数据
  └─ 继续下一步
    ↓
完成
```

### 关键设计

**called_skills 的作用**:
- 声明依赖(用于规划)
- 限制调用范围(安全性)
- 建立图结构关联

**LLM 的职责**:
- 理解 instructions
- 决定调用时机
- 处理数据传递

**实现伪代码**:
```python
def execute_skill(skill, context):
    prompt = f"""
    Skill: {skill.name}
    步骤: {skill.instructions}
    可用子Skills: {skill.called_skills}
    当前状态: {context}
    """
    return llm.execute_with_tools(prompt, tools=skill.called_skills)
```


---

## 🔍 方法论评分机制

### 流程图

```
用户请求
    ↓
向量搜索 → 候选 Skills [A, B, C]
    ↓
对每个 Skill:
    ├─ 获取 methodology_scores
    ├─ 加权求和: Σ(方法论权重 × 符合度)
    ├─ 归一化: 总和 / 总权重
    └─ 混合历史成功率: 0.7×评分 + 0.3×success_rate
    ↓
排序 → 选择得分最高的 Skill
```

### 伪代码

```python
def calculate_skill_score(skill, methodologies):
    weighted_sum = 0
    total_weight = 0
    
    for meth in methodologies:
        score = skill.methodology_scores.get(meth.id, 0.5)
        weighted_sum += meth.weight * score
        total_weight += meth.weight
    
    base_score = weighted_sum / total_weight
    
    # 混合历史表现
    if skill.usage_count > 0:
        final = 0.7 * base_score + 0.3 * skill.success_rate
    else:
        final = base_score
    
    return clamp(final, 0, 1)
```

---

## 🔄 Skills 组合机制 (规划式)

### 流程图

```
用户: "处理CSV并生成图表"
    ↓
LLM 解析目标 → ["has_dataframe", "has_chart"]
    ↓
当前状态: {"has_csv_file"}
    ↓
对每个目标状态:
    ├─ 找能产生该状态的 Skills
    ├─ 按方法论评分排序
    ├─ 选择最佳 Skill
    ├─ 递归处理前置条件
    └─ 添加到执行计划
    ↓
返回: [Skill("CSV处理"), Skill("数据可视化")]
```

### 伪代码

```python
def plan_skills(user_goal, available_skills, current_state):
    # 1. LLM 解析目标
    required_effects = llm.parse(user_goal)
    # 例: ["has_dataframe", "has_chart"]
    
    # 2. 贪心搜索
    plan = []
    state = current_state.copy()
    
    for target in required_effects:
        if target in state:
            continue
        
        # 找候选 Skills
        candidates = [s for s in available_skills if target in s.effects]
        
        # 评分排序
        best = max(candidates, key=lambda s: score(s))
        
        # 递归处理前置条件
        for precond in best.preconditions:
            if precond not in state:
                sub_plan = plan_skills(precond, available_skills, state)
                plan.extend(sub_plan)
        
        plan.append(best)
        state.update(best.effects)
    
    return plan
```

---

## 🎭 用户交互三级策略

### 决策流程

```
操作发生
    ↓
评估风险 (0-1)
    ↓
    ├─ < 0.3: 静默执行 (不打断)
    ├─ 0.3-0.8: 加入队列 (任务完成时展示)
    └─ > 0.8: 立即确认 (弹窗)
```

### 风险评估规则

```
操作类型          基础风险    影响范围调整
─────────────────────────────────────
artifact_add      0.1        local: ×1, global: ×1.5
skill_update      0.5        local: ×1, global: ×1.5
skill_create      0.6        local: ×1, global: ×1.5
methodology_change 0.9       local: ×1, global: ×1.5
```

### 队列处理

```
任务完成时:
    ↓
检查队列
    ├─ 高风险 (>0.7): 必须确认
    └─ 低风险 (≤0.7): 可选确认,1小时后自动批准
```

---

## 🛡️ 错误处理和容错机制

### 分层错误处理

```
L1: LLM 调用层
  ├─ 网络错误 → 重试(3次,指数退避)
  ├─ API 限流 → 等待 + 降级
  ├─ 响应超时 → 重试 + 缩短 prompt
  └─ 解析错误 → 记录 + 默认值

L2: Skills 执行层
  ├─ Skill 不存在 → 推荐相似 Skills
  ├─ 前置条件不满足 → 自动满足 or 提示
  ├─ 执行失败 → 记录 + 降低 success_rate
  └─ 部分成功 → 返回已完成部分

L3: 知识库层
  ├─ 图查询失败 → 降级到向量搜索
  ├─ 向量搜索失败 → 返回默认 Skills
  ├─ 数据不一致 → 自动修复 or 标记
  └─ 索引损坏 → 重建索引
```

### 核心策略

**1. LLM 调用重试**
```python
def call_llm_with_retry(prompt, max_retries=3):
    for i in range(max_retries):
        try:
            return llm.call(prompt)
        except NetworkError:
            time.sleep(2 ** i)  # 指数退避
        except RateLimitError:
            time.sleep(60)
        except TimeoutError:
            prompt = shorten_prompt(prompt)
    return fallback_response()
```

**2. 优雅降级**
```
完整功能 → 降级功能 → 最小功能

示例:
- 完整: LLM 理解 + Skills 组合 + 执行
- 降级: 规则匹配 + 单个 Skill + 执行
- 最小: 用户手动选择 Skill
```

**3. 错误隔离**
```
单个 Skill 失败 ≠ 整个任务失败

策略:
- 跳过失败的 Skill
- 继续执行其他 Skills
- 最后汇总结果
```

### 用户提示原则

```
1. 清晰: 说明发生了什么
2. 可操作: 告诉用户可以做什么
3. 友好: 不要技术术语

示例:
❌ "VectorSearchError: Index not found"
✅ "抱歉,搜索功能暂时不可用。我会用其他方式帮你查找。"
```

### 实现优先级

**Phase 1 必须**:
- LLM 调用重试机制
- Skills 执行错误处理
- 基础错误日志

**Phase 2 可选**:
- 状态恢复机制
- 完整监控指标
- 自动数据修复

---


## 🔍 关联机制技术实现

### 向量搜索

```
启动时:
    ├─ 加载所有 Skills 的 name + description
    ├─ 向量化 (sentence-transformers)
    └─ 建立索引 (Chroma)

查询时:
    ├─ 向量化用户输入
    ├─ 搜索 Top-K 相似 Skills
    └─ 按需加载完整内容
```

**技术栈**: Chroma + sentence-transformers (all-MiniLM-L6-v2)

### 上下文加权

```
维护上下文:
    ├─ recent_topics: 最近10个关键词
    └─ current_project: 当前项目

查询时:
    ├─ 向量搜索 → 候选 Skills
    ├─ 检查与上下文的匹配度
    └─ 调整得分: base_score + context_boost (最多+0.5)
```

---

## 📝 技术栈

### 核心依赖

```
图数据库:
  - Neo4j (生产)
  - NetworkX (开发/测试)

向量搜索:
  - chromadb
  - sentence-transformers

LLM:
  - anthropic / openai
```

### 性能指标

```
向量索引:
  - 500 Skills → 索引大小 < 10MB
  - 启动时间 < 2s

图查询:
  - 单跳查询 < 50ms
  - 多跳查询 < 200ms
```


## 🔎 查询流程设计 (渐进式)

### Phase 1: 最简方案 (MVP)

```
用户输入
    ↓
向量搜索 → Top-5 Skills
    ↓
方法论评分 → 排序
    ↓
决策:
  ├─ 得分差距 > 0.3: 返回最佳
  └─ 得分差距 < 0.3: 返回 Top-3 供选择
```

**核心假设**: 图结构的邻近关系会自然体现在向量相似度中

**验证指标**:
- 首次命中率 > 80%
- 用户需要选择的频率 < 20%

### Phase 2: 反馈优化 (按需)

```
用户反馈 "不是这个"
    ↓
图结构查询:
  ├─ 找 sibling skills (同方法论下)
  ├─ 找 related skills (调用关系)
  └─ 找 upstream/downstream (前后置)
    ↓
返回新候选
```

**触发条件**:
- 用户明确拒绝
- 首次搜索得分 < 0.5

**实现策略**: 先实现 Phase 1,根据实际效果决定是否需要 Phase 2

---

## ✅ 核心决策总结

1. **Skills 组合**: 规划式 (HTN Planning 简化版)
2. **方法论量化**: 评分机制 + 归一化
3. **用户交互**: 三级策略 (静默/队列/立即)
4. **向量搜索**: Chroma + sentence-transformers
5. **图数据库**: Neo4j(生产) / NetworkX(开发)

---

**版本**: v1.1  
**最后更新**: 2026-01-18  
**状态**: 核心机制已确定,待实现


---

## 🌱 冷启动种子库设计

### 精简方案 (MVP)

**方法论层**: 5个
1. 简单优于复杂
2. 优先使用标准库/成熟工具
3. 保持一致性
4. 从小开始,逐步迭代
5. 记录和复盘

**Skills 层**: 15-20个

```
生活管理 (6个):
├─ 任务分解
├─ 任务跟踪
├─ 日程规划
├─ 笔记整理
├─ 日复盘
└─ 周复盘

数据处理 (6个):
├─ CSV 处理
├─ JSON 处理
├─ 数据清洗
├─ 数据验证
├─ 数据转换
└─ 数据可视化

代码辅助 (3个):
├─ Python 脚本生成
├─ 函数重构
└─ 错误处理

通用工具 (2个):
├─ 文件读写
└─ 命令行调用
```

**副产品层**: 每个 Skill 1个核心副产品

### 生成方式

- 生活管理类: 手工编写(核心价值)
- 其他类: LLM 生成 + 人工审核
- 后续: 从 Claude Skills 库参考优化

### 实施顺序

**Phase 1 (Week 3)**: 5个基础 Skills
- 任务分解, CSV处理, Python脚本生成, 文件读写, 日复盘

**Phase 2 (Week 4)**: 扩展到 15-20个

**后续**: 从使用中学习,自动生成新 Skills
