# Mindflow 文档策略

## 概述

Mindflow采取分层文档策略，平衡开源透明度和用户隐私。本文件说明如何管理公开和私有文档。

## 文档分类

### 公开文档（适合GitHub发布）

这些文档提供技术信息，不包含用户个人细节。

#### 📄 docs/ARCHITECTURE.md
**内容**：系统架构设计、数据库模式、Agent设计、工作流
**隐私评级**：✅ 安全发布
**理由**：纯技术设计，无用户特定信息

#### 📄 docs/DEVELOPMENT.md
**内容**：开发阶段规划（Phase 1-6）、任务清单、技术决策
**隐私评级**：✅ 安全发布
**理由**：通用开发指南，已删除"~5事件/天"等用户特定数据
**已修改**：
- 替换了具体的使用场景为通用表述
- 去除了关于个别用户需求的描述

#### 📄 docs/DATABASE.md
**内容**：表结构定义、SQL示例、字段说明、备份策略
**隐私评级**：✅ 安全发布
**理由**：通用数据库设计，无个人数据示例

#### 📄 docs/LLM_CONFIG.md
**内容**：LLM提供商配置、API密钥管理、成本估算、切换指南
**隐私评级**：✅ 安全发布
**理由**：技术配置指南，包含安全建议但无个人信息

#### 📄 docs/DEPLOYMENT.md
**内容**：部署步骤、Docker配置、备份恢复、安全建议
**隐私评级**：✅ 安全发布
**理由**：通用部署指南，适用于所有用户

#### 📄 docs/README.md
**内容**：文档导航、快速开始、常见问题、技术栈概览
**隐私评级**：✅ 安全发布
**理由**：总览文档，引导用户查阅特定文档

### 私有文档（保留本地）

这些文档包含用户特定信息，不应发布到公开仓库。

#### 📋 PLAN.md（根目录）
**内容**：
- 用户具体需求：需要push和督促、行动力较差
- 具体使用场景：~5事件/天、~3活跃计划
- 11问初始化问卷（包含个人问题）
- 完整的9阶段计划
- 提示词模板示例

**隐私风险等级**：🔴 高
**为什么私有**：
- 包含用户个人特征和自我评价
- 反映用户的困难和弱点
- 初始化问卷包含敏感个人信息
- 不适合公开讨论

**保留位置**：
- ✓ 保持在仓库中作为开发参考
- ✓ 添加到 .gitignore（防止提交到GitHub）
- 或完全保存在本地（不在仓库中）

**使用场景**：
- 开发时参考用户具体需求
- 优化提示词时使用示例
- 评估开发进度和范围

#### 📋 其他私有文件（如有）
- 用户测试记录
- 个人邮件或通信记录
- API密钥和敏感配置
- 性能测试结果（如包含个人信息）

---

## GitHub发布检查清单

在将文档上传到GitHub前，使用此清单确保内容安全：

### 内容检查

- [ ] **移除用户特定数据**
  - [ ] 删除具体的使用量数据（"~5事件/天"）
  - [ ] 删除用户特征描述（"行动力较差"）
  - [ ] 删除个人需求（"需要push和督促"）

- [ ] **移除敏感信息**
  - [ ] 没有实际的API密钥
  - [ ] 没有真实的用户名或邮箱
  - [ ] 没有个人问卷内容

- [ ] **保留技术价值**
  - [ ] 系统架构清晰
  - [ ] 实现指南详细
  - [ ] 决策说明充分

### 文件检查

- [ ] 检查代码示例中没有敏感信息
- [ ] 检查JSON示例中没有真实数据
- [ ] 检查SQL示例使用通用字段名
- [ ] 检查配置文件示例使用占位符

---

## 文件管理建议

### 版本控制

```
mindflow/
├── docs/                          # 公开文档（可发布）
│   ├── ARCHITECTURE.md            # ✅ 安全
│   ├── DEVELOPMENT.md             # ✅ 安全（已清理）
│   ├── DATABASE.md                # ✅ 安全
│   ├── LLM_CONFIG.md              # ✅ 安全
│   ├── DEPLOYMENT.md              # ✅ 安全
│   ├── README.md                  # ✅ 安全
│   └── DOCUMENTATION_STRATEGY.md  # ✅ 本文件
│
├── PLAN.md                        # 🔴 私有（不发布）
└── .gitignore                     # 包含 PLAN.md
```

### .gitignore 配置

确保以下内容在 `.gitignore` 中：

```
# 私有规划文档
PLAN.md

# 环境变量和敏感信息
.env
.env.local
.env.*.local

# API密钥和凭证
credentials.json
secrets.yaml

# 用户测试数据
data/
*.db
backups/

# 日志文件
logs/
*.log
```

---

## 公开发布流程

当准备发布到GitHub时：

### 1. 本地准备
```bash
# 创建feature分支
git checkout -b feature/documentation

# 添加公开文档
git add docs/

# 确保PLAN.md在.gitignore中
echo "PLAN.md" >> .gitignore
git add .gitignore
```

### 2. 验证步骤
```bash
# 检查将要提交的文件
git diff --cached --stat

# 确保PLAN.md不在提交列表中
git status | grep PLAN.md  # 应该显示: On branch...
```

### 3. 提交并推送
```bash
git commit -m "Add public documentation: architecture, development, database, LLM config, and deployment guides"
git push origin feature/documentation
```

### 4. 创建Pull Request
- 标题：Add comprehensive public documentation
- 描述：包含创建的文档列表和概述

---

## 文档维护

### 定期审查

每个月审查一次文档：
- [ ] 检查内容是否仍然准确
- [ ] 检查是否有新发现的敏感信息
- [ ] 更新链接和参考
- [ ] 根据开发进展更新示例

### 更新流程

当更新文档时：

```bash
# 创建更新分支
git checkout -b docs/update-xxx

# 编辑文档
nano docs/ARCHITECTURE.md

# 验证没有敏感信息
grep -i "user\|password\|api_key" docs/

# 提交更新
git add docs/
git commit -m "Update documentation: [specific changes]"
git push origin docs/update-xxx
```

---

## 特定文档的敏感信息处理

### DEVELOPMENT.md 处理

**原始PLAN.md中的内容**：
```
#### Phase 2：生活记录系统（2周）
用户需要...行动力较差...需要push...
约5个事件/天...3个活跃计划...
```

**公开DEVELOPMENT.md中的表述**：
```
#### Phase 2：生活记录系统（2周）
实现通过对话记录生活事件的核心功能...
典型使用场景包括记录日常活动、工作进展等
```

**关键改变**：
- ❌ 移除个人特征描述
- ✅ 保留技术要求
- ✅ 用通用表述替换具体数据

### DATABASE.md 处理

**数据示例**：
- ✅ 使用通用用户ID（user_001）
- ✅ 使用通用数据（"项目A"而不是"我的真实项目"）
- ✅ 保留数据结构清晰

### LLM_CONFIG.md 处理

**API密钥**：
- ✅ 使用占位符（your_api_key_here）
- ✅ 详细说明密钥管理最佳实践
- ✅ 警告不要提交真实密钥

---

## 常见问题

**Q: 为什么要分开公开和私有文档？**
A: 这样既能开源代码提高透明度，又能保护用户的个人信息和隐私。

**Q: PLAN.md可以共享给其他开发者吗？**
A: 可以，但应该：
1. 通过安全的私有渠道（不是GitHub）
2. 告知接收者这是私人信息
3. 确保开发者签署NDA或保密协议

**Q: 如何处理用户测试数据？**
A:
1. 测试数据只保存在本地（不提交到仓库）
2. 如需分享，使用匿名或虚拟数据
3. 真实用户数据绝不发布

**Q: 如果无意中提交了敏感信息怎么办？**
A:
```bash
# 从历史中删除
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch PLAN.md' \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（仅在必要时）
git push origin --force --all
```

---

## 合规性考虑

### 数据保护
- GDPR合规：欧盟用户数据保护
- CCPA合规：加州消费者隐私保护
- 行业标准：遵循开源最佳实践

### 许可证
所有公开文档应包含适当的许可证头：
```
# This file is part of Mindflow
# Licensed under [LICENSE_TYPE]
```

### 审计
定期审计公开仓库的内容：
```bash
# 搜索潜在的敏感关键词
git grep -i "password\|api_key\|secret" -- docs/

# 检查大文件
git ls-files -z | xargs -0 du -h | sort -rh | head -20
```

---

## 总结

| 文档 | 位置 | 发布 | 原因 |
|------|------|------|------|
| ARCHITECTURE.md | docs/ | ✅ 公开 | 技术设计 |
| DEVELOPMENT.md | docs/ | ✅ 公开 | 开发指南 |
| DATABASE.md | docs/ | ✅ 公开 | 数据库文档 |
| LLM_CONFIG.md | docs/ | ✅ 公开 | 配置指南 |
| DEPLOYMENT.md | docs/ | ✅ 公开 | 部署指南 |
| README.md | docs/ | ✅ 公开 | 文档导航 |
| PLAN.md | 根目录 | 🔴 私有 | 个人信息 |
| .env | 根目录 | 🔴 私有 | 敏感配置 |

---

## 下一步

1. ✅ 创建公开文档（已完成）
2. ⏳ 将公开文档提交到GitHub
3. ⏳ 在仓库中添加指向文档的README链接
4. ⏳ 建立定期审查计划
5. ⏳ 为社区贡献者创建文档指南

---

更新日期：2024年12月3日
