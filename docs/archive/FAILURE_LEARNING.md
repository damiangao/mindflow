# 失败学习机制设计文档

> **基于**: ARCHITECTURE.md v1.0, TECHNICAL_DESIGN.md v1.1  
> **版本**: v1.0  
> **日期**: 2026-01-20  
> **状态**: 设计中

---

## 🎯 目标

让系统从"失败→重试→成功"的完整链条中学习，而不仅仅记录最终结果。

---

## 📊 三层设计

```
┌─────────────────────────────────────┐
│  1. 失败记录 (数据层)                │
│  - Artifact: execution_history      │
│  - Skill: failure_patterns          │
└─────────────────────────────────────┘
            ↓ 输入
┌─────────────────────────────────────┐
│  2. 执行轨迹 (上下文层)              │
│  - 完整的 失败→重试→成功 链条        │
│  - 每次尝试的输入/输出/修复动作       │
└��────────────────────────────────────┘
            ↓ 输入
┌─────────────────────────────────────┐
│  3. 复盘触发 (机制层)                │
│  - 执行后立即触发: Self-Verification │
│  - 定时/任务结束触发: 整体分析        │
└─────────────────────────────────────┘
            ↓ 输出
┌─────────────────────────────────────┐
│  改进建议                            │
│  - 更新 Skill 权重/instructions      │
│  - 更新 Methodology 权重             │
│  - 生成新的 failure_patterns         │
└─────────────────────────────────────┘
```

---

## 1️⃣ 失败记录 (数据层)

### Artifact 层: execution_history

记录代码/模板的调用结果。

```python
Artifact {
    # ... 原有字段 ...
    
    execution_history: List[ExecutionRecord]
}

ExecutionRecord {
    timestamp: datetime
    success: bool
    error: str | None          # 失败时的错误信息
    context_hash: str          # 调用时的上下文摘要
}
```

**用途**: 
- 统计 Artifact 在不同上下文下的成功率
- 识别"在某些条件下总是失败"的模式

### Skill 层: failure_patterns

记录方法在什么条件下失败。

```python
Skill {
    # ... 原有字段 ...
    
    failure_patterns: List[FailurePattern]
}

FailurePattern {
    condition: str             # 失败条件描述 (如 "输入含中文时")
    error_type: str            # 错误类型
    frequency: int             # 发生次数
    last_occurred: datetime
    suggested_fix: str | None  # 已知的修复方法
}
```

**用途**:
- 执行前检查是否命中已知失败模式
- 提前警告或自动应用修复

---

## 2️⃣ 执行轨迹 (上下文层)

记录 Skill 执行的完整过程，包括所有重试。

```python
ExecutionTrace {
    id: str
    skill_id: str
    task_id: str               # 所属任务
    
    attempts: List[Attempt]    # 所有尝试，包括失败的
    final_success: bool
    
    created_at: datetime
    duration_ms: int           # 总耗时
}

Attempt {
    index: int                 # 第几次尝试 (从1开始)
    timestamp: datetime
    
    # 输入
    context: dict              # 当时的输入/环境
    activated_artifacts: List[str]  # 使用了哪些 Artifact
    
    # 输出
    result: str
    success: bool
    error: str | None
    
    # 修复 (如果是重试)
    fix_applied: str | None    # 应用了什么修复
    fix_source: str | None     # 修复来源: "self_correction" | "user_hint" | "failure_pattern"
}
```

### 关键场景

**场景1: 一次成功**
```
attempts: [
    {index: 1, success: true}
]
final_success: true
```
→ 正常记录，无需特殊处理

**场景2: 失败→重试→成功** ⭐ 最有学习价值
```
attempts: [
    {index: 1, success: false, error: "编码错误"},
    {index: 2, success: true, fix_applied: "添加 encoding='utf-8'"}
]
final_success: true
```
→ 复盘时重点分析，提取 failure_pattern

**场景3: 多次失败→放弃**
```
attempts: [
    {index: 1, success: false, error: "..."},
    {index: 2, success: false, error: "..."},
    {index: 3, success: false, error: "..."}
]
final_success: false
```
→ 降低 Skill 成功率，标记需要人工介入

---

## 3️⃣ 复盘触发 (机制层)

### 触发时机

| 时机 | 触发条件 | 处理内容 |
|------|----------|----------|
| **即时** | 每次执行后 | Self-Verification，即时纠错 |
| **任务结束** | 任务完成时 | 分析本次任务的所有 traces |
| **定时** | 每日/每周 | 整体分析，更新权重 |

### 即时复盘 (Self-Verification)

```
执行完成
    ↓
检查结果是否符合预期
    ├─ 符合 → 记录成功
    └─ 不符合 → 
        ├─ 尝试自动修复 (最多3次)
        └─ 记录失败原因
```

### 任务结束复盘

```
任务完成
    ↓
收集本任务所有 ExecutionTrace
    ↓
筛选: final_success=true && len(attempts) > 1
    ↓
对每个 trace:
    ├─ 分析失败原因
    ├─ 提取修复模式
    └─ 生成/更新 failure_pattern
    ↓
更新 Skill 的 success_rate
```

### 定时复盘

```
定时触发 (如每日凌晨)
    ↓
收集最近 N 天的所有 traces
    ↓
统计分析:
    ├─ 各 Skill 成功率变化
    ├─ 高频失败模式
    └─ Methodology 有效性
    ↓
输出:
    ├─ 更新 Skill 权重
    ├─ 更新 Methodology 权重
    └─ 生成改进建议报告
```

---

## 🔄 数据流

```
执行 Skill
    ↓
记录 Attempt
    ↓
失败? ─────────────────────┐
    ↓ 是                    │
查找匹配的 failure_pattern  │
    ↓                       │
有修复建议? ────────────────┤
    ↓ 是                    │
应用修复，重试              │
    ↓                       │
←──────────────────────────┘
    ↓
执行结束
    ↓
保存 ExecutionTrace
    ↓
即时复盘 (Self-Verification)
    ↓
任务结束时: 任务复盘
    ↓
定时: 整体复盘
```

---

## 📝 实现优先级

### Phase 1 (MVP)

- [ ] ExecutionTrace 数据结构
- [ ] 基础记录功能 (每次执行记录 trace)
- [ ] 即时复盘 (Self-Verification)

### Phase 2

- [ ] failure_patterns 数据结构
- [ ] 任务结束复盘
- [ ] 失败模式匹配和自动修复

### Phase 3

- [ ] 定时复盘
- [ ] Methodology 权重更新
- [ ] 改进建议报告

---

## ✅ 核心原则

1. **完整链条**: 记录失败→重试→成功的完整过程，不只是最终结果
2. **学习价值**: 优先分析"踩过坑又爬出来"的案例
3. **渐进改进**: 从简单记录开始，逐步增加分析能力
4. **低侵入**: 不影响正常执行流程，异步处理复盘

---

**版本**: v1.0  
**最后更新**: 2026-01-20  
**状态**: 设计中，待评审
