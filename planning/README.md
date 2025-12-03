# 📋 Mindflow 项目规划版本管理

## 概述

此目录用于管理Mindflow项目规划文档的版本历史，记录项目研发的全流程演变。

## 目录结构

```
planning/
├── README.md                          # 本文件，版本管理说明
├── VERSIONS.md                        # 版本索引和历史记录
├── CHANGELOG.md                       # 详细的变更日志
├── v1.0/                             # 版本1.0文件夹
│   ├── PLAN.md                       # 该版本的完整规划
│   ├── SUMMARY.md                    # 该版本的总结
│   └── TIMESTAMP.txt                 # 版本创建时间
├── v1.1/                             # 版本1.1文件夹
│   ├── PLAN.md
│   ├── SUMMARY.md
│   ├── CHANGES.md                    # 相比v1.0的变更
│   └── TIMESTAMP.txt
└── archive/                          # 存档的旧版本
    └── ...
```

## 版本命名规则

- **主版本号**（Major）：产品大方向或核心功能改变
  - v1.x: MVP阶段（生活记录 + 计划 + 复盘）
  - v2.x: 知识库阶段（添加知识库功能）
  - v3.x: 多用户阶段（支持多用户）

- **次版本号**（Minor）：功能补充或优化
  - v1.0: 初始版本
  - v1.1: 阶段反馈修订
  - v1.2: 进一步优化
  - ...

## 当前版本

**最新版本**: v1.0（2024-12-03）

### v1.0 的内容
- ✅ 9阶段完整规划（产品调研 → 用户隔离架构）
- ✅ 6个开发阶段（Phase 1-6），共9-10周
- ✅ 完整的数据库设计（7个核心表）
- ✅ 4层复盘提示系统
- ✅ 11个初始化问卷问题
- ✅ 详细的检查清单
- ✅ 用户登录和隔离的架构预留

## 版本创建流程

每当项目有重大更新或阶段完成时，按以下步骤创建新版本：

### 1. 创建版本文件夹
```bash
mkdir -p planning/v1.1
```

### 2. 复制更新后的PLAN
```bash
cp PLAN.md planning/v1.1/PLAN.md
```

### 3. 创建SUMMARY（一页纸总结）
```bash
# planning/v1.1/SUMMARY.md
# 包含：
# - 版本目标
# - 主要更新内容
# - 关键决策
# - 已完成的任务
# - 待处理的项目
```

### 4. 创建CHANGES（相比上一版本的变更）
```bash
# planning/v1.1/CHANGES.md
# 包含：
# - 新增内容
# - 修改内容
# - 删除内容
# - 理由说明
```

### 5. 创建TIMESTAMP
```bash
date > planning/v1.1/TIMESTAMP.txt
```

### 6. 更新VERSIONS.md和CHANGELOG.md
```bash
# 添加新版本信息
```

## 何时创建新版本

- 📌 **完成某个Phase开发**
  - Phase 1完成 → v1.0.1
  - Phase 2完成 → v1.0.2

- 📌 **阶段反馈和修订**
  - 用户反馈修订 → v1.1
  - 技术方案优化 → v1.2

- 📌 **重大决策变更**
  - MVP范围调整 → v2.0
  - 技术栈更换 → v2.0
  - 架构重构 → v2.0

- 📌 **项目里程碑**
  - MVP完成 → v1.5
  - 生产发布 → v2.0

## 版本之间的关系

```
v1.0 (2024-12-03) - 初始规划版本
  ↓
v1.0.1 - Phase 1完成后
  ↓
v1.0.2 - Phase 2完成后
  ↓
v1.0.3 - Phase 3完成后
  ...
v1.5 - MVP完成时
  ↓
v2.0 - 知识库功能规划
  ↓
v3.0 - 多用户功能规划
```

## 查看历史版本

### 查看所有版本
```bash
cat planning/VERSIONS.md
```

### 查看版本的变更
```bash
cat planning/v1.1/CHANGES.md
```

### 对比两个版本
```bash
diff planning/v1.0/PLAN.md planning/v1.1/PLAN.md
```

### 查看版本时间线
```bash
ls -la planning/v*/TIMESTAMP.txt
```

## 版本管理最佳实践

### 1. 保持PLAN.md同步
```
当前开发使用：PLAN.md（根目录）
版本存档：planning/vX.X/PLAN.md（只读参考）
```

### 2. 定期总结
- 每完成一个Phase后创建版本
- 每个月回顾一次是否需要创建新版本
- 大的决策变更后立即创建版本

### 3. 清晰的变更说明
```markdown
# v1.1 变更说明

## 相比v1.0的改进

### 新增
- [ ] 新增特性1的描述
- [ ] 新增特性2的描述

### 修改
- [ ] 修改项1：旧内容 → 新内容（理由）
- [ ] 修改项2：...

### 删除
- [ ] 删除项1：原因说明
- [ ] 删除项2：...

## 完成的任务
- ✅ 任务1
- ✅ 任务2

## 后续计划
- ⏳ 下一步任务1
- ⏳ 下一步任务2
```

### 4. 完整的SUMMARY
```markdown
# v1.1 总结

## 目标
描述这个版本的主要目标

## 完成情况
- ✅ 目标1完成
- ✅ 目标2完成

## 核心变更
1. 变更项1
2. 变更项2

## 统计数据
- 文档行数：xxxx
- Phase数：6
- 表数：7
- 检查项：xxx

## 下一个版本的预期
- 计划何时发布
- 预期的主要变更
```

## 使用git追踪版本

### 创建tag
```bash
git tag -a v1.0 -m "Initial Mindflow plan: 9-stage planning with 6 development phases"
git tag -a v1.1 -m "Phase 1 completed: Framework setup verified"
git push origin --tags
```

### 查看tags
```bash
git tag -l
git show v1.0
```

## 查询和检索

### 按主题查询版本
```bash
# 查询所有包含"用户画像"修改的版本
grep -r "用户画像" planning/v*/CHANGES.md
```

### 按时间查询
```bash
# 查看2024年12月的所有版本
ls -la planning/v*/ | grep "Dec"
```

### 按关键词查询
```bash
# 查询所有包含"数据库"的版本总结
grep -l "数据库" planning/v*/SUMMARY.md
```

## 版本发布流程

### 1. 检查准备
- [ ] 所有Phase任务完成
- [ ] 相关文档已更新
- [ ] 变更清单已填写

### 2. 创建版本
- [ ] 创建新版本文件夹
- [ ] 复制PLAN.md
- [ ] 编写SUMMARY
- [ ] 编写CHANGES

### 3. 更新索引
- [ ] 更新VERSIONS.md
- [ ] 更新CHANGELOG.md
- [ ] 创建git tag

### 4. 存档旧版本
- [ ] 移动到archive/（如果不常用）
- [ ] 保留README说明为什么归档

## 故障排除

### 如何恢复到旧版本？
```bash
# 查看旧版本内容
cat planning/v1.0/PLAN.md

# 恢复到某个历史版本（基于git）
git checkout v1.0 -- PLAN.md
```

### 如何合并两个版本的变更？
```bash
# 手动合并 - 查看CHANGES.md理解变更
# 然后在PLAN.md中应用需要的改动
```

### 如何处理版本冲突？
- 在CONFLICTS.md中记录冲突内容
- 讨论并决议如何处理
- 在新版本中明确说明决议

## 联系和反馈

如果有关于版本管理的建议：
1. 在FEEDBACK.md中记录
2. 在下一个版本时纳入改进

---

## 快速参考

| 操作 | 命令 |
|------|------|
| 查看所有版本 | `cat planning/VERSIONS.md` |
| 查看最新版本 | `cat planning/v1.0/PLAN.md` |
| 创建新版本 | `mkdir planning/v1.1` |
| 对比版本 | `diff planning/v1.0/PLAN.md planning/v1.1/PLAN.md` |
| 查看版本变更 | `cat planning/v1.1/CHANGES.md` |
| 查看版本总结 | `cat planning/v1.1/SUMMARY.md` |

---

**文档最后更新**: 2024-12-03
**维护者**: Project Team
