# docs 目录重组方案

## 📊 当前状态分析

### 当前结构
```
docs/
├── 核心文档 (10个)
│   ├── ARCHITECTURE.md (14KB) - 架构设计
│   ├── CHANGELOG.md (4.8KB) - 更新日志
│   ├── DEVELOPMENT_ENVIRONMENT.md (7.7KB) - 开发环境 ✨ 新增
│   ├── DEVELOPMENT_PLAN.md (1.5KB) - 开发计划
│   ├── DOCUMENTATION_UPDATE_SUMMARY.md (7.5KB) - 文档更新总结 ✨ 新增
│   ├── PROGRESS.md (4KB) - 进度跟踪
│   ├── README.md (856B) - 文档索引
│   ├── SKILL_FORMAT.md (6.4KB) - Skill 格式规范
│   ├── TECHNICAL_DESIGN.md (11KB) - 技术设计
│   └── VECTOR_STORE_OPTIMIZATION.md (6.3KB) - VectorStore 优化 ✨ 新增
│
├── archive/ (4个) - 归档文档
│   ├── advise_by_deepseek.md (5.9KB)
│   ├── DEVELOPMENT.md (6KB)
│   ├── FAILURE_LEARNING.md (7.7KB)
│   └── LEARNING.md (4.9KB)
│
├── plans/ (6个) - 开发计划
│   ├── README.md (5KB)
│   ├── phase1-knowledge-base.md (7KB)
│   ├── phase2-io-layer.md (2.4KB)
│   ├── phase3-evolution.md (2.5KB)
│   ├── phase4-ui.md (1.2KB)
│   └── phase5-production.md (1.3KB)
│
├── research/ (2个) - 调研文档
│   ├── knowledge_graph_tools.md (11.6KB)
│   └── obsidian_skills_analysis.md (14.9KB)
│
└── weekly/ (1个) - 周报
    └── WEEK1_SUMMARY.md (4.5KB)
```

**总计**: 23 个文档

---

## 🎯 精简目标

### 问题分析
1. **核心文档过多** (10个) - 部分文档可以合并或归档
2. **临时文档未归档** - DOCUMENTATION_UPDATE_SUMMARY.md 是临时总结
3. **重复内容** - DEVELOPMENT_PLAN.md 和 plans/ 目录有重复
4. **过时文档** - TECHNICAL_DESIGN.md 部分内容已过时

### 精简原则
- ✅ 保留：活跃使用的核心文档
- 📦 归档：历史记录、临时总结、过时设计
- 🔄 合并：内容重复的文档
- 🗑️ 删除：无价值的临时文件

---

## 📋 重组方案

### 方案 A: 激进精简（推荐）

#### 核心文档保留 (6个)
```
docs/
├── README.md - 文档导航（需更新）
├── CHANGELOG.md - 更新日志
├── DEVELOPMENT_ENVIRONMENT.md - 开发环境配置
├── ARCHITECTURE.md - 系统架构（需更新）
├── SKILL_FORMAT.md - Skill 格式规范
└── VECTOR_STORE_OPTIMIZATION.md - 最新优化说明
```

#### 归档文档 (移动到 archive/)
```
archive/
├── 2026-01/
│   ├── DOCUMENTATION_UPDATE_SUMMARY.md - 文档更新总结
│   ├── PROGRESS.md - 进度快照（2026-01-28）
│   ├── WEEK1_SUMMARY.md - Week 1 总结
│   ├── TECHNICAL_DESIGN.md - 技术设计 v1.1
│   └── DEVELOPMENT_PLAN.md - 开发计划 v1.0
│
├── advise_by_deepseek.md
├── DEVELOPMENT.md
├── FAILURE_LEARNING.md
└── LEARNING.md
```

#### 计划文档 (保持)
```
plans/
├── README.md
├── phase1-knowledge-base.md
├── phase2-io-layer.md
├── phase3-evolution.md
├── phase4-ui.md
└── phase5-production.md
```

#### 调研文档 (保持)
```
research/
├── knowledge_graph_tools.md
└── obsidian_skills_analysis.md
```

**结果**: 23 → 16 个文档（-7个）

---

### 方案 B: 温和精简

#### 核心文档保留 (8个)
```
docs/
├── README.md
├── CHANGELOG.md
├── DEVELOPMENT_ENVIRONMENT.md
├── PROGRESS.md - 保留，持续更新
├── ARCHITECTURE.md
├── SKILL_FORMAT.md
├── TECHNICAL_DESIGN.md - 保留，标注版本
└── VECTOR_STORE_OPTIMIZATION.md
```

#### 归档文档
```
archive/
├── 2026-01/
│   ├── DOCUMENTATION_UPDATE_SUMMARY.md
│   ├── WEEK1_SUMMARY.md
│   └── DEVELOPMENT_PLAN.md
│
├── advise_by_deepseek.md
├── DEVELOPMENT.md
├── FAILURE_LEARNING.md
└── LEARNING.md
```

**结果**: 23 → 19 个文档（-4个）

---

## 🎯 推荐方案：方案 A（激进精简）

### 理由
1. **PROGRESS.md** → 归档
   - 内容是 Week 1 的快照，不会再更新
   - CHANGELOG.md 已经记录了进度

2. **TECHNICAL_DESIGN.md** → 归档
   - 设计文档版本 v1.1，部分内容已过时
   - ARCHITECTURE.md 和 VECTOR_STORE_OPTIMIZATION.md 已包含最新设计

3. **DEVELOPMENT_PLAN.md** → 归档
   - 内容与 plans/ 目录重复
   - plans/ 目录更详细和结构化

4. **DOCUMENTATION_UPDATE_SUMMARY.md** → 归档
   - 临时总结文档，记录了 2026-01-28 的更新
   - 归档后作为历史记录保存

5. **WEEK1_SUMMARY.md** → 归档
   - Week 1 已完成，是历史记录
   - 移到 archive/2026-01/ 更合理

### 优势
- ✅ 核心文档清晰（6个）
- ✅ 历史记录完整（archive/2026-01/）
- ✅ 易于维护和查找
- ✅ 新人友好（文档少而精）

---

## 📝 执行步骤

### 1. 创建归档目录
```bash
mkdir -p docs/archive/2026-01
```

### 2. 移动文档到归档
```bash
# 移动到 archive/2026-01/
mv docs/DOCUMENTATION_UPDATE_SUMMARY.md docs/archive/2026-01/
mv docs/PROGRESS.md docs/archive/2026-01/
mv docs/TECHNICAL_DESIGN.md docs/archive/2026-01/
mv docs/DEVELOPMENT_PLAN.md docs/archive/2026-01/
mv docs/weekly/WEEK1_SUMMARY.md docs/archive/2026-01/

# 删除空目录
rmdir docs/weekly
```

### 3. 更新 docs/README.md
添加归档说明和文档导航

### 4. 更新 archive/README.md
说明归档结构和查找方法

### 5. Git 提交
```bash
git add docs/
git commit -m "docs: 精简文档结构，归档历史文档到 archive/2026-01/"
git push
```

---

## 🔗 更新后的文档结构

```
docs/
├── README.md                          # 📖 文档导航（需更新）
├── CHANGELOG.md                       # 📝 更新日志
├── DEVELOPMENT_ENVIRONMENT.md         # 🔧 开发环境配置
├── ARCHITECTURE.md                    # 🏗️ 系统架构
├── SKILL_FORMAT.md                    # 📋 Skill 格式规范
├── VECTOR_STORE_OPTIMIZATION.md       # ⚡ VectorStore 优化
│
├── archive/                           # 📦 归档文档
│   ├── README.md                      # 归档说明
│   ├── 2026-01/                       # 2026年1月归档
│   │   ├── DOCUMENTATION_UPDATE_SUMMARY.md
│   │   ├── PROGRESS.md
│   │   ├── TECHNICAL_DESIGN.md
│   │   ├── DEVELOPMENT_PLAN.md
│   │   └── WEEK1_SUMMARY.md
│   ├── advise_by_deepseek.md
│   ├── DEVELOPMENT.md
│   ├── FAILURE_LEARNING.md
│   └── LEARNING.md
│
├── plans/                             # 📅 开发计划
│   ├── README.md
│   ├── phase1-knowledge-base.md
│   ├── phase2-io-layer.md
│   ├── phase3-evolution.md
│   ├── phase4-ui.md
│   └── phase5-production.md
│
└── research/                          # 🔬 调研文档
    ├── knowledge_graph_tools.md
    └── obsidian_skills_analysis.md
```

**核心文档**: 6 个  
**总文档数**: 16 个（-7个）

---

## ✅ 验证清单

- [ ] 创建 archive/2026-01/ 目录
- [ ] 移动 5 个文档到归档
- [ ] 删除空的 weekly/ 目录
- [ ] 更新 docs/README.md
- [ ] 创建/更新 archive/README.md
- [ ] Git 提交和推送
- [ ] 验证所有链接正确

---

**创建时间**: 2026-01-28 09:45  
**方案**: 激进精简（推荐）  
**预期效果**: 文档清晰、易维护、新人友好
