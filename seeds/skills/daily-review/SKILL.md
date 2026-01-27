---
name: daily-review
description: 每日工作和学习的回顾总结。当用户提到日复盘、每日总结、今日回顾、工作记录时使用。
metadata:
  id: skill_daily_review
  display_name: 日复盘
  preconditions:
    - has_daily_activities
  effects:
    - has_review_notes
  methodology_scores:
    meth_reflect: 0.9
    meth_iterate: 0.8
  parent_methodologies:
    - meth_reflect
    - meth_iterate
  called_skills: []
  tags:
    - life-management
    - review
    - productivity
  version: "1.0.0"
  author: MindFlow
---

# 日复盘

## 概述

每日工作和学习的回顾总结。通过结构化的复盘流程，帮助积累经验、发现问题、持续改进。

## 执行步骤

1. 回顾今天完成的任务
2. 记录遇到的问题和解决方案
3. 总结学到的经验教训
4. 规划明天的重点任务
5. 输出结构化的复盘记录

## 复盘模板

```markdown
# 日复盘 - {{date}}

## 今日完成
- [ ] 任务1
- [ ] 任务2

## 遇到的问题
1. 问题描述
   - 解决方案：...

## 经验教训
- 学到了什么
- 下次可以改进的地方

## 明日计划
1. 重点任务1
2. 重点任务2

## 心情/状态
😊 / 😐 / 😔
```

## 最佳实践

### 固定时间
- 建议在每天结束工作前 15-30 分钟进行
- 保持一致的时间有助于养成习惯

### 聚焦重点
- 不需要记录所有细节
- 关注有价值的经验和教训

### 行动导向
- 每个问题都要有解决方案或下一步行动
- 明日计划要具体可执行
