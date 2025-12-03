# 📚 规划版本管理 - 快速开始

> 记录Mindflow项目从规划到实现的完整演变过程

## 🎯 目的

为项目保留清晰的版本历史，包括：
- ✅ 每个阶段的规划快照
- ✅ 相比前一版本的详细变更
- ✅ 开发过程中的重要决策
- ✅ 项目演进的完整记录

## 🗂️ 当前结构

```
planning/
├── README.md                    # 完整的版本管理指南
├── VERSIONS.md                  # 版本时间线和索引
├── VERSION_TEMPLATE.md          # 创建新版本的模板
├── QUICK_START.md              # 本文件（快速开始）
└── v1.0/                        # 版本1.0文件夹
    ├── PLAN.md                 # 完整规划文档
    ├── SUMMARY.md              # 版本总结（一页纸）
    └── TIMESTAMP.txt           # 创建时间
```

## 🚀 常见操作

### 1️⃣ 查看当前版本的规划
```bash
cat planning/v1.0/PLAN.md
```

### 2️⃣ 了解当前版本的要点
```bash
cat planning/v1.0/SUMMARY.md
```

### 3️⃣ 查看所有版本时间线
```bash
cat planning/VERSIONS.md
```

### 4️⃣ 查看版本管理完整指南
```bash
cat planning/README.md
```

## 📅 版本时间线

当前版本及预期版本：

| 版本 | 发布日期 | 阶段 | 状态 |
|------|---------|------|------|
| v1.0 | 2024-12-03 | 初始规划 | ✅ 完成 |
| v1.0.1 | 预期：2024-12-09 | Phase 1完成 | ⏳ 待开发 |
| v1.0.2 | 预期：2024-12-23 | Phase 2完成 | ⏳ 待开发 |
| v1.0.3 | 预期：2025-01-06 | Phase 3完成 | ⏳ 待开发 |
| v1.0.4 | 预期：2025-01-20 | Phase 4完成 | ⏳ 待开发 |
| v1.0.5 | 预期：2025-02-03 | Phase 5完成 | ⏳ 待开发 |
| v1.5 | 预期：2025-02-17 | MVP发布 | ⏳ 待开发 |

## 📋 v1.0 快速概览

**发布日期**: 2024-12-03

### 核心内容
- ✅ 9阶段完整规划
- ✅ 6个开发Phase（9-10周）
- ✅ 完整的系统架构设计
- ✅ 4个LangGraph Agent的工作流
- ✅ 7个数据库表的Schema
- ✅ 详细的检查清单和提示词

### 关键数字
- 📄 文档行数：1548
- 📊 数据库表：7个
- 🤖 Agent数：4个
- 📋 检查项：70+
- ⏱️ 开发周期：9-10周
- 🎯 支持的LLM：4个

### 核心决策
- **技术栈**: Gradio + LangGraph + SQLite + Claude Haiku 4.5
- **MVP范围**: 生活记录 + 计划 + 复盘
- **部署方式**: Docker + Linux自建服务器

## 🎓 如何使用版本管理系统

### 情景1：我想看项目规划
```bash
# 查看最新版本的完整规划
cat planning/v1.0/PLAN.md

# 也可以查看根目录的PLAN.md（两者相同）
cat PLAN.md
```

### 情景2：我想了解版本间的变化
```bash
# 查看v1.0.1相比v1.0的变化（发布后）
cat planning/v1.0.1/CHANGES.md

# 或对比两个版本
diff planning/v1.0/PLAN.md planning/v1.0.1/PLAN.md
```

### 情景3：我想追踪项目进度
```bash
# 查看版本时间线
cat planning/VERSIONS.md

# 查看每个版本的完成情况
cat planning/v1.0/SUMMARY.md
cat planning/v1.0.1/SUMMARY.md  # 发布后
```

### 情景4：我要创建新版本（如Phase 1完成）
```bash
# 1. 阅读模板
cat planning/VERSION_TEMPLATE.md

# 2. 创建新版本文件夹
mkdir -p planning/v1.0.1

# 3. 复制PLAN.md
cp PLAN.md planning/v1.0.1/PLAN.md

# 4. 创建SUMMARY和CHANGES（使用模板）
# 参考 VERSION_TEMPLATE.md 中的模板内容

# 5. 创建时间戳
date > planning/v1.0.1/TIMESTAMP.txt

# 6. 更新索引
# 编辑 planning/VERSIONS.md 添加新版本信息

# 7. 提交到git
git add planning/v1.0.1/
git commit -m "Release v1.0.1: Phase 1 completed"
git tag -a v1.0.1 -m "Phase 1 completed: Framework setup verified"
```

## 🔍 快速查询

### 按时间查找
```bash
# 查看v1.0创建的时间
cat planning/v1.0/TIMESTAMP.txt

# 查看所有版本的时间
for f in planning/v*/TIMESTAMP.txt; do echo "=== $f ==="; cat $f; done
```

### 按内容查找
```bash
# 查找所有包含"用户画像"的版本
grep -l "用户画像" planning/v*/PLAN.md

# 查找所有变更中提到"性能"的地方
grep -r "性能" planning/v*/CHANGES.md
```

### 按阶段查找
```bash
# 查找Phase 1相关的版本
grep -l "Phase 1" planning/v*/SUMMARY.md
```

## 📊 版本统计

### v1.0统计
- **文档大小**: ~60KB
- **代码示例**: 10+
- **数据库表**: 7个
- **开发时间**: 9-10周
- **检查清单项**: 70+

## 🔄 工作流程

```
基于根目录的 PLAN.md 进行开发
        ↓
每个Phase完成时
        ↓
创建新版本快照 (vX.X)
  ├─ 复制更新后的PLAN.md
  ├─ 编写SUMMARY（总结）
  ├─ 编写CHANGES（变更）
  └─ 创建TIMESTAMP
        ↓
更新VERSIONS.md索引
        ↓
创建git tag
        ↓
继续开发下一个Phase
```

## ✨ 版本管理的好处

1. **清晰的演进轨迹**
   - 看到项目是如何一步步发展的
   - 了解每个版本的里程碑

2. **便于回溯**
   - 需要参考之前的设计决策？
   - 想了解当时是如何解决某个问题的？

3. **知识积累**
   - 记录开发过程中的经验教训
   - 为未来的项目提供参考

4. **团队协作**
   - 新加入的成员可以快速了解项目历史
   - 通过版本变更理解项目演进

## 📝 版本号含义

- **v1.0**: 初始规划版本
- **v1.0.1, v1.0.2, ...**: Phase完成版本
- **v1.5**: MVP完整版本
- **v2.0**: 新阶段（知识库等）
- **v3.0**: 重大变更（多用户等）

## 🎯 何时创建新版本

- ✅ **一定要创建**：
  - Phase完成时
  - 重大功能上线时
  - MVP发布时

- ⭐ **建议创建**：
  - 有大量用户反馈修订时
  - 重要的架构优化时
  - 性能显著提升时

- ⏸️ **可选创建**：
  - 小的bug修复
  - 文档更新
  - 代码清理

## 🚨 注意事项

### 关于PLAN.md
- **根目录的PLAN.md**: 用于开发时参考，可以动态修改
- **planning/vX.X/PLAN.md**: 版本快照，记录该时刻的完整规划

### 关于更新频率
- 根目录PLAN.md：开发中可随时修改
- 版本快照：Phase完成后创建，不修改

### 关于git管理
- 每个版本创建时创建git tag
- planning目录纳入版本控制
- 可通过git查看任何历史版本

## 🔗 相关文件导航

| 文件 | 用途 | 位置 |
|------|------|------|
| PLAN.md | 当前完整规划 | 根目录 |
| README.md | 版本管理完整指南 | planning/ |
| VERSIONS.md | 版本时间线和索引 | planning/ |
| VERSION_TEMPLATE.md | 创建新版本的模板 | planning/ |
| v1.0/PLAN.md | v1.0版本快照 | planning/v1.0/ |
| v1.0/SUMMARY.md | v1.0版本总结 | planning/v1.0/ |
| QUICK_START.md | 本文件 | planning/ |

## 💬 常见问题

**Q: 我想修改当前的规划（PLAN.md），应该修改哪个？**
A: 修改根目录的PLAN.md。版本文件夹中的是快照，不应修改。

**Q: 如果觉得v1.0的某些决策不对怎么办？**
A: 在根目录的PLAN.md中修改，然后在创建v1.0.1时通过CHANGES.md记录改进说明。

**Q: 多久创建一个新版本？**
A: 建议每个Phase完成后创建一个版本。如果项目进度快，可以更频繁。

**Q: 版本文件会很大吗？**
A: 不会。每个版本只是规划文档的快照，通常几KB到几十KB。

**Q: 可以删除旧版本吗？**
A: 可以移到archive/文件夹，但建议保留。它们占用空间很小，但提供很大的参考价值。

## 🎬 快速操作命令

```bash
# 查看当前规划
cat PLAN.md | head -100

# 查看v1.0总结
cat planning/v1.0/SUMMARY.md

# 查看所有版本
ls planning/v*/SUMMARY.md

# 创建新版本（参考模板）
# mkdir -p planning/v1.0.1
# cp PLAN.md planning/v1.0.1/PLAN.md
# [编辑SUMMARY和CHANGES]

# 查看版本时间线
cat planning/VERSIONS.md | head -50

# 对比两个版本（发布后）
# diff planning/v1.0/PLAN.md planning/v1.0.1/PLAN.md
```

---

## 🎉 总结

你现在拥有一个完整的版本管理系统来记录Mindflow的演变过程。从规划 → 开发 → 发布，每一步都有清晰的记录。

**现在可以**：
1. ✅ 查看v1.0的完整规划
2. ✅ 了解项目的版本时间线
3. ✅ 跟踪项目进度
4. ✅ 为每个阶段创建版本快照

**下一步**：
1. 💻 开始Phase 1开发
2. 📊 定期检查进度
3. 📝 Phase完成时创建新版本

---

**快速开始完成！** 🎊

有问题？查看：
- 详细指南：`planning/README.md`
- 版本时间线：`planning/VERSIONS.md`
- 创建模板：`planning/VERSION_TEMPLATE.md`

